#!/bin/bash

sudo mkdir -p /var/tmp/archive
sudo chown ${USER} /var/tmp/archive

initdb hotstandby1

echo "port = 7000" >> hotstandby1/postgresql.conf
echo "wal_level = 'hot_standby'" >> hotstandby1/postgresql.conf
echo "archive_mode = on" >> hotstandby1/postgresql.conf
echo "archive_command = 'cp %p /var/tmp/archive/%f'" >> hotstandby1/postgresql.conf
echo "archive_timeout = 60" >> hotstandby1/postgresql.conf

pg_ctl -D hotstandby1 start -l hotstandby1.log

sleep 5

psql -p 7000 postgres -c "select pg_start_backup('backup')"
cp -pr hotstandby1/ hotstandby2
psql -p 7000 postgres -c "select pg_stop_backup()"
rm hotstandby2/postmaster.pid
rm -rf hotstandby2/pg_xlog/*
rm -rf hotstandby2/backup_label
mkdir -p hotstandby2/pg_xlog/archive_status

echo 'hot_standby = on' >> hotstandby2/postgresql.conf
echo 'port = 7001' >> hotstandby2/postgresql.conf

# echo "restore_command = 'cp -i /var/tmp/archive/%f %p'" >> hotstandby2/recovery.conf
## For testing pg_standby and a new -W parameter
echo "restore_command = '/usr/local/bin/pg_standby -W 300 -d -t /tmp/trigger /var/tmp/archive %f %p 2>&1 >> pg_standby.log'" >> hotstandby2/recovery.conf

echo "standby_mode = 'on'" >> hotstandby2/recovery.conf

pg_ctl -D hotstandby2 start -l hotstandby2.log
