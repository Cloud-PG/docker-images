#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import logging
import subprocess
import sys

from exceptions import *

FORMAT = '%(asctime)s %(message)s'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-P', '--proxy', help='XrootD proxy file cache mode', action="store_true")
group.add_argument('-R', '--redirector', help='XrootD cache redirector mode', action="store_true")
group.add_argument('--config', help='XrootD config file path')

parser.add_argument('--cache_host', help='cache host address', default='0.0.0.0')
parser.add_argument('--redir_host', help='cache redirector host address', default='0.0.0.0' )
parser.add_argument('--origin_host', help='origin server/redirector host address', default='0.0.0.0')

parser.add_argument('--cache_xrd_port', help='cache host port for xrootd daemon', default='1094')
parser.add_argument('--redir_xrd_port', help='cache redirector host port for xrootd daemon', default='1094' )
parser.add_argument('--origin_xrd_port', help='origin server/redirector host port for xrootd daemon', default='1094')

parser.add_argument('--cache_cmsd_port', help='cache host address port for cmsd daemon', default='1213')
parser.add_argument('--redir_cmsd_port', help='cache redirector host port for cmsd daemon', default='1213' )

def configure_proxy(server):
    pass


def configure_redirector(server):
    pass
    

if __name__ == "__main__":

    args = parser.parse_args()
    logging.info("Starting server: \
                 \n proxy: %s \
                 \n redirector: %s \
                 \n config: %s \
                 \n cache host: %s \
                 \n redirector host: %s \
                 \n origin host: %s \
                 \n cache xrootd port: %s \
                 \n redirector xrootd port: %s \
                 \n origin xrootd port: %s \
                 \n cache cmsd port: %s \
                 \n redirector cmsd port: %s \
                 " % (args.proxy, args.redirector, args.config, 
                      args.cache_host, args.redir_host, args.origin_host,
                      args.cache_xrd_port, args.redir_xrd_port, args.origin_xrd_port,
                      args.cache_cmsd_port, args.redir_cmsd_port))

    if args.config:


        subprocess.check_call(["cmsd", "-b", "-l", "/var/log/xrootd/xrd.log", "-c", args.config])
        subprocess.check_call(["xrootd", "-c", args.config])

    else:
        server = {'cache_host':      args.cache_host,
                'redir_host':        args.redir_host,
                'origin_host':       args.origin_host,
                'cache_xrd_port':    args.cache_xrd_port,
                'redir_xrd_port':    args.redir_xrd_port,
                'origin_xrd_port':   args.origin_xrd_port,
                'cache_cmsd_port':   '1213',
                'redir_cmsd_port':   '1213',
                }

        if args.proxy:
            configure_proxy(server)
        elif args.redirector:
            configure_redirector(server)