#!/usr/bin/env bash

# python3.9 fisher.py

gunicorn --worker-class gevent \
    --bind 0.0.0.0:8088 \
    --workers 2 \
    --pid fisher.pid \
    --reload \
    --log-level debug \
    fisher:app