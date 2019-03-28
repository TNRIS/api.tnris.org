import boto3
import os
import psycopg2
import datetime
import uuid

#########
# go get the scanned index files from s3
client = boto3.client('s3')
objects = []

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
        key = i['Key']
        if '/index/scanned/' in key and key[-8:] == '.tif.tif':
            objects.append({'Key':key, 'Size': str(i['Size'])})
    if response['IsTruncated']:
        get_objects(response['NextContinuationToken'])

get_objects()
print('scans: %s' % len(objects))
s3 = boto3.resource('s3')
one = 0
for o in objects:
    print(o)
    new_key = o['Key'].replace('.tif.tif', '.tif')
    # print(new_key)
    # if 'Harris' in o['Key'] and 'USDA_1973_01.tif.tif' in o['Key']:
    # old_source = 'tnris-ls4/%s' % o['Key']
    # s3.Object('tnris-ls4',new_key).copy_from(CopySource=old_source)
    # s3.Object('tnris-ls4',o['Key']).delete()
    one += 1



print("that's all folks!!")
