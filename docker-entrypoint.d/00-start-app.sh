#!/bin/sh

export SECRET_KEY=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.SECRET_KEY'`
export DB_NAME=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.DB_NAME'`
export DB_USER=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.DB_USER'`
export DB_PASSWORD=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.DB_PASSWORD'`
export DB_HOST=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.DB_HOST'`
export DB_PORT=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.DB_PORT'`

export SEO_TOKEN=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.SEO_TOKEN'`

export RECAPTCHA_SECRET=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.RECAPTCHA_SECRET'`
export MAIL_DEFAULT_FROM=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.MAIL_DEFAULT_FROM'`
export MAIL_DEFAULT_TO=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.MAIL_DEFAULT_TO'`
export AWS_SES_ACCESS_KEY=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.AWS_SES_ACCESS_KEY'`
export AWS_SES_SECRET_KEY=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.AWS_SES_SECRET_KEY'`
export S3_UPLOAD_BUCKET=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.S3_UPLOAD_BUCKET'`
export S3_UPLOAD_SECRET=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.S3_UPLOAD_SECRET'`
export S3_UPLOAD_KEY=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.S3_UPLOAD_KEY'`

export CCP_MERCHANT_CODE=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.CCP_MERCHANT_CODE'`
export CCP_MERCHANT_KEY=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.CCP_MERCHANT_KEY'`
export CCP_SERVICE_CODE=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.CCP_SERVICE_CODE'`
export CCP_API_KEY=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.CCP_API_KEY'`
export CCP_ACCESS_CODE=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.CCP_ACCESS_CODE'`

export FKEY1=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FKEY1'`
export ACCESS_PEPPER=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.ACCESS_PEPPER'`

export IS_LIVE=true
export DATAHUB_MASTER_CLOUDFRONT=`/envs/data_hub/bin/aws cloudformation describe-stack-resource --stack-name datahub-master --logical-resource-id MasterCloudfront --query StackResourceDetail.PhysicalResourceId --output text`

echo "environment variables set!!!"

eval /src/data_hub/manage.py collectstatic --noinput "$@"
eval /usr/bin/supervisord "$@"
