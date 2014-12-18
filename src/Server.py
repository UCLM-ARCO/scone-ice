#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import os
import Ice
import socket
from commodity.os_ import SubProcess

dharma_root = "/usr/share/slice/dharma"
Ice.loadSlice("-I {} {}/dharma.ice".format(Ice.getSliceDir(), dharma_root))
import SemanticModel


class SconeServiceI(SemanticModel.SconeService):
    def __init__(self, host):
        self.host = host

    def sconeRequest(self, msg, current=None):
        print msg

        size = 1024
        prompt = "[PROMPT]\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, 5000))

        answer = s.recv(size)
        if (answer == prompt):
            s.send(msg)
            answer = s.recv(size)
            print answer

        return answer


class Server(Ice.Application):
    def run(self, args):
        host = "localhost"
        if len(args) > 1:
            host = args[1]

        broker = self.communicator()
        self.scone_path = broker.getProperties().getProperty('SconeServer.path')
        if not self.scone_path:
            print "Error: set 'SconeServer.path' property"
            return 1

        servant = SconeServiceI(host)

        # self.start_scone()
        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("scone"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        # self.stop_scone()
        return 0

    def start_scone(self):
        SubProcess("./start-server 5000 -noxml", cwd=self.scone_path)

    def stop_scone(self):
        SubProcess("./stop-server", cwd=self.scone_path)


sys.exit(Server().main(sys.argv))
