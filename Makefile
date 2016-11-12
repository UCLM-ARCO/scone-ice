# -*- mode: makefile-gmake; coding: utf-8 -*-

DIRNAME = $(notdir $(shell 'pwd'))
DESTDIR?=~

all:

-PHONY: tests
tests:
	nosetests3 -s test/*_tests.py

install:
	install -d $(DESTDIR)/usr/bin/
	install -m 744 scone-wrapper $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/scone-wrapper/
	install -m 644 src/Server.py $(DESTDIR)/usr/lib/scone-wrapper/
	install -d $(DESTDIR)/etc/default
	install -m 644 src/Server.config $(DESTDIR)/etc/default/scone-wrapper.config


PHONY: clean
clean:
	find . \( -name "*.pyc" -o -name "*~" \) -print -delete
