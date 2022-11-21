#!/bin/bash

PGPASSWORD="postgres" psql -h db -p 5432 -U postgres -d garden -a -f test.sql