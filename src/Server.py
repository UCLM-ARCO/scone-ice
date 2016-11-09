#!/usr/bin/python3 -u
# -*- coding:utf-8; tab-width:4; mode:python -*-

import os
import sys
import Ice
import socket
import time
import signal
# from commodity.os_ import SubProcess
from subprocess import Popen
import scone_client
import logging

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.INFO)


slice_dir = "/usr/share/slice"
Ice.loadSlice("-I{0} {0}/dharma/dharma.ice --all".format(slice_dir))
import Semantic


class SconeServiceI(Semantic.SconeService):
    def __init__(self, host):
        self.host = host
        self.client = self.patient_connect()
        if self.client:
            logging.info("connection OK")
        else:
            raise SystemExit("connection FAILED!")

    def patient_connect(self):
        logging.info("Trying to connect to scone-server...")
        for i in range(20):
            try:
                return scone_client.SconeClient('127.0.0.1', 6517)
            except socket.error:
                time.sleep(0.4)

        return None

    def sconeRequest(self, msg, current=None):
        try:
            return self.client.send(msg)
        except scone_client.SconeError as e:
            raise Semantic.SconeError(str(e))

    # def checkpoint(self, s, size, prompt):
    #     checkpoint_file = "/var/lib/dharma/checkpoint.lisp"
    #     checkpoint = "(checkpoint-new \"" + checkpoint_file + "\")\n"

    #     answer = s.recv(size)
    #     if (answer == prompt):
    #         s.send(checkpoint)
    #         checkpoint_answer = s.recv(size)
    #         print(checkpoint_answer)


class Server(Ice.Application):
    def run(self, args):
        host = "localhost"
        if len(args) > 1:
            host = args[1]

        broker = self.communicator()
        self.scone_path = os.path.expanduser(
            broker.getProperties().getProperty('SconeServer.path'))

        if not self.scone_path:
            print("Error: set 'SconeServer.path' property")
            return 1

        try:
            self.start_scone_server()
            servant = SconeServiceI(host)
            adapter = broker.createObjectAdapter("SconeAdapter")
            proxy = adapter.add(servant, broker.stringToIdentity("scone"))

            print(proxy)
            sys.stdout.flush()

            adapter.activate()
            self.shutdownOnInterrupt()
            broker.waitForShutdown()
        finally:
            self.stop_scone_server()
            pass

        return 0

    def start_scone_server(self):
        self.scone_server = Popen(['/bin/bash', '-c', './server.sh'],
                                  cwd=self.scone_path)
        logging.info("scone-server started PID:{}".format(self.scone_server.pid))

    def stop_scone_server(self):
        self.scone_server.send_signal(signal.SIGINT)
        logging.info("scone-server terminated")


sys.exit(Server().main(sys.argv))
