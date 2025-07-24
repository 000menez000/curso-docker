#!/bin/sh

pip install \
    bottle==0.12.13 \
    psycopg2-binary==2.9.8 \
    redis==2.10.5

python -u sender.py