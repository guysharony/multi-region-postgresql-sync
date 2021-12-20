FROM debezium/postgres AS base

COPY ./src/destination.sql /docker-entrypoint-initdb.d/

COPY ./src/postgresql.conf /etc/postgresql/postgresql.conf
# COPY ./src/pg_hba.conf /etc/postgresql/pg_hba.conf

RUN chmod a+r /docker-entrypoint-initdb.d/*