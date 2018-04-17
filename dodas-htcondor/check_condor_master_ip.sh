#!/bin/bash

ZOOKEEPER_CONDOR_HOST=$(dodas_cache --wait-for true zookeeper CONDOR_HOST || echo "None")

if [ "$CONDOR_HOST" == "$ZOOKEEPER_CONDOR_HOST" ];
then
    exit 0 ;
else
    exit 1 ;
fi