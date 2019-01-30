#!/usr/bin/env bash
rm -rf ./datasets/NPL/index/
./gavi.py index npl
rm -rf ./datasets/LISA/index/
./gavi.py index lisa