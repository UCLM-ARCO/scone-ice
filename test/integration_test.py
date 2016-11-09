#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

from unittest import TestCase
from subprocess import Popen, PIPE
from hamcrest import is_not

from commodity.testing import assert_that, wait_that
from commodity.net import localhost, listen_port

import Ice

slice_dir = "/usr/share/slice"
Ice.loadSlice("-I{0} {0}/dharma/dharma.ice --all".format(slice_dir))
import Semantic


class SconeWrapperTest(TestCase):
    def setUp(self):
        assert_that(localhost, is_not(listen_port(5001)))
        self.server = Popen(['src/Server.py', '--Ice.Config=src/Server.config'],
                            stdout=PIPE)
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
            self.assertEquals(e.reason, '{elephant} cannot be a {bird}.')
