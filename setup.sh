#!/usr/bin/env bash
set -e
./scripts/clear-all.sh
./scripts/setup-venv.sh
source ./venv/bin/activate
./scripts/npl-splitter.py
./scripts/lisa-splitter.py
./scripts/index-all.sh
./scripts/npl-prepare-benchmark.py
./scripts/lisa-prepare-benchmark.py
deactivate
