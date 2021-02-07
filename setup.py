long_description = '''
snapshot.py is a small library to assist users of the python shell to explore debugging in long running processes.
Calling snapshot() let's you continue interacting with your processes, while keeping the current state as a snapshot.
Then once your interaction with the program ends and the program terminates, it will appear to reset to the state 
at which you ran the `snapshot() command. Under the hood this spawns a new fork()-ed subprocess that you continue 
interacting with, and the original process waits for the child to terminate and let's you continue. This will work 
'''

from setuptools import setup
setup(name='snapshot',
      version='1.0.0',
      py_modules=['snapshot'],
      description='Snapshot the current state and continue interacting, on exit resume with the original snapshotted state.',
      long_description=long_description,
      install_requires=[],
      url='https://github.com/Lukas-Dresel/snapshot',
      author='Lukas-Dresel',
      author_email='lukas.patrick.dresel@gmail.com',
      license='MIT',
      keywords='interpreter debug debugger debugging snapshot'
      )
