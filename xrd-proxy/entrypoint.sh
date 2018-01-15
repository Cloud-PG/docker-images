#!/bin/bash

sed -i -e "s/pss.origin*/pss.origin $1/" /etc/xrootd/xrd.conf

exec xrootd -c /etc/xrootd/xrd.conf 
