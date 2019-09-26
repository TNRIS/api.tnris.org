#!/usr/bin/env bash
export DB_PASSWORD="<database password here>"
export DB_NAME="<database name>"
export DB_USER="<database user>"
export DB_HOST="<database host address>"
export DB_PORT="<database port>"

export SEO_TOKEN="<prerender.io account token>"

# CONTACT APP ENV VARIABLES
export RECAPTCHA_SECRET="<recaptcha secret>"
export MAIL_DEFAULT_FROM="<twdb domained tnris support email address>"
export MAIL_DEFAULT_TO="<supportsystem email>"
export AWS_SES_ACCESS_KEY="<ses-smtp-user aws iam access key>"
export AWS_SES_SECRET_KEY="<ses-smtp-user aws iam secret key>"

echo "environment variables set!!!"

# the following is only used within ETL scripts (specifically, migrate.py)
export TNRIS_REPO='<local path to cloned tnris.org website repo>'
