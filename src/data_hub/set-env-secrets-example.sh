#!/usr/bin/env bash
export DB_PASSWORD="<database password here>"
echo DB_PASSWORD $DB_PASSWORD
export DB_NAME="<database name>"
echo DB_NAME $DB_NAME
export DB_USER="<database user>"
echo DB_USER $DB_USER
export DB_HOST="<database host address>"
echo DB_HOST $DB_HOST
export DB_PORT="<database port>"
echo DB_PORT $DB_PORT

export SEO_TOKEN="<prerender.io account token>"
echo SEO_TOKEN $SEO_TOKEN

# CONTACT APP ENV VARIABLES
export RECAPTCHA_SECRET="<recaptcha secret>"
echo RECAPTCHA_SECRET $RECAPTCHA_SECRET
export MAIL_DEFAULT_FROM="<twdb domained tnris support email address>"
echo MAIL_DEFAULT_FROM $MAIL_DEFAULT_FROM
export MAIL_DEFAULT_TO="<supportsystem email>"
echo MAIL_DEFAULT_TO $MAIL_DEFAULT_TO
export AWS_SES_ACCESS_KEY="<ses-smtp-user aws iam access key>"
echo AWS_SES_ACCESS_KEY $AWS_SES_ACCESS_KEY
export AWS_SES_SECRET_KEY="<ses-smtp-user aws iam secret key>"
echo AWS_SES_SECRET_KEY $AWS_SES_SECRET_KEY
export S3_UPLOAD_BUCKET="<s3 bucket for contact uploads>"
echo S3_UPLOAD_BUCKET $S3_UPLOAD_BUCKET
export S3_UPLOAD_SECRET="<s3 bucket secret>"
echo S3_UPLOAD_SECRET $S3_UPLOAD_SECRET
export S3_UPLOAD_KEY="<s3 bucket key>"
echo S3_UPLOAD_KEY $S3_UPLOAD_KEY

export MAPSERVER_DB_NAME='<mapserver database name>'
echo MAPSERVER_DB_NAME $MAPSERVER_DB_NAME
export MAPSERVER_DB_USER='<mapserver database user>'
echo MAPSERVER_DB_USER $MAPSERVER_DB_USER
export MAPSERVER_DB_PASSWORD='<mapserver database password>'
echo MAPSERVER_DB_PASSWORD $MAPSERVER_DB_PASSWORD

export DATAHUB_MASTER_CLOUDFRONT=$(aws cloudformation describe-stack-resource --stack-name datahub-master --logical-resource-id MasterCloudfront --query StackResourceDetail.PhysicalResourceId --output text)
echo DATAHUB_MASTER_CLOUDFRONT $DATAHUB_MASTER_CLOUDFRONT

echo "environment variables set!!!"

# the following is only used within ETL scripts (specifically, migrate.py)
export TNRIS_REPO='<local path to cloned tnris.org website repo>'
