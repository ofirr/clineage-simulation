#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -o    output base directory
    -s    seed

EOF
}

while getopts "s:o:h" OPTION
do
    case $OPTION in
        s) seed=$OPTARG ;;
        o) path_output_base=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$seed" ] || [ -z "$path_output_base" ]
then
    usage
    exit 1
fi

path_work="${path_output_base}/seed-${seed}"
path_scores="${path_work}/scores.${seed}.csv"

# remove the existing score because we're going to append
rm -rf ${path_score}

list=`find ${path_work} -name "final-score.csv"`

for file in $list
do
    echo ${file}
    cat $file >> ${path_scores}
done

echo
echo "${path_scores}"
echo "DONE."

