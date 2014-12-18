# -*- mode: makefile-gmake; coding: utf-8 -*-

SHELL   = /bin/bash
DIRNAME = $(notdir $(shell 'pwd'))

all:

deploy: ICEPATCH2_DIR = /var/lib/icegrid/icepatch2.dir
deploy: all
	rm -rf $(ICEPATCH2_DIR)/$(DIRNAME)
	cp -r $$(pwd) $(ICEPATCH2_DIR)
	icepatch2calc $(ICEPATCH2_DIR)

install:
	true


PHONY: clean
clean:
	find . \( -name "*.pyc" -o -name "*~" \) -print -delete
