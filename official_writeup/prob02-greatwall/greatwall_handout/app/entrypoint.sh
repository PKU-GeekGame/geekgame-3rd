#!/bin/bash
set -ex

node /app/prepare_flag.mjs

exec supervisord -c /app/supervisord.conf
