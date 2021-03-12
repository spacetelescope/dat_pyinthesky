#!/usr/bin/env bash

set -e

mkdir -p webbpsf-data
FILE_URL='http://www.stsci.edu/~mperrin/software/webbpsf/webbpsf-data-0.9.0.tar.gz'
FILE_URL='https://www.stsci.edu/~mperrin/software/webbpsf/webbpsf-data-0.9.0.tar.gz'
filename=$(basename $FILE_URL)
filepath="webbpsf-data/$filename"

if [ ! -f "$filepath" ]; then
    curl -v $FILE_URL -o $filepath
    cd webbpsf-data
    tar -xf $filename
    cd -
fi


if [ ! -f "grp" ]; then

    curl -v https://ssb.stsci.edu/trds/tarfiles/synphot1.tar.gz -o synphot1.tar.gz | tar xvz
    tar -xzf synphot1.tar.gz

    curl -v https://ssb.stsci.edu/trds/tarfiles/synphot2.tar.gz -o synphot2.tar.gz | tar xvz
    tar -xzf synphot2.tar.gz

    curl -v https://ssb.stsci.edu/trds/tarfiles/synphot5.tar.gz -o synphot5.tar.gz | tar xvz
    tar -xzf synphot5.tar.gz

    curl -v https://ssb.stsci.edu/trds/tarfiles/synphot6.tar.gz -o synphot6.tar.gz | tar xvz
    tar -xzf synphot6.tar.gz

fi

exit 0
