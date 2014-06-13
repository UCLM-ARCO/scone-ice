#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('SconeWrapper.ice')
import SconeWrapper


class client (Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        scone = SconeWrapper.SconeServicePrx.checkedCast(proxy)

        if not scone:
            raise RuntimeError('Invalid proxy')

        cad = "(is-util-way  {calle tinte})\n"
        str = scone.sconeRequest(cad)
        print(str)

        return 0


sys.exit(client().main(sys.argv))
