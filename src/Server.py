#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import os
import Ice
import socket
from commodity.os_ import SubProcess

slice_dir = "/usr/share/slice"
Ice.loadSlice("-I{0} {0}/dharma/dharma.ice --all".format(slice_dir))
import Semantic


class SconeServiceI(Semantic.SconeService):
    def __init__(self, host):
        self.host = host

    def sconeRequest(self, msg, current=None):

        size = 1024
        prompt = "[PROMPT]\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, 5000))

        answer = s.recv(size)
        if (answer == prompt):
            s.send(msg)
            answer = s.recv(size)
            print(answer)
            #self.checkpoint(s, size, prompt)

        return answer

    def checkpoint(self, s, size, prompt):
        checkpoint_file = "/var/lib/dharma/checkpoint.lisp"
        checkpoint = "(checkpoint-new \"" + checkpoint_file + "\")\n"

        answer = s.recv(size)
        if (answer == prompt):
            s.send(checkpoint)
            checkpoint_answer = s.recv(size)
            print(checkpoint_answer)


class Server(Ice.Application):
    def run(self, args):
        host = "localhost"
        if len(args) > 1:
            host = args[1]

        broker = self.communicator()
        self.scone_path = broker.getProperties().getProperty('SconeServer.path')
        if not self.scone_path:
            print("Error: set 'SconeServer.path' property")
            return 1

        servant = SconeServiceI(host)

        self.start_scone()
        adapter = broker.createObjectAdapter("SconeAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("scone"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        self.stop_scone()
        return 0

    def start_scone(self):
        SubProcess("./start-server 5000 -noxml", cwd=self.scone_path)

    def stop_scone(self):
        SubProcess("./stop-server", cwd=self.scone_path)


sys.exit(Server().main(sys.argv))
