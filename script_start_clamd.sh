#!/bin/bash
/usr/sbin/clamd -c /etc/clamav/clamd.conf &
sleep 20s
python3 server.py
