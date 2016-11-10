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

LOCAL_KNOWLEDGE = 'scone-knowledge.d'


class SconeServiceI(Semantic.SconeService):
    def __init__(self, host):
        self.host = host
        self.client = self.patient_connect()
        if self.client:
            logging.info("connection OK")
        else:
            raise SystemExit("connection FAILED!")

        if os.path.exists(LOCAL_KNOWLEDGE):
            self.load_local_knowledge()

    def load_local_knowledge(self):
        logging.info("Uploading local knowledge...")

        for fname in os.listdir(LOCAL_KNOWLEDGE):
            self.load_local_file(os.path.join(LOCAL_KNOWLEDGE, fname))

    def load_local_file(self, fname):
        error = False
        with open(fname, mode='rt') as f:
            for i, sentence in enumerate(f.readlines()):
                try:
                    self.client.sentence(sentence)
                except scone_client.SconeError as e:
                    logging.error("{}:{} returns '{}'".format(fname, i + 1, e))
                    error = True
                    break

        if error:
            raise SystemExit("Error loading '{}'.".format(fname))

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
        cmd = '/bin/bash -c scone-server'.split()
        self.scone_server = Popen(cmd)
        logging.info("scone-server started PID:{}".format(self.scone_server.pid))

    def stop_scone_server(self):
        self.scone_server.send_signal(signal.SIGINT)
        logging.info("scone-server terminated OK")


try:
    sys.exit(Server().main(sys.argv))
except SystemExit:
    sys.exit(1)
