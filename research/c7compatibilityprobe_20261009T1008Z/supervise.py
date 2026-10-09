"""One attempt: C7 child <=10 wall / <=6 CPU, parent <=20 wall."""
import os, sys, time, signal, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def phase_deadline(global_started, phase_started):
    """Both deadlines include fork/exec and interpreter startup."""
    return min(phase_started + 10, global_started + 20)

def main():
    start = time.monotonic()
    # Exclusive local marker prevents repeated invocation in the same checkout.
    with (ROOT/'ATTEMPT_CONSUMED').open('x') as stream:
        stream.write('SYNTHETIC_ONLY\n')
    rows = []; total_cpu = 0.0
    for suite in ('c7',):
        phase_started = time.monotonic()
        deadline = phase_deadline(start, phase_started)
        if phase_started >= deadline:
            return 1
        pid = os.fork()
        if pid == 0:
            os.setsid()
            os.execv(sys.executable, [sys.executable, '-I', '-S', '-B', str(ROOT/'probe.py'), suite])
        timed_out = False
        while True:
            done, status, usage = os.wait4(pid, os.WNOHANG)
            if done: break
            if time.monotonic() >= deadline:
                timed_out = True
                os.killpg(pid, signal.SIGKILL)
                _, status, usage = os.wait4(pid, 0)
                break
            time.sleep(.01)
        phase_elapsed = time.monotonic() - phase_started
        cpu = usage.ru_utime + usage.ru_stime; total_cpu += cpu
        row = {'suite': suite, 'exit_code': os.waitstatus_to_exitcode(status), 'cpu_seconds': cpu,
               'elapsed_wall_seconds': time.monotonic()-start, 'total_child_cpu': total_cpu,
               'phase_wall_seconds': phase_elapsed, 'phase_wall_limit_seconds': 10,
               'timed_out': timed_out}
        rows.append(row); print(json.dumps(row), flush=True)
        if (row['exit_code'] != 0 or timed_out or phase_elapsed > 10 or
                total_cpu > 6 or row['elapsed_wall_seconds'] > 20):
            return 1
    print(json.dumps({'scope':'SYNTHETIC_ONLY_NOT_NATIVE_ADMISSION','completed':rows}))
    return 0

if __name__ == '__main__':
    sys.exit(main())
