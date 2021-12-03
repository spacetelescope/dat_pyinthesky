#!/usr/bin/env bash

set -e

export LANG=C.UTF-8
export LC_ALL=C.UTF-8
#conda install python=3.7.11
conda install python=3.8.10
apt-get update
apt-get install -y git make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl \
    llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libfreetype6-dev

git clone https://github.com/spacetelescope/nbcollection nbcollection
cd nbcollection
pip install -U pip setuptools
pip install -r ci_requirements.txt
python setup.py install
#export CRDS_SERVER_URL=https://jwst-crds.stsci.edu
#export CRDS_PATH=$HOME/crds_cache
cd -
