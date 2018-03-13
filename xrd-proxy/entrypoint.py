#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import exceptions
import logging
import subprocess
import sys
import time


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
    logging.warn("Feature not implemented yet. Please use --config to pass a valid configuration file")


def configure_redirector(server):
    logging.warn("Feature not implemented yet. Please use --config to pass a valid configuration file")
    

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
        logging.info("Using configuration file: %s" % args.config)

        #cmsd_command = "/usr/bin/cmsd -b -l /var/log/xrootd/cmsd.log -c "+args.config
        cmsd_command = "/usr/bin/cmsd -l /var/log/xrootd/cmsd.log -c" + args.config

        logging.debug("Starting cmsd daemon: \n %s", cmsd_command)
        try:
            cmsd_proc = subprocess.Popen(cmsd_command, shell=True)
        except ValueError as ex:
            logging.error("ERROR: when launching cmsd daemon: %s \n %s" % (ex.args, ex.message))
            sys.exit(1)
        logging.debug("cmsd daemon started!")

        xrd_command = "/usr/bin/xrootd -l /var/log/xrootd/xrd.log -c" + args.config

        logging.debug("Starting xrootd daemon: \n %s", xrd_command)
        try:
            xrd_proc = subprocess.Popen(cmsd_command, shell=True)
        except ValueError as ex:
            logging.error("ERROR: when launching xrootd daemon: %s \n %s" % (ex.args, ex.message))
            sys.exit(1)
        logging.debug("xrootd daemon started!")

        services_running = True
        while services_running:
            xrd_check = xrd_proc.poll()
            cmsd_check = cmsd_proc.poll()
            
            if xrd_check or cmsd_check:
                logging.error("ERROR: one deamon down! Take a look to the logs.")
                sys.exit(1)
            else:
                logging.info("All services running")
            time.sleep(1)

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
