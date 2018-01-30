#!/bin/bash

echo $@

if [[ -n "$1" ]]; then
    echo "HIIII"
    if [[ "$1" -eq "proxy" ]]; then
    echo "HIIII"

        cp /etc/xrootd/xrd_cache.conf  /etc/xrootd/xrd.conf
        if [[ "$2" -eq "-redirector_url" && -n "$3" ]]; then
    echo "HIIII"
            sed -i -e "s/rdtr_cache/$3/" /etc/xrootd/xrd.conf
        fi
        if [[ "$4" -eq "-cmsd_redirector_port" && -n "$5" ]]; then
            sed -i -e "s/rdtr_port_cmsd/$5/" /etc/xrootd/xrd.conf
        fi
        if [[ "$6" -eq "-xrd_redirector_port" && -n "$7" ]]; then
            sed -i -e "s/rdtr_port_xrd/$7/" /etc/xrootd/xrd.conf
        fi

    elif [[ "$1" -eq "redirector" ]]; then
        cp /etc/xrootd/xrd_redirector.conf  /etc/xrootd/xrd.conf
    else 
        echo "no Valid options"
    fi

fi

xrootd -b -c /etc/xrootd/xrd.conf -l /var/log/xrootd/proxyXrd.log 
exec cmsd -c /etc/xrootd/xrd.conf
