#!/bin/bash  
export DATABASE_URL=$(heroku config:get DATABASE_URL -a control-module-database)
flask --app front-end run