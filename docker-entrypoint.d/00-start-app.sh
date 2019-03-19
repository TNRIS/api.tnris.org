#!/bin/sh

export SECRET_KEY=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/secret_key --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_NAME=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_name --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_USER=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_user --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_PASSWORD=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_password --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_HOST=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_host --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export DB_PORT=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/db_port --with-decryption --region us-east-1 --output text | awk '{print $6}'`
export SEO_TOKEN=`/envs/data_hub/bin/aws ssm get-parameters --name /apps/data_tnris_org/seo_token --with-decryption --region us-east-1 --output text | awk '{print $6}'`

eval /src/data_hub/manage.py collectstatic --noinput "$@"
eval /usr/bin/supervisord "$@"
