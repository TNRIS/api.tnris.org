#
#
#
# ORIGINAL SCRIPT TO CREATE HARD HTML CODE FOR tnris.org/mapserver LIST OF SCANNED S3 INDEXES
# WITH LINKS TO DOWNLOAD. THIS IS DEPRECATED AS THE PAGE WAS UPDATED TO BE DYNAMIC
# USING THE DATABASE API AT TIME OF PAGE LOAD
#
#
#
#

import boto3
import os

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
        if '/index/scanned/' in key and key[-4:] == '.tif':
            objects.append({'Key':key, 'Size': str(i['Size'])})
    if response['IsTruncated']:
        get_objects(response['NextContinuationToken'])

get_objects()
# print(len(objects))
total_size = 0
for i in objects:
    # print(i)
    parts = i['Key'].split("/")
    county = parts[1]
    agency = parts[-1].split('_')[0]
    year = parts[-1].split('_')[1]
    sheet = parts[-1].split('_')[2].replace('.tif', '')
    link = 'https://s3.amazonaws.com/tnris-ls4/%s' % (i['Key'])
    raw_size = i['Size'][:-5]
    total_size += int(i['Size'])
    print(int(i['Size']))
    try:
        size = str(raw_size[:-1]) + "." + str(raw_size[-1]) + "MB"
    except:
        continue
    # print(county, agency, year, sheet, link)
    html = '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href="%s">Download</a></td></tr>' % (county, agency, year, sheet, size, link)
    # print(html)
print(total_size)

print("that's all folks!!")
