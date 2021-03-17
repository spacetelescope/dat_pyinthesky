#!/usr/bin/env bash

source bin/activate
pip install astropy-helpers==2.0.11
pip install git+https://github.com/spacetelescope/jdaviz.git@625acca8562249c2f4d9041c566c1820a4d480b2#egg=jdaviz
