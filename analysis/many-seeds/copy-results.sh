#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

	-n  template name without the prefix 'template-' (e.g. 8K-100-biallelic)

EOF
}

while getopts "n:h" OPTION
do
    case $OPTION in
		n) template_name=$OPTARG ;;
		h) usage; exit 1 ;;
		*) usage; exit 1 ;;
	esac
done

if [ -z "$template_name" ]
then
    usage
    exit 1
fi

path_dest="/home/chun/s/Jaeyoung/simul-outputs/${template_name}"

# create a destination directory
mkdir -p ${path_dest}

# generate mutation speed information
find template-${template_name}/ -name "*.json" | xargs -I {} \
    grep "mutationSpeed" {} -H > ${path_dest}/speed-info.txt

# copy results
cp --recursive seed-* ${path_dest}

# grant permission
chmod g+rwx ${path_dest} --recursive

echo "DONE."
