FROM postgres:14.2-alpine

WORKDIR /db

ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB garden
# Do not specifiy POSTGRES_USER so defaulted to postgres

#Install Python
RUN apt-get update && apt-get install -y python

#Copying all files into container 
COPY . .

#Give permision 
RUN chmod 777 *.sh

EXPOSE 5432

# Docker run .sql or .sh scripts in initdb when postgres container is started 
# Note: scripts in initdb are only run if you start the container with an empty data directory, any pre-existing (mounted) data will be left untouched on container startup
COPY generate.sql /docker-entrypoint-initdb.d/
