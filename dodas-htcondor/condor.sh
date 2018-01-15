#!bin/bash

if [ "$1" == "master" ];
then
    echo "master"
elif [ "$1" == "startd" ];
then
    echo "startd"
elif [ "$1" == "schedd" ];
then
    echo "schedd"
elif [ "$1" == "collector" ];
then
    echo "collector"
elif [ "$1" == "wn" ];
then
    echo "wn"
fi