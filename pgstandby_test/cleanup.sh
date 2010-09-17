#!/bin/bash
pg_ctl -D hotstandby1 stop -m f
pg_ctl -D hotstandby2 stop -m f

rm -rf hotstandby1 hotstandby2 hotstandby1.log hotstandby2.log
