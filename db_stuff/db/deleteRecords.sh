#!/bin/bash
while getopts t: flag
do
    case "${flag}" in
        t) tablename=${OPTARG};;
    esac
done

psql -U postgres -d garden -v table_name=$table_name -c "TRUNCATE table $tablename RESTART IDENTITY;"
