# -*- mode: makefile-gmake; coding: utf-8 -*-

SHELL   = /bin/bash
DIRNAME = $(notdir $(shell 'pwd'))
DESTDIR?=~

all:

-PHONY: tests
tests:
	nosetests3 -s test

install:
	install -d $(DESTDIR)/usr/bin/
	install -m 644 src/Server.py $(DESTDIR)/usr/bin/scone-wrapper
	install -d $(DESTDIR)/etc
	install -m 644 src/scone-wrapper.conf $(DESTDIR)/etc/


PHONY: clean
clean:
	find . \( -name "*.pyc" -o -name "*~" \) -print -delete
