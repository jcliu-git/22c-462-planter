FROM postgres:14.2-alpine

WORKDIR /scripts

ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB garden
# Do not specifiy POSTGRES_USER so defaulted to postgres

COPY . .
#Give permision
RUN chmod 777 *

# Docker run .sql or .sh scripts in initdb when postgres container is started 
# Note: scripts in initdb are only run if you start the container with an empty data directory, any pre-existing (mounted) data will be left untouched on container startup
COPY generate.sql /docker-entrypoint-initdb.d/
