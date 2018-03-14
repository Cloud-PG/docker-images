#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import exceptions
import logging
import os.path
import subprocess
import sys
import time

from flask import Flask


APP = Flask(__name__)
FORMAT = '%(asctime)s %(message)s'
DEFAULT_CONFIG = '/etc/xrootd/xrd_cache.conf'

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
    """Make configuration file for proxy setup
    
    Arguments:
        server = {'cache_host':      args.cache_host,
                'redir_host':        args.redir_host,
                'origin_host':       args.origin_host,
                'cache_xrd_port':    args.cache_xrd_port,
                'redir_xrd_port':    args.redir_xrd_port,
                'origin_xrd_port':   args.origin_xrd_port,
                'cache_cmsd_port':   '1213',
                'redir_cmsd_port':   '1213',
                }
    """

    with open(DEFAULT_CONFIG, 'r') as file:
        filedata = file.read()

        logging.info("Creating config file..")
        # Replace the target string
        filedata = filedata.replace('rdtr_cache',server["redir_host"])
        filedata = filedata.replace('rdtr_port_xrd',server["redir_xrd_port"])
        filedata = filedata.replace('rdtr_port_cmsd',server["redir_cmsd_port"])
        filedata = filedata.replace('rdtr_global_port',server["origin_xrd_port"])
        filedata = filedata.replace('rdtr_global',server["origin_host"])
        
    with open(DEFAULT_CONFIG, 'w') as file:
        file.write(filedata)

def configure_redirector(server):
    """Make configuration file for proxy setup
    
    Arguments:
        server = {'cache_host':      args.cache_host,19:15,060 Return code cmsd_check: 0
                'redir_host':        args.redir_host,
                'origin_host':       args.origin_host,
                'cache_xrd_port':    args.cache_xrd_port,
                'redir_xrd_port':    args.redir_xrd_port,
                'origin_xrd_port':   args.origin_xrd_port,
                'cache_cmsd_port':   '1213',
                'redir_cmsd_port':   '1213',
                }
    """

    DEFAULT_CONFIG = '/etc/xrootd/xrd_redirector.conf'

    with open(DEFAULT_CONFIG, 'r') as file:
        filedata = file.read()

        logging.info("Creating config file..")
        # Replace the target string
        filedata = filedata.replace('rdtr_cache',server["redir_host"])
        filedata = filedata.replace('rdtr_port_xrd',server["redir_xrd_port"])
        filedata = filedata.replace('rdtr_port_cmsd',server["redir_cmsd_port"])
        filedata = filedata.replace('rdtr_global_port',server["origin_xrd_port"])
        filedata = filedata.replace('rdtr_global',server["origin_host"])
        
    with open(DEFAULT_CONFIG, 'w') as file:
        file.write(filedata)
    
@APP.route('/check_health', methods=['GET'])
def check_health():
    """Check health of xrootd daemons
    
    Arguments:
        xrd_proc {subprocess.Popen} -- xrootd daemon process
        cmsd_proc {subprocess.Popen} -- cmsd daemon process
    
    Returns:
        int -- 0 if healthy, 1 if down
    """

    xrd_check = APP.xrd_proc.poll()
    cmsd_check = APP.cmsd_proc.poll()

    logging.debug("Return code xrd_check: %s", xrd_check)
    logging.debug("Return code cmsd_check: %s", cmsd_check)

    if xrd_check is not None or cmsd_check is not None:
        logging.error("ERROR: one deamon down! Take a look to the logs:")
        if xrd_check:
            log_path = '/var/log/xrootd/xrd.log'
            if os.path.exists(log_path):
                with open(log_path, 'r') as fin:
                    logging.debug('%s: \n %s' % (log_path,fin.read()))
        if cmsd_check:
            log_path = '/var/log/xrootd/cmsd.log'
            if os.path.exists(log_path):
                with open(log_path, 'r') as fin:
                    logging.debug('%s: \n %s' % (log_path,fin.read()))
        return "1"
    else:
        logging.info("It's all good!")
        return "0"


if __name__ == "__main__":

    args = parser.parse_args()

    logging.info("Intalling certificates...")
    try:
        subprocess.check_output("/opt/xrd_proxy/install_ca.sh", stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as ex:
        logging.warn("WARNING: failed to install CAs: \n %s" % ex.output)

    logging.info("Intalling CAs... - DONE")

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
        if args.config == 'default':
            args.config = '/etc/xrootd/xrd_cache.conf'
        logging.info("Using configuration file: %s" % args.config)

        cmsd_command = "sudo -u xrootd /usr/bin/cmsd -l /var/log/xrootd/cmsd.log -c" + args.config
        logging.debug("Starting cmsd daemon: \n %s", cmsd_command)
        try:
            cmsd_proc = subprocess.Popen(cmsd_command, shell=True)
        except ValueError as ex:
            logging.error("ERROR: when launching cmsd daemon: %s \n %s" % (ex.args, ex.message))
            sys.exit(1)
        logging.debug("cmsd daemon started!")

        xrd_command = "sudo -u xrootd /usr/bin/xrootd -l /var/log/xrootd/xrd.log -c" + args.config
        logging.debug("Starting xrootd daemon: \n %s", xrd_command)
        try:
            xrd_proc = subprocess.Popen(xrd_command, shell=True)
        except ValueError as ex:
            logging.error("ERROR: when launching xrootd daemon: %s \n %s" % (ex.args, ex.message))
            sys.exit(1)
        logging.debug("xrootd daemon started!")

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
            try:
                configure_proxy(server)
            except:
                logging.exception("Unknown exception")
        elif args.redirector:
            try:
                configure_redirector(server)
            except:
                logging.exception("Unknown exception")
        
        logging.info("Using configuration file: %s" % DEFAULT_CONFIG)

        cmsd_command = "sudo -u xrootd /usr/bin/cmsd -l /var/log/xrootd/cmsd.log -c" + DEFAULT_CONFIG
        logging.debug("Starting cmsd daemon: \n %s", cmsd_command)
        try:
            cmsd_proc = subprocess.Popen(cmsd_command, shell=True)
        except ValueError as ex:
            logging.error("ERROR: when launching cmsd daemon: %s \n %s" % (ex.args, ex.message))
            sys.exit(1)
        logging.debug("cmsd daemon started!")

        xrd_command = "sudo -u xrootd /usr/bin/xrootd -l /var/log/xrootd/xrd.log -c" + DEFAULT_CONFIG
        logging.debug("Starting xrootd daemon: \n %s", xrd_command)
        try:
            xrd_proc = subprocess.Popen(xrd_command, shell=True)
        except ValueError as ex:
            logging.error("ERROR: when launching xrootd daemon: %s \n %s" % (ex.args, ex.message))
            sys.exit(1)
        logging.debug("xrootd daemon started!")

    APP.cmsd_proc = cmsd_proc
    APP.xrd_proc = xrd_proc
    APP.run(host="0.0.0.0", port=80)