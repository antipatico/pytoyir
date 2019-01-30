#!/usr/bin/env bash
rm -rf ./datasets/NPL/index/
./pytoyir.py index npl
rm -rf ./datasets/LISA/index/
./pytoyir.py index lisa
