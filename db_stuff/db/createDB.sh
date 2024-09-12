#!/bin/bash

DB_NAME=garden
PASSWORD=postgres

sudo su postgres <<EOF
createdb  $DB_NAME;
psql -c "ALTER USER postgres PASSWORD '$PASSWORD';
EOF
