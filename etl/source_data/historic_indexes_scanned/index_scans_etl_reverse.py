#
#
#
# FOR QC CHECKING THAT ALL RECORDS IN photo_index_scanned_ls4_link TABLE HAVE
# ACTUAL MATCHING KEYS/FILES IN S3
#
#
#

import boto3
import os
import psycopg2
import datetime
import uuid

database = os.environ.get('DB_NAME')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

# connect to database
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# go get the scanned index files from s3
client = boto3.client('s3')
all_keys = []
count_keys = []
print("---------------------------------------------------")
print("The following are keys which have dpi in the name (only non-800dpi permitted):")
def get_objects(token=''):
    if token == '':
        response = client.list_objects_v2(
            Bucket='tnris-ls4',
            Prefix='bw'
        )
    else:
        response = client.list_objects_v2(
            Bucket='tnris-ls4',
            Prefix='bw',
            ContinuationToken=token
        )
    for i in response['Contents']:
        key = 'https://s3.amazonaws.com/tnris-ls4/' + i['Key']
        key2 = 'https://tnris-ls4.s3.amazonaws.com/' + i['Key']
        if '/index/scanned/' in key and key[-4:] == '.tif':
            all_keys.append(key)
            all_keys.append(key2)
            count_keys.append(key)
            if 'dpi' in key:
                print(key)

    if response['IsTruncated']:
        get_objects(response['NextContinuationToken'])

get_objects()
print("---------------------------------------------------")
print("TOTALS:")
print('s3 scans count: %s' % len(count_keys))
# query temp etl view to compile all the ref info for collections
tablename = 'photo_index_scanned_ls4_link'
query = "SELECT link FROM %s;" % tablename
cur.execute(query)
response = cur.fetchall()
all_links = [r[0] for r in response]
print('database records count: %s' % len(response))
print("---------------------------------------------------")
print("The following are keys in the database which are not in s3/cloudberry:")
for link in all_links:
    if link not in all_keys:
        print(link)

print("---------------------------------------------------")
print("The following are keys in the s3/cloudberry which are not in the database:")

for c in count_keys:
    if c not in all_links:
        alt_link = c.replace('https://s3.amazonaws.com/tnris-ls4/', 'https://tnris-ls4.s3.amazonaws.com/')
        if alt_link not in all_links:
            print(c.replace('https://s3.amazonaws.com/tnris-ls4/', ''))

print("---------------------------------------------------")
cur.close()
conn.close()

print("that's all folks!!")
