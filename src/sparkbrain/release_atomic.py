from __future__ import annotations

import ctypes
import errno
import os
import platform
from pathlib import Path

AT_FDCWD = -100
RENAME_NOREPLACE = 1
DARWIN_RENAME_EXCL = 0x00000004


def _raise_errno(operation: str, source: Path, destination: Path) -> None:
    code = ctypes.get_errno()
    if code in {errno.EEXIST, errno.ENOTEMPTY}:
        raise FileExistsError(code, os.strerror(code), str(destination))
    raise OSError(code, f"{operation}: {os.strerror(code)}", f"{source} -> {destination}")


def _linux_rename_noreplace(source: Path, destination: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    func = getattr(libc, 'renameat2', None)
    if func is None:
        raise OSError(errno.ENOSYS, 'renameat2(RENAME_NOREPLACE) is unavailable')
    func.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    func.restype = ctypes.c_int
    result = func(
        AT_FDCWD,
        os.fsencode(source),
        AT_FDCWD,
        os.fsencode(destination),
        RENAME_NOREPLACE,
    )
    if result != 0:
        _raise_errno('renameat2(RENAME_NOREPLACE)', source, destination)


def _darwin_rename_noreplace(source: Path, destination: Path) -> None:
    libc = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True)
    func = getattr(libc, 'renamex_np', None)
    if func is None:
        raise OSError(errno.ENOSYS, 'renamex_np(RENAME_EXCL) is unavailable')
    func.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    func.restype = ctypes.c_int
    result = func(os.fsencode(source), os.fsencode(destination), DARWIN_RENAME_EXCL)
    if result != 0:
        _raise_errno('renamex_np(RENAME_EXCL)', source, destination)


def _windows_rename_noreplace(source: Path, destination: Path) -> None:
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    move_file = kernel32.MoveFileW
    move_file.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
    move_file.restype = ctypes.c_int
    if not move_file(str(source), str(destination)):
        code = ctypes.get_last_error()
        if code in {80, 183}:  # ERROR_FILE_EXISTS / ERROR_ALREADY_EXISTS
            raise FileExistsError(code, 'destination already exists', str(destination))
        raise OSError(code, ctypes.FormatError(code), f'{source} -> {destination}')


def atomic_publish_directory_noreplace(
    source: str | os.PathLike[str],
    destination: str | os.PathLike[str],
) -> None:
    """Atomically publish *source* without replacing an existing destination.

    The primitive deliberately fails when the platform cannot provide a native
    no-replace rename. It never degrades to an exists-check followed by rename.
    Source and destination must reside on the same filesystem.
    """
    source_path = Path(source)
    destination_path = Path(destination)
    if source_path.is_symlink() or destination_path.is_symlink():
        raise ValueError("atomic publish paths must not be symbolic links")
    src = Path(os.path.abspath(source_path))
    dst = Path(os.path.abspath(destination_path))
    if not src.exists():
        raise FileNotFoundError(src)
    if not src.is_dir():
        raise NotADirectoryError(src)
    system = platform.system()
    if system == 'Linux':
        _linux_rename_noreplace(src, dst)
    elif system == 'Darwin':
        _darwin_rename_noreplace(src, dst)
    elif system == 'Windows':
        _windows_rename_noreplace(src, dst)
    else:
        raise OSError(
            errno.ENOSYS,
            f'atomic no-replace directory publish is unsupported on {system}',
        )
