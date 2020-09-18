#!/bin/sh

export SECRET_KEY=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/secret_key --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export DB_NAME=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/db_name --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export DB_USER=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/db_user --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export DB_PASSWORD=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/db_password --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export DB_HOST=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/db_host --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export DB_PORT=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/db_port --with-decryption --region us-east-1 --output text | awk '{print $7}'`

export SEO_TOKEN=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/seo_token --with-decryption --region us-east-1 --output text | awk '{print $7}'`

export RECAPTCHA_SECRET=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/recaptcha_secret --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export MAIL_DEFAULT_FROM=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/mail_default_from --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export MAIL_DEFAULT_TO=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/mail_default_to --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export AWS_SES_ACCESS_KEY=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/aws_ses_access_key --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export AWS_SES_SECRET_KEY=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/aws_ses_secret_key --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export S3_UPLOAD_BUCKET=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/s3_upload_bucket --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export S3_UPLOAD_SECRET=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/s3_upload_secret --with-decryption --region us-east-1 --output text | awk '{print $7}'`
export S3_UPLOAD_KEY=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/api_tnris_org/s3_upload_key --with-decryption --region us-east-1 --output text | awk '{print $7}'`

eval /src/data_hub/manage.py collectstatic --noinput "$@"
eval /usr/bin/supervisord "$@"
