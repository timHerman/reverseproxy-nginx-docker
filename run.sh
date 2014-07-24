#!/bin/bash
cd /docker/toolkit/nginxgenerator/
python refresh_configs.py -o /docker/data/global/router/reverseproxy
cd -
