# Install

* Configure Debian testing (stretch) mirror
* Add [arco repository](https://uclm-arco.github.io/debian/)
* sudo apt install scone-wrapper


# Running

```
$ scone-wrapper
INFO:root:scone-server started PID:24329
INFO:root:Trying to connect to scone-server...
Config: port: 6517, xml: nil, host=0.0.0.0

All error and log messages will be printed to "SCONE-SERVER.LOG")...
Server started. Press C-c to stop
INFO:root:connection OK
scone -t -e 1.1:tcp -h 10.130.89.144 -p 5001 -t 60000
...
```

# Stopping the server

The termination of the service is done using the combination Ctrl+C. However, if the server does not properly finish its execution, you will not be able to start it up again. In order to overcome this problem, simply delte `.scone/scone-server.pid`. This will solve the problem.


# Local knowledge

Different knowledge bases can be load automatically during the scone-wrapper startup. This is very convenient if you don't want to mess around with core-kb files or if you are simply doing some tests.

In order to do that, you just have to keep all your .lisp files in a directory called `scone-knowledge.d`. Then, the `scone-wrapper` will have to be launched in the directoy where `scone-knowledge.d` directory is. Please, note that all ".lisp" files contained in the`scone-knowledge.d` directory and its subdirectories are loaded in alphabetic order.

Start `scone-wrapper` from parent:

```
$ ls
scone-knowledge.d

$ ls scone-knowledge.d/
monkeys.lisp

$ cat scone-knowledge.d/monkeys.lisp
(new-indv {Martin} {monkey})
(new-indv {Felix}  {monkey})

$ scone-wrapper
INFO:root:scone-server started PID:24936
INFO:root:Trying to connect to scone-server...
Config: port: 6517, xml: nil, host=0.0.0.0

All error and log messages will be printed to "SCONE-SERVER.LOG")...
Server started. Press C-c to stop
INFO:root:connection OK
INFO:root:Uploading local knowledge...
scone -t -e 1.1:tcp -h 10.130.89.144 -p 5001 -t 60000
...
```

# Using checkpoints

The scone-wrapper client may issue:

    scone_proxy.request('(checkpoint "new-things")')

Then server generates a file at:

    <working-dir>/scone-knowledge.d/snapshots/new-things.lisp

When you restart the server, these files will be loaded as the other local knowledge.


# Run server from the source directory (this repository)

To start scone-wrapper from repository contents run:

    scone.wrapper/src$ Server.py --Ice.Config=Server.config
