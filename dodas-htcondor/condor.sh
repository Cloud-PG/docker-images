#!/bin/bash

if [ "$1" == "master" ];
then
    j2 /usr/local/sbin/dodas/htc_config/condor_config.template /usr/local/sbin/dodas/htc_config/master_condor_config.json > /etc/condor/condor_config
elif [ "$1" == "wn" ];
then
    j2 /usr/local/sbin/dodas/htc_config/condor_config.template /usr/local/sbin/dodas/htc_config/wn_condor_config.json > /etc/condor/condor_config
elif [ "$1" == "schedd" ];
then
    j2 /usr/local/sbin/dodas/htc_config/condor_config.template /usr/local/sbin/dodas/htc_config/schedd_condor_config.json > /etc/condor/condor_config
    exec /usr/sbin/sshd -D
fi