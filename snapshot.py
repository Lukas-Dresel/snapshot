import os
import signal


LAYERS = 0


def in_snapshot():
    return LAYERS > 0


def only_outside_snapshot(f):
    def __inner(*args, **kwargs):
        if not LAYERS:
            return f(*args, **kwargs)
    return __inner


def snapshot():
    global LAYERS
    child_pid = os.fork()

    if child_pid == 0:
        # in the child we act like nothing happened
        print(f"SNAPSHOT process pid={os.getpid()} created, continuing in snapshot.")
        LAYERS += 1
        return True

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

    return False


def set_trace(debugger='pdb'):
    snapshot()
    dbg = __import__(debugger)
    dbg.set_trace()
