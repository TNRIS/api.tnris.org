# Dockerized PostGIS
This directory contains a Dockerfile to build an image of postgis for use in local development.
The helper script, start_local_db.sh, will build the image and run it as a container, forwarding the container port 5432 to your localhost:9000.
Note that you must run start_local_db.sh from this directory for it to build the image properly.

## Docker Image Resources
There are two scripts in this directory which are copied into the Dockerfile to setup a user and database in the postgis container.
These scripts are:

1.) z_api_init.sh
2.) z_init.sql

z_api_init.sh runs the z_init.sql file over psql inside the container so that the user, password, and database are all setup at startup.
The script creates user "localapi" with password "localapi" and assigns this user as the owner of a new database, "localapi".
Since `python manage.py migrate` requires superuser privileges, the user localapi is also made a superuser. This is not ideal in a production setting,
but it works just fine for local development.