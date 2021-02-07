# snapshot
A small python library to create process snapshots for debugging long-running processes. Let's you debug with impunity and on exit it will revert back to the original snapshot state.

# Installation

```bash
pip install snapshot
```

# Usage

```python
from snapshot import snapshot

# create a new snapshot to work with, revert to here on exit
snapshot()
```

[![demo](https://asciinema.org/a/389733.svg)](https://asciinema.org/a/389733?autoplay=1)

# Limitations

As of now, this is very rudimentary, it's a simple `fork()` to clone the process state. This does not roll back any operating system state, including: 
1. File system changes
2. Connection state in sockets, including the data sent and received
3. any managed system resources: docker containers, file locks, files, temporary files, etc.

Another issue that you will often see is context managers associated with these resources, e.g. temporary files, subprocesses, etc. that will be closed on termination of the child process. These effects will propagate to the original state when debugging and will likely cause errors.

# Todo
- Flesh out utilities to implement non-snapshot only operations to reduce errors from the above limitations, e.g. closed files, etc.
- Fix issue with IPython where sometimes you get a file does not exist error on reverting to snapshot
