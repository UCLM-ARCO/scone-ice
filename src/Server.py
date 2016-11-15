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
logging.getLogger().setLevel(logging.DEBUG)


slice_dir = "/usr/share/slice"
Ice.loadSlice("-I{0} {0}/dharma/dharma.ice --all".format(slice_dir))
import Semantic

LOCAL_KNOWLEDGE_DIR = 'scone-knowledge.d'
SNAPSHOT_DIR = 'snapshots'

SCONE_STATE = '.scone'
PROXY_FILE = os.path.join(SCONE_STATE, 'scone-wrapper.proxy')


def iterate_files(path, callback):
    def walk(path):
        for root, dirs, files in os.walk(path):
            files = [x for x in sorted(files) if x.endswith('.lisp')]
            dirs.sort()
            if SNAPSHOT_DIR in dirs:
                del dirs[dirs.index(SNAPSHOT_DIR)]

            for f in files:
                callback(os.path.join(root, f))

    walk(path)
    walk(os.path.join(path, SNAPSHOT_DIR))


class SconeServiceI(Semantic.SconeService):
    def __init__(self, host):
        self.host = host
        self.client = self.patient_connect()
        if self.client:
            logging.info("connection OK")
        else:
            raise SystemExit("connection FAILED!")

        self.load_local_knowledge()

    def load_local_knowledge(self):
        if not os.path.exists(LOCAL_KNOWLEDGE_DIR):
            return

        logging.info("Uploading local knowledge...")
        iterate_files(LOCAL_KNOWLEDGE_DIR, self.load_local_file)

    def load_local_file(self, fname):
        logging.info("Loading '{}'".format(fname))

        try:
            self.client.sentence('(load-kb "{}")'.format(os.path.abspath(fname)))
        except scone_client.SconeError as e:
            logging.error("{} returns '{}'".format(fname, e))
            raise SystemExit("Error loading '{}'.".format(fname))

    def patient_connect(self):
        logging.info("Trying to connect to scone-server...")
        for i in range(20):
            try:
                return scone_client.SconeClient('127.0.0.1', 6517)
            except socket.error:
                time.sleep(0.4)

        return None

    def do_sentence(self, msg):
        try:
            return self.client.send(msg)
        except scone_client.SconeError as e:
            raise Semantic.SconeError(str(e))

    def sentence(self, msg, current=None):
        return self.do_sentence(msg)

    def sconeRequest(self, msg, current=None):
        return self.do_sentence(msg)

    def checkpoint(self, fname, current=None):
        path = os.path.join(LOCAL_KNOWLEDGE_DIR, SNAPSHOT_DIR)
        if not os.path.isdir(path):
            os.makedirs(path)

        fpath = os.path.abspath(os.path.join(path, fname + '.lisp'))
        if os.path.exists(fpath):
            raise Semantic.FileError("File {} already exists".format(fpath))

        sentence = '(checkpoint-new "{}")'.format(fpath)
        self.client.sentence(sentence)
        logging.info("New checkpoint at '{}' was OK".format(fpath))


def save_proxy_to_file(proxy):
    if not os.path.isdir(SCONE_STATE):
        os.mkdir(SCONE_STATE)

    with open(PROXY_FILE, 'wt') as f:
        f.write('"{}"'.format(proxy))


def remove_proxy_file():
    if os.path.exists(PROXY_FILE):
        os.remove(PROXY_FILE)


class Server(Ice.Application):
    def run(self, args):
        host = "localhost"
        if len(args) > 1:
            host = args[1]

        self.scone_server = None
        broker = self.communicator()

        try:
            self.start_scone_server()
            servant = SconeServiceI(host)
            adapter = broker.createObjectAdapter("SconeAdapter")
            proxy = adapter.add(servant, broker.stringToIdentity("scone"))

            print(proxy)
            save_proxy_to_file(proxy)

            sys.stdout.flush()

            adapter.activate()
            self.shutdownOnInterrupt()
            broker.waitForShutdown()

        except Ice.SocketException:
            logging.error("scone-wrapper already running!")
            return 1

        finally:
            self.stop_scone_server()
            remove_proxy_file()

        return 0

    def start_scone_server(self):
        cmd = '/bin/bash -c scone-server'.split()
        self.scone_server = Popen(cmd)
        logging.info("scone-server started PID:{}".format(self.scone_server.pid))

    def stop_scone_server(self):
        logging.info("\nterminating scone-server...")

        server = self.scone_server
        if server is None:
            return

        for i in range(10):
            if server.poll():
                break

            server.send_signal(signal.SIGINT)
            time.sleep(0.3)

        logging.info("scone-server terminated OK")


if __name__ == '__main__':
    try:
        sys.exit(Server().main(sys.argv))
    except SystemExit:
        sys.exit(1)
