if [ "$1" -eq "master" ];
then
    echo "master"
elif [ "$1" -eq "startd" ];
then
    echo "startd"
elif [ "$1" -eq "schedd" ];
then
    echo "schedd"
elif [ "$1" -eq "collector" ];
then
    echo "collector"
elif [ "$1" -eq "wn" ];
then
    echo "wn"
fi