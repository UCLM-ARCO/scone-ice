#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

import os
import time
from unittest import TestCase
from subprocess import Popen, PIPE
from hamcrest import is_not

from commodity.path import find_in_ancestors
from commodity.testing import assert_that, wait_that
from commodity.net import localhost, listen_port

import Ice

slice_dir = "/usr/share/slice"
Ice.loadSlice("-I{0} {0}/dharma/dharma.ice --all".format(slice_dir))
import Semantic

project_dir = os.path.abspath(find_in_ancestors('.git', __file__))
SRC_DIR = os.path.join(project_dir, 'src')


class SconeWrapperTest(TestCase):
    def setUp(self):
        assert_that(localhost, is_not(listen_port(5001)))
        cmd = '{0}/Server.py --Ice.Config={0}/Server.config'.format(SRC_DIR)
        self.server = Popen(cmd.split(), stdout=PIPE)
        wait_that(localhost, listen_port(5001))
        self.addCleanup(self.server.terminate)

        ic = Ice.initialize()
        self.addCleanup(ic.destroy)
        str_proxy = 'scone -t:tcp -h localhost -p 5001'
        proxy = ic.stringToProxy(str_proxy)
        self.scone = Semantic.SconeServicePrx.uncheckedCast(proxy)

    def tearDown(self):
        self.server.terminate()
        wait_that(localhost, is_not(listen_port(5001)))

    def test_query(self):
        assert self.scone
        self.assertEquals(
            self.scone.sconeRequest('(is-x-a-y? {elephant} {mammal})'), 'YES')

    def test_exception(self):
        assert self.scone

        try:
            self.scone.sconeRequest('(new-is-a {elephant} {bird})')
            self.fail('exception should be thrown')
        except Semantic.SconeError as e:
            self.assertEquals(e.reason, '{elephant} cannot be a {bird}')


class LocalKnowledgeTest(TestCase):
    def setUp(self):
        assert_that(localhost, is_not(listen_port(5001)))
        self.cmd = '{0}/Server.py --Ice.Config={0}/Server.config'.format(SRC_DIR)

        ic = Ice.initialize()
        self.addCleanup(ic.destroy)
        str_proxy = 'scone -t:tcp -h localhost -p 5001'
        proxy = ic.stringToProxy(str_proxy)
        self.scone = Semantic.SconeServicePrx.uncheckedCast(proxy)

    def tearDown(self):
        os.chdir(project_dir)
        self.server.terminate()
        wait_that(localhost, is_not(listen_port(5001)))

    def test_local_knowledge_ok(self):
        os.chdir('test/knowledge_ok')

        self.server = Popen(self.cmd.split(), stdout=PIPE)
        wait_that(localhost, listen_port(5001))
        self.addCleanup(self.server.terminate)

        self.assertEquals(
            self.scone.sconeRequest('(is-x-a-y? {Felix} {monkey})'), 'YES')

    def test_local_knowledge_error(self):
        os.chdir('test/knowledge_error')

        self.server = Popen(self.cmd.split(), stderr=PIPE)
        time.sleep(5)
        self.addCleanup(self.server.terminate)
        assert_that(localhost, is_not(listen_port(5001)))

        expected = "Error loading 'scone-knowledge.d/martin.lisp'"
        actual = self.server.stderr.read()
        print(actual)
        self.assert_(expected in actual)
