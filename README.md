# snapshot
A small python library to create process snapshots for debugging long-running processes. Let's you debug with impunity and on exit it will revert back to the original snapshot state.

# Installation

```bash
git clone https://github.com/Lukas-Dresel/snapshot.git
pip install -e ./snapshot
```

# Usage

```python
from snapshot import snapshot

# create a new snapshot to work with, revert to here on exit
snapshot()
```

[![demo](https://asciinema.org/a/389733.svg)](https://asciinema.org/a/389733?autoplay=1)

# How does it work?

The actual logic of this module is 7 lines of python. It uses the `fork()` system call to create a copy of your current process in which you can perform any and all operations that you want to test out. Whenever you make a mistake or are done experimenting in your current snapshot simply exit the process, and you will continue in the original process.

The snapshot function boils down to this:

```python
def snapshot():
    child_pid = os.fork()
    if child_pid == 0:
        return True
    pid, status = os.waitpid(child_pid, 0)
    assert os.WIFEXITED(status) or os.WIFSIGNALED(status)
    return False
```

# Limitations

As of now, this is very rudimentary, it's a simple `fork()` to clone the process state. This does not roll back any operating system state, including: 
1. File system changes
2. Connection state in sockets, including the data sent and received
3. any managed system resources: docker containers, file locks, files, temporary files, etc.

Another issue that you will often see is context managers associated with these resources, e.g. temporary files, subprocesses, etc. that will be closed on termination of the child process. These effects will propagate to the original state when debugging and will likely cause errors.

# Todo
- Flesh out utilities to implement root-process-only operations to reduce errors from the above limitations, e.g. closed files, etc.
- Fix issue with IPython where sometimes you get a file does not exist error on reverting to snapshot
- Fix Ctrl+c sometimes killing the original process
