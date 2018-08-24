#!/usr/bin/env bash
export DB_PASSWORD="<database password here>"
export DB_NAME="<database name>"
export DB_USER="<database user>"
export DB_HOST='<database host address>'
export DB_PORT='<database port>'

# the following is only used within ETL scripts (specifically, migrate.py)
export TNRIS_REPO='<local path to cloned tnris.org website repo>'
