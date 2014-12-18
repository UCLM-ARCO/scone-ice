# -*- mode: makefile-gmake; coding: utf-8 -*-

SHELL   = /bin/bash
DIRNAME = $(notdir $(shell 'pwd'))
DESTDIR?=~

all:

deploy: ICEPATCH2_DIR = /var/lib/icegrid/icepatch2.dir
deploy: all
	rm -rf $(ICEPATCH2_DIR)/$(DIRNAME)
	cp -r $$(pwd) $(ICEPATCH2_DIR)
	icepatch2calc $(ICEPATCH2_DIR)

install:
	install -d $(DESTDIR)/usr/bin/
	install -m 644 src/Server.py $(DESTDIR)/usr/bin/scone-wrapper




PHONY: clean
clean:
	find . \( -name "*.pyc" -o -name "*~" \) -print -delete
