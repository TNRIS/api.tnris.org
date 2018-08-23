#!/bin/sh

export SECRET_KEY=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/secret_key --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_NAME=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_name --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_USER=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_user --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_PASSWORD=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_password --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_HOST=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_host --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_PORT=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_port --with-decryption --region us-east-1 --output text | awk '{print $6}'`

export AWS_ACCESS_KEY_ID=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/aws_access_key_id --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export AWS_SECRET_ACCESS_KEY=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/aws_secret_access_key --with-decryption --region us-east-1 --output text | awk '{print $6}'`

eval /src/data_hub/manage.py collectstatic --noinput "$@"
eval /usr/bin/supervisord "$@"
