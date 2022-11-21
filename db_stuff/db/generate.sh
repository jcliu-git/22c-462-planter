#!/bin/bash

psql -U postgres -d garden -a -f generate.sql
