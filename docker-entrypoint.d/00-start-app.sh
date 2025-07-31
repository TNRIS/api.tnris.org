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
export STRATMAP_EMAIL=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.STRATMAP_EMAIL'`

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

export FISERV_ACCOUNT_ID=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_PROD_ACCOUNT_ID'`
export FISERV_ACCOUNT_NAME=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_ACCOUNT_NAME'`
export FISERV_GATEWAY=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_GATEWAY'`
export FISERV_MERCHANT_ID=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_MERCHANT_ID'`
export FISERV_MERCHANT_NAME=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_MERCHANT_NAME'`
export FISERV_DEV_AUTH_USER=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_DEV_AUTH_USER'`
export FISERV_AUTH_CODE=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_PROD_AUTH_CODE'`
export FISERV_API_BASIC_AUTH_PWD=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_PROD_API_BASIC_AUTH_PWD'`
export FISERV_API_BASIC_AUTH_USERNAME=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_API_BASIC_AUTH_USERNAME'`
export FISERV_COMPANY_CODE=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_COMPANY_CODE'`
export FISERV_CUSTOMER_ID=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_CUSTOMER_ID'`
export FISERV_USER_ID=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_USER_ID'`
export FISERV_SERVICE_CODE=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FISERV_SERVICE_CODE'`

export API_URL=stagingapi.tnris.org
export FDMS_URL=https://securecheckout-uat.cdc.nicusa.com/ccprest/api/v1/TX/
export FISERV_URL=https://snappaydirectapi-cert.fiserv.com/api/interop/
export FISERV_URL_V2=https://snappaydirectapi-cert.fiserv.com/api/interop/v2/
export FISERV_URL_V3=https://snappaydirectapi-cert.fiserv.com/api/interop/v3/
export FISERV_HPP_PAGE=https://snappaydirect-cert.fiserv.com/interop/HostedPaymentPage/

export CCP_URL=https://securecheckout.cdc.nicusa.com/ccprest/api/v1/TX/

export FKEY1=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.FKEY1'`
export ACCESS_PEPPER=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.ACCESS_PEPPER'`
export BCC_EMAIL_1=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.BCC_EMAIL_1'`

export ARCGIS_USERNAME=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.ARCGIS_USERNAME'`
export ARCGIS_PASSWORD=`/envs/data_hub/bin/aws secretsmanager get-secret-value --secret-id api-tnris-org --query SecretString --output text | jq -cr '.ARCGIS_PASSWORD'`

export IS_LIVE=true
export IS_DEBUG=false

export DATAHUB_MASTER_CLOUDFRONT=`/envs/data_hub/bin/aws cloudformation describe-stack-resource --stack-name datahub-master --logical-resource-id MasterCloudfront --query StackResourceDetail.PhysicalResourceId --output text`

echo "environment variables set!!!"

eval /src/data_hub/manage.py collectstatic --noinput "$@"
eval /usr/bin/supervisord "$@"
