#!/bin/sh

echo "worker"

pip install redis==2.10.5

pip list

python -u worker.py