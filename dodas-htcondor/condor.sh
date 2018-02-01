#!/bin/bash

if [ "$1" == "master" ];
then
    echo "==> Compile configuration file for master node with env vars"
    export CONDOR_DAEMON_LIST="COLLECTOR, MASTER, NEGOTIATOR"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master -f
elif [ "$1" == "wn" ];
then
    echo "==> Compile configuration file for worker node with env vars"
    export CONDOR_DAEMON_LIST="MASTER, STARTD"
    export CCB_ADDRESS_STRING="CCB_ADDRESS = $CONDOR_FULL_HOSTNAME"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master -f
    echo "==> Start service"
elif [ "$1" == "schedd" ];
then
    echo "==> Compile configuration file for sheduler node with env vars"
    export CONDOR_DAEMON_LIST="MASTER, SCHEDD"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master
    echo "==> Start sshd on port $CONDOR_SCHEDD_SSH_PORT"
    exec /usr/sbin/sshd -E /var/log/sshd.log -g 30 -p $CONDOR_SCHEDD_SSH_PORT -D
elif [ "$1" == "all" ];
then
    echo "==> Compile configuration file for sheduler node with env vars"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master -f
    echo "==> Start sshd on port $CONDOR_SCHEDD_SSH_PORT"
    exec /usr/sbin/sshd -E /var/log/sshd.log -g 30 -p $CONDOR_SCHEDD_SSH_PORT -D
else
    echo "[ERROR]==> You have to supply a role, like: 'master', 'wn', 'schedd' or 'all'..."
    exit 1
fi