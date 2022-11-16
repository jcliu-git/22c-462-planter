#!/bin/bash

while getopts h:u:d: flag
do
    case "${flag}" in
        h) remotehost=${OPTARG};;
        u) remoteuser=${OPTARG};;
        d) dbname=${OPTARG};;
    esac
done

# dump a local database and restore to a specified remote machine
pg_dump -C -h localhost -U postgres garden | psql -h $remotehost -U $remoteuser $dbname