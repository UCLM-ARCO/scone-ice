#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-
import sys
import Ice
import socket

Ice.loadSlice('SconeWrapper.ice')
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

        adapter = broker.createObjectAdapter("SconeWrapperAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("sconeService"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
