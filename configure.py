import boto3
import json
client = boto3.client('secretsmanager')
cloudformation = boto3.resource('cloudformation')

api_response = client.get_secret_value(
    SecretId='api-tnris-org'
)

gspread_response = client.get_secret_value(
    SecretId='api-gspread-config'
)

stack_resource = cloudformation.StackResource('datahub-master', 'MasterCloudfront')
secrets = json.loads(api_response["SecretString"])
gspread = gspread_response["SecretString"]

#Create the gspread_config.json file
text_file = open("./src/data_hub/gspread_config.json", "w")
text_file.write(gspread)
text_file.close()

export_command = ("export DB_PASSWORD=" + secrets["DB_PASSWORD"] +
" DB_NAME=" + secrets["DB_NAME"] +
" DB_USER=" + secrets["DB_USER"] +
" DB_HOST=localhost" +
" DB_PORT=9000" +
" SEO_TOKEN=" + secrets["SEO_TOKEN"] +

# CONTACT APP ENV VARIABLES
" RECAPTCHA_SECRET=" + secrets["RECAPTCHA_SECRET"] +
" MAIL_DEFAULT_FROM=" + secrets["MAIL_DEFAULT_FROM"] +
" MAIL_DEFAULT_TO=" + secrets["MAIL_DEFAULT_TO"] +
" AWS_SES_ACCESS_KEY=" + secrets["AWS_SES_ACCESS_KEY"] +
" AWS_SES_SECRET_KEY=" + secrets["AWS_SES_SECRET_KEY"] +
" S3_UPLOAD_BUCKET=" + secrets["S3_UPLOAD_BUCKET"] +
" S3_UPLOAD_SECRET=" + secrets["S3_UPLOAD_SECRET"] +
" S3_UPLOAD_KEY=" + secrets["S3_UPLOAD_KEY"] +
" MAPSERVER_DB_NAME=" + secrets["MAPSERVER_DB_NAME"] +
" MAPSERVER_DB_USER=" + secrets["MAPSERVER_DB_USER"] +
" MAPSERVER_DB_PASSWORD=" + secrets["MAPSERVER_DB_PASSWORD"] +
" DATAHUB_MASTER_CLOUDFRONT=" + stack_resource.physical_resource_id +

# CCP Environment Variables
" CCP_MERCHANT_CODE=" + secrets["CCP_MERCHANT_CODE"] +
" CCP_MERCHANT_KEY=" + secrets["CCP_MERCHANT_KEY"] +
" CCP_SERVICE_CODE=" + secrets["CCP_SERVICE_CODE"] +
" CCP_API_KEY=" + secrets["CCP_API_KEY"] +
" CCP_ACCESS_CODE=" + secrets["CCP_ACCESS_CODE"] +

# Encryption Environmental Variables
" FKEY1=" + secrets["FKEY1"] +
" ACCESS_PEPPER=" + secrets["ACCESS_PEPPER"] +

# the following is only used within ETL scripts (specifically, migrate.py)
" TNRIS_REPO='local_path_to_cloned_tnris_website_repo'")

print(export_command)
