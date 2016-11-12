# Install

* Configure Debian testing (stretch) mirror
* Add [pike repository](http://pike.esi.uclm.es/)
* sudo apt install scone-wrapper


# Running

    $ scone-wrapper
    INFO:root:scone-server started PID:24329
    INFO:root:Trying to connect to scone-server...
    Config: port: 6517, xml: nil, host=0.0.0.0

    All error and log messages will be printed to "SCONE-SERVER.LOG")...
    Server started. Press C-c to stop
    INFO:root:connection OK
    scone -t -e 1.1:tcp -h 10.130.89.144 -p 5001 -t 60000
    ...

# Local knowledge

If you want upload local knowledge, save on .lisp files in a subdirectory called `scone-knowledge.d`. All ".lisp" files on directories and subdirectories are loaded in alphabetic order.

Start `scone-wrapper` from parent:

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

# Using checkpoints

The scone-wrapper client may issue:

    scone_proxy.request('(checkpoint "new-things")')

Then server generates a file at:

    <working-dir>/scone-knowledge.d/snapshots/new-things.lisp

When you restart the server, these files will be loaded as the other local knowledge.


# Run from repository

To start scone-wrapper from repository contents run:

    scone.wrapper/src$ Server.py --Ice.Config=Server.config
