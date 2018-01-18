#!/bin/bash

if [ "$1" == "master" ];
then
    echo "==> Copy configuration file for master node"
    j2 /opt/dodas/htc_config/condor_config.template /opt/dodas/htc_config/master_condor_config.json > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master
    echo "==> Start service"
    python -m SimpleHTTPServer 5000
elif [ "$1" == "wn" ];
then
    echo "==> Copy configuration file for worker node"
    j2 /opt/dodas/htc_config/condor_config.template /opt/dodas/htc_config/wn_condor_config.json > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master
    echo "==> Start service"
    RAND_PORT=$(python -c "import time; print(int(time.time()) % 1000)")
    python -m SimpleHTTPServer $RAND_PORT
elif [ "$1" == "schedd" ];
then
    echo "==> Copy configuration file for sheduler node"
    j2 /opt/dodas/htc_config/condor_config.template /opt/dodas/htc_config/schedd_condor_config.json > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master
    echo "==> Start sshd"
    exec /usr/sbin/sshd -E /var/log/sshd.log -g 30 -p $2 -D
fi