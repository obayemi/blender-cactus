FROM postgres:17-bullseye

RUN apt-get update -y
# RUN apt-get install -y postgresql-14-wal2json

COPY ./init/ /docker-entrypoint-initdb.d/
# CMD [ "postgres", "-c", "wal_level=logical" ]
