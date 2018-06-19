#!/bin/sh

export SECRET_KEY=`/envs/data-concierge/bin/aws ssm get-parameters --name /apps/tnris_data_concierge/secret_key --with-decryption --region us-east-1 --output text | awk '{print $4}'`
export DB_NAME=`/envs/data-concierge/bin/aws ssm get-parameters --name /apps/tnris_data_concierge/db_name --with-decryption --region us-east-1 --output text | awk '{print $4}'`
export DB_USER=`/envs/data-concierge/bin/aws ssm get-parameters --name /apps/tnris_data_concierge/db_user --with-decryption --region us-east-1 --output text | awk '{print $4}'`
export DB_PASSWORD=`/envs/data-concierge/bin/aws ssm get-parameters --name /apps/tnris_data_concierge/db_password --with-decryption --region us-east-1 --output text | awk '{print $4}'`
export DB_HOST=`/envs/data-concierge/bin/aws ssm get-parameters --name /apps/tnris_data_concierge/db_host --with-decryption --region us-east-1 --output text | awk '{print $4}'`
export AWS_STORAGE_BUCKET_NAME=`/envs/data-concierge/bin/aws ssm get-parameters --name /apps/tnris_data_concierge/aws_storage_bucket_name --region us-east-1 --output text | awk '{print $4}'`

eval /src/data_concierge/manage.py collectstatic --noinput "$@"
eval /usr/bin/supervisord "$@"
