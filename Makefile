SHELL := bash -euo pipefail -c
MAKEFLAGS += --warn-undefined-variables

THIS_MAKEFILE = $(abspath $(firstword $(MAKEFILE_LIST)))
SRC_ROOT := $(shell dirname ${THIS_MAKEFILE})
# MAKE_LIB_DIR := ${SRC_ROOT}/.makefiles
# include ${MAKE_LIB_DIR}/Makefile.base.mk

deploy:
	# workon slack-devel
	zappa update vortex
