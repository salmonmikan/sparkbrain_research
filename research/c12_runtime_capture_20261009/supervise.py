"""Linux-only, one-attempt prospective launcher; no admission or Phase B path."""
import os
import sys
import json
import time
import signal
import resource
import selectors
import subprocess
import hashlib

WALL = 30
CPU = 15
MEMORY = 512 * 1024 * 1024
OUTPUT = 4 * 1024 * 1024


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')


def limits():
    # Installed in the child BEFORE exec of the target interpreter.
    resource.setrlimit(resource.RLIMIT_CPU, (CPU, CPU))
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY, MEMORY))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT, OUTPUT))


def launch(manifest_path, collector, output_dir, bootstrap=None, emit_logs=False):
    start = time.monotonic()
    deadline = start + WALL
    if sys.platform != 'linux' or not hasattr(os, 'O_NOFOLLOW'):
        raise RuntimeError('UNSUPPORTED_SUPERVISOR_PLATFORM')
    # No discovery, installer, automatic retry or target preflight subprocess.
    for path in ([collector] if bootstrap is not None else [manifest_path, collector]):
        if not os.path.isabs(path) or os.path.realpath(path) != path:
            raise RuntimeError('NONCANONICAL_INPUT')
    if bootstrap is None:
        with open(manifest_path, 'rb') as stream:
            raw = stream.read(65537)
        if len(raw) > 65536:
            raise RuntimeError('MANIFEST_SIZE')
        manifest = json.loads(raw)
    else:
        manifest = bootstrap
    executable = manifest['executable']
    if not os.path.isabs(executable) or os.path.realpath(executable) != executable:
        raise RuntimeError('NONCANONICAL_EXECUTABLE')
    with open(collector, 'rb') as stream:
        source = stream.read(1024 * 1024 + 1)
    child_env = {}
    if bootstrap is not None:
        prefix = manifest['runtime_prefix']
        if prefix != '/opt/hostedtoolcache/Python/3.14.8/x64' or os.path.realpath(prefix) != prefix:
            raise RuntimeError('NONOFFICIAL_RUNTIME_PREFIX')
        # Only the explicitly approved public runtime loader directory is passed;
        # never inherit runner credentials, tokens or unrelated environment data.
        child_env = {'LD_LIBRARY_PATH': prefix + '/lib'}
        raw = canonical(manifest)
    if len(source) > 1024 * 1024 or hashlib.sha256(source).hexdigest() != manifest['capture_sha256']:
        raise RuntimeError('CAPTURE_SOURCE_MISMATCH')
    if not os.path.isabs(output_dir) or os.path.realpath(os.path.dirname(output_dir)) != os.path.dirname(output_dir):
        raise RuntimeError('NONCANONICAL_OUTPUT')
    os.mkdir(output_dir, 0o700)  # Exclusive attempt reservation; never reuse or retry.
    receipt = {'status': 'INCOMPLETE', 'attempt_id': manifest['attempt_id'],
               'native_admission': False, 'scientific_execution': False,
               'trusted_pins_approved': False, 'target_capture_attempts': 0,
               'network_isolation_established': False,
               'read_limit_scope': 'explicit collector reads only; loader I/O excluded',
               'limits': {'wall_seconds': WALL, 'cpu_seconds': CPU,
                          'address_space_bytes': MEMORY, 'combined_output_bytes': OUTPUT},
               'process_policy': 'one target; collector creates no descendants; no OS fork containment'}
    proc = None
    body = bytearray()
    def deadline_signal(signum, frame):
        raise RuntimeError('OUTER_TIMEOUT_SIGNAL')
    # GNU timeout TERM enters the cleanup path once Popen has returned.
    # Startup before a process handle exists retains the documented limitation.
    signal.signal(signal.SIGTERM, deadline_signal)
    # Combined stdout/stderr are capped; receipt and log framing reserve 8192 bytes.
    try:
        if time.monotonic() >= deadline:
            raise RuntimeError('DEADLINE_BEFORE_START')
        receipt['target_capture_attempts'] = 1
        proc = subprocess.Popen([executable, '-I', '-S', '-B', collector],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, env=child_env, cwd=output_dir,
                                start_new_session=True, preexec_fn=limits)
        # Small fixed manifest input; bounded by 64 KiB. Nonblocking handles avoid
        # a malicious/failed startup preventing the parent from enforcing wall time.
        os.set_blocking(proc.stdin.fileno(), False)
        os.set_blocking(proc.stdout.fileno(), False)
        selector = selectors.DefaultSelector()
        selector.register(proc.stdin, selectors.EVENT_WRITE, 'input')
        selector.register(proc.stdout, selectors.EVENT_READ, 'output')
        offset, ended = 0, False
        try:
            while not ended:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise RuntimeError('WALL_LIMIT')
                for key, _ in selector.select(min(remaining, 0.1)):
                    if key.data == 'input':
                        try:
                            offset += os.write(proc.stdin.fileno(), raw[offset:])
                        except BrokenPipeError:
                            offset = len(raw)
                        if offset == len(raw):
                            selector.unregister(proc.stdin)
                            proc.stdin.close()
                    else:
                        chunk = os.read(proc.stdout.fileno(), min(65536, OUTPUT - 8192 - len(body) + 1))
                        if not chunk:
                            ended = True
                            selector.unregister(proc.stdout)
                            break
                        if len(body) + len(chunk) > OUTPUT - 8192:
                            raise RuntimeError('OUTPUT_LIMIT')
                        body.extend(chunk)
            proc.wait(timeout=max(0.001, deadline - time.monotonic()))
            receipt['returncode'] = proc.returncode
            receipt['status'] = 'CAPTURE_PROCESS_EXITED' if proc.returncode == 0 else 'CAPTURE_INCOMPLETE'
        finally:
            selector.close()
    except Exception as exc:
        receipt['reason'] = ('TARGET_RUNTIME_UNAVAILABLE' if type(exc) is FileNotFoundError
                             else str(exc) if type(exc) is RuntimeError else type(exc).__name__)
    finally:
        if proc is not None:
            # Kill entire process group even if its leader exited; no late writers.
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            # No unbounded wait beyond the deadline. Kernel D-state may delay reap;
            # report that limitation rather than invent guaranteed hard termination.
            try:
                proc.wait(timeout=max(0.001, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                receipt['termination_unconfirmed'] = True
            proc.stdout.close()
            if not proc.stdin.closed:
                proc.stdin.close()
        receipt['elapsed_seconds'] = time.monotonic() - start
        receipt['captured_stream_bytes'] = len(body)
        encoded = canonical(receipt)
        if len(encoded) > 4096:
            raise RuntimeError('RECEIPT_LIMIT')
        if emit_logs:
            # Public hosted-runtime observations only, after separate user approval.
            # No duplicate evidence files/artifact uploads in this delivery mode.
            sys.stdout.buffer.write(b'C12_CAPTURE_STREAM_BEGIN\n' + body +
                                    b'\nC12_CAPTURE_STREAM_END\nC12_SUPERVISOR_RECEIPT\n' +
                                    encoded + b'\n')
            sys.stdout.buffer.flush()
        else:
            for name, payload in (('capture.stream', body), ('supervisor.json', encoded)):
                fd = os.open(os.path.join(output_dir, name), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(payload)
    return receipt


if __name__ == '__main__':
    if len(sys.argv) == 8 and sys.argv[1] == '--bootstrap':
        _, _, executable, prefix, collector, output, attempt, expected_capture_sha = sys.argv
        # Bind implementation bytes to the reviewed workflow literal before launch.
        with open(collector, 'rb') as stream:
            candidate = stream.read(1024 * 1024 + 1)
        if hashlib.sha256(candidate).hexdigest() != expected_capture_sha:
            raise SystemExit('CAPTURE_SOURCE_MISMATCH')
        config = {'schema': 'c12-phase-a-bootstrap-v1', 'attempt_id': attempt,
                  'executable': executable, 'runtime_prefix': prefix,
                  'capture_sha256': expected_capture_sha}
        result = launch(None, collector, output, bootstrap=config, emit_logs=True)
    elif len(sys.argv) == 4:
        result = launch(*sys.argv[1:])
    else:
        raise SystemExit('usage: supervise.py MANIFEST COLLECTOR OUTPUT; or --bootstrap EXE PREFIX COLLECTOR OUTPUT ATTEMPT CAPTURE_SHA')
    raise SystemExit(0 if result['status'] == 'CAPTURE_PROCESS_EXITED' else 2)
