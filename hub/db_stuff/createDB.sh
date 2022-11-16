#!/bin/bash

DB_NAME=garden

sudo su postgres <<EOF
createdb  $DB_NAME;
EOF