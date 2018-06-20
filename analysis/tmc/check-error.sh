#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -s    seed

EOF
}

while getopts "s:h" OPTION
do
    case $OPTION in
        s) seed=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$seed" ]
then
    usage
    exit 1
fi

if [ "$seed" == "all" ]
then
    find . -name "*.stderr" ! -size 0
else
    find seed-${seed} -name "*.stderr" ! -size 0
fi

