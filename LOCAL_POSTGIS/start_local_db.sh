#! /bin/bash

docker build . -t tnris/api-local-postgis
docker run -d -p 9000:5432 tnris/api-local-postgis