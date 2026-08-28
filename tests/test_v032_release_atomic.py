import platform
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from sparkbrain import release_atomic
from sparkbrain.release_atomic import atomic_publish_directory_noreplace

pytestmark = [pytest.mark.slow, pytest.mark.reproduction]


@pytest.mark.skipif(
    platform.system() not in {'Linux', 'Darwin', 'Windows'},
    reason='unsupported platform',
)
def test_atomic_directory_publish_never_clobbers(tmp_path: Path):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'ours').write_text('ours')
    destination = tmp_path / 'destination'
    destination.mkdir()
    (destination / 'theirs').write_text('theirs')
    with pytest.raises(FileExistsError):
        atomic_publish_directory_noreplace(source, destination)
    assert (destination / 'theirs').read_text() == 'theirs'
    assert source.exists()


@pytest.mark.skipif(
    platform.system() not in {'Linux', 'Darwin', 'Windows'},
    reason='unsupported platform',
)
def test_atomic_directory_publish_success(tmp_path: Path):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'payload').write_text('ok')
    destination = tmp_path / 'destination'
    atomic_publish_directory_noreplace(source, destination)
    assert not source.exists()
    assert (destination / 'payload').read_text() == 'ok'


@pytest.mark.skipif(
    platform.system() not in {'Linux', 'Darwin', 'Windows'},
    reason='unsupported platform',
)
def test_concurrent_publish_has_exactly_one_winner(tmp_path: Path):
    sources = []
    for index in range(2):
        source = tmp_path / f'source-{index}'
        source.mkdir()
        (source / 'winner.txt').write_text(str(index), encoding='utf-8')
        sources.append(source)
    destination = tmp_path / 'destination'

    def publish(source: Path) -> str:
        try:
            atomic_publish_directory_noreplace(source, destination)
        except FileExistsError:
            return 'lost'
        return 'won'

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(publish, sources))
    assert sorted(outcomes) == ['lost', 'won']
    assert (destination / 'winner.txt').read_text(encoding='utf-8') in {'0', '1'}
    assert sum(source.exists() for source in sources) == 1


@pytest.mark.parametrize(
    ('system', 'function_name'),
    [
        ('Linux', '_linux_rename_noreplace'),
        ('Darwin', '_darwin_rename_noreplace'),
        ('Windows', '_windows_rename_noreplace'),
    ],
)
def test_platform_dispatch_is_explicit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    system: str,
    function_name: str,
):
    source = tmp_path / 'source'
    source.mkdir()
    destination = tmp_path / 'destination'
    called = []

    def fake(src: Path, dst: Path) -> None:
        called.append((src, dst))

    monkeypatch.setattr(release_atomic.platform, 'system', lambda: system)
    monkeypatch.setattr(release_atomic, function_name, fake)
    atomic_publish_directory_noreplace(source, destination)
    assert called == [(source.resolve(), destination.resolve())]


def test_unsupported_platform_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source = tmp_path / 'source'
    source.mkdir()
    monkeypatch.setattr(release_atomic.platform, 'system', lambda: 'UnknownOS')
    with pytest.raises(OSError, match='unsupported'):
        atomic_publish_directory_noreplace(source, tmp_path / 'destination')


def test_source_symlink_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / 'source'
    source.mkdir()
    link = tmp_path / 'source-link'
    try:
        link.symlink_to(source, target_is_directory=True)
    except OSError:
        pytest.skip('directory symlinks are not available')
    with pytest.raises(ValueError, match='symbolic links'):
        atomic_publish_directory_noreplace(link, tmp_path / 'destination')
    assert source.is_dir()
