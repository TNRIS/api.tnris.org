#! /bin/bash

docker build . -t txgio/api-local-postgis
docker run -d -p 9000:5432 txgio/api-local-postgis