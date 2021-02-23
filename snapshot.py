import os
import signal
import traceback

SNAPSHOTS = []


def is_in_snapshot():
    return len(SNAPSHOTS) > 0


def not_in_snapshot(f):
    def __inner(*args, **kwargs):
        if not SNAPSHOTS:
            return f(*args, **kwargs)
    return __inner


def format_snapshot_list(context_frames=3):
    result = ''
    for i, (pid, bt) in enumerate(SNAPSHOTS):
        result += '=' * 20 + f' Snapshot #{i} ' + '=' * 20 + '\n'
        result += '\n'.join(bt[-context_frames:])
    return result


def print_snapshot_list(context_frames=3):
    print(format_snapshot_list(context_frames=context_frames))


def snapshot(context=None):
    global SNAPSHOTS
    child_pid = os.fork()

    context = context if context is not None else traceback.format_stack()

    if child_pid == 0:
        # in the child we act like nothing happened
        my_pid = os.getpid()
        print(f"SNAPSHOT process pid={my_pid} created, continuing in snapshot.")
        SNAPSHOTS.append((my_pid, context))
        return True

    def sig_to_child(signum, frame):
        os.kill(child_pid, signum)

    # ignore SIGINT as that should go to the child process only until it terminates
    old_handler = signal.signal(signal.SIGINT, sig_to_child)
    pid, status = os.waitpid(child_pid, 0)
    assert pid == child_pid
    if os.WIFEXITED(status):
        exit_code = os.WEXITSTATUS(status)
        print(f"SNAPSHOT pid={child_pid} reverted! Exited with exit code {exit_code}!")
    elif os.WIFSIGNALED(status):
        signum = os.WTERMSIG(status)
        signame = signal.Signals(signum)
        print(f"SNAPSHOT pid={child_pid} reverted! Exited with signal {signum}[{signame}]!")
    else:
        print(f"What the hell kind of waitpid result is this?????? (pid={pid}, status={status})")
        import ipdb; ipdb.set_trace()
        assert False

    # we're done handling it, reset the SIGINT handler
    signal.signal(signal.SIGINT, old_handler)
    print(f"Reverted to snapshot #{len(SNAPSHOTS)} with pid={os.getpid()}!")
    print('\n'.join(context[-3:]))
    return False


def set_trace(debugger='ipdb'):
    dbg = __import__(debugger)
    dbg.set_trace()
    snapshot()
