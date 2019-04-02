#!/usr/bin/env bash

py.test --collect-only tests/ --not_publish_results True

read -rp $'\nMake sure desired capabilities is empty.\n\tVerify your tests were collected, press any key to continue or CTRL+C to abort.\n' key

## Remove cached files
find . -name '__pycache__' -type d -exec rm -r {} +
find . -name '*.pyc' -exec rm -f {} +
find . -name '*.pyo' -exec rm -f {} +
find . -name '*~' -exec rm -f {} +

## Write installed packages to requirements.txt
#pip freeze > requirements.txt

## Build wheel archive
pip wheel --wheel-dir wheelhouse -r requirements.txt

## Zip tests/, wheelhouse/, and requirements.txt into test_bundle.zip
zip -r test_bundle.zip tests/ wheelhouse/ requirements.txt testrail/
