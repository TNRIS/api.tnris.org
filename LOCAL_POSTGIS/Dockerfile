FROM mdillon/postgis

COPY z_api_init.sh /docker-entrypoint-initdb.d/z_api_init.sh
COPY z_init.sql /z_init.sql

EXPOSE 5432