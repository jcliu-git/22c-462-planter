#!/bin/bash

echo Deleting Old Rows...
PGPASSWORD="postgres" psql -h db -p 5432 -U postgres -d garden -a -f deleteOldRows.sql

#TODO: set up a Cron Job
#@weekly <path to deleteOldRows.sh> 
#Delete once a week on Sunday at midnight
#How to add Cron to docker: https://www.airplane.dev/blog/docker-cron-jobs-how-to-run-cron-inside-containers
