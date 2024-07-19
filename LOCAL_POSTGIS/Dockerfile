FROM postgis/postgis:13-3.4

COPY ./z_api_init.sh /docker-entrypoint-initdb.d/11_z_api_init.sh
COPY ./z_init.sql /z_init.sql

RUN chmod +x /docker-entrypoint-initdb.d/11_z_api_init.sh

## NEVER USE THIS IN PRODUCTION OR SECURITY SENSITIVE SITUATION!!!!
ENV POSTGRES_HOST_AUTH_METHOD=trust

EXPOSE 5432