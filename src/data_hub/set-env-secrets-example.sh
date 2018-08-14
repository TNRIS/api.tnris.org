#!/usr/bin/env bash
export DB_PASSWORD="<database password here>"
export AWS_ACCESS_KEY_ID='<data.tnris.org user aws access key>'
export AWS_SECRET_ACCESS_KEY='<data.tnris.org user aws secret key>'

# the following is only used within ETL scripts (specifically, migrate.py)
export TNRIS_REPO='<local path to cloned tnris.org website repo>'
