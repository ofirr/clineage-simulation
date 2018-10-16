#!/bin/bash

cd bin

#-->> TreeCmp

# download TreeCmp
wget https://eti.pg.edu.pl/treecmp/treecmp/bin/TreeCmp_v2.0-b11.zip

# uncompress
unzip TreeCmp_v2.0-b11.zip

# delete zip
rm -rf TreeCmp_v2.0-b11.zip

#-->> eSTGt

# get eSTGt
git clone https://github.com/hisplan/eSTGt.git

cd eSTGt

#fixme: for now, use dev
git checkout dev
