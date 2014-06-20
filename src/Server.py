#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import os
import Ice
import socket
from commodity.os_ import SubProcess


pwd = os.path.dirname(__file__)
slice_path = os.path.join(pwd, 'SconeWrapper.ice')
Ice.loadSlice(slice_path)
import SconeWrapper


class SconeServiceI(SconeWrapper.SconeService):
    def sconeRequest(self, str, current=None):
        print str

        size = 1024
        prompt = "[PROMPT]\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 5000))

        answer = s.recv(size)
        if (answer == prompt):
            s.send(str)
            answer = s.recv(size)
            print answer

        return answer


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SconeServiceI()

        self.start_scone()
        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("sconeService"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        self.stop_scone()
        return 0

    def start_scone(self):
        SubProcess("./start-server 5000 -noxml", cwd="/opt/scone/scone-server-1.0/")

    def stop_scone(self):
        SubProcess("./stop-server", cwd="/opt/scone/scone-server-1.0/")


server = Server()
sys.exit(server.main(sys.argv))
