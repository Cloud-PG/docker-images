#!/bin/bash

if [[ -z "$1" ]]; then
    if [[ "$1" -eq "proxy" ]]; then

        cp /etc/xrootd/xrd_cache.conf  /etc/xrootd/xrd.conf
        if [[ "$2" -eq "-redirector_url" && -z "$3" ]]; then
            sed -i -e "s/rdtr_cache/$3/" /etc/xrootd/xrd.conf
        else if [[ "$2" -eq "-cmsd_redirector_port" && -z "$3" ]]; then
            sed -i -e "s/rdtr_port_cmsd/$3/" /etc/xrootd/xrd.conf
        else if [[ "$2" -eq "-xrd_redirector_port" && -z "$3" ]]; then
            sed -i -e "s/rdtr_port_xrd/$3/" /etc/xrootd/xrd.conf
        else
            echo "Invalid options"    
        fi

    else if [[ "$1" -eq "redirector" ]]; then
        cp /etc/xrootd/xrd_redirector.conf  /etc/xrootd/xrd.conf
    else 
        echo "no Valid options"
    fi

fi

exec xrootd -c /etc/xrootd/xrd.conf 
