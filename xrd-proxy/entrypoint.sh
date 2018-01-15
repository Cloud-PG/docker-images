#!/bin/bash

echo "pss.origin $1" > /etc/xrootd/xrd.conf

exec xrootd -b -c /etc/xrootd/xrd.conf
