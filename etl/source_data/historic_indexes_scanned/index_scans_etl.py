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

# query temp etl view to compile all the ref info for collections
tablename = 'etl_scanned_index'
query = "SELECT * FROM %s;" % tablename
cur.execute(query)
response = cur.fetchall()
ref = {}
alt_ref = {}
total_collections = 0
dupes = []
for r in response:
    coll = r[0]
    county = r[1]
    agency = r[2]
    try:
        year = int(r[3])
    except:
        continue
    try:
        alt_year = int(r[4])
    except:
        continue
    # print(coll,county,agency,year)
    if county is not None and "," not in county and agency != '':
        county = county.replace(' ', '')
        if agency in ref.keys():
            if county in ref[agency].keys():
                if year in ref[agency][county].keys():
                    # print("uh oh, we got a dupe: ", agency, county, year)
                    # print(coll,county,agency,year)
                    dupes.append(agency)
                else:
                    ref[agency][county][year] = coll
                    alt_ref[agency][county][alt_year] = coll
                    total_collections += 1
            else:
                ref[agency][county] = {}
                ref[agency][county][year] = coll

                alt_ref[agency][county] = {}
                alt_ref[agency][county][alt_year] = coll

                total_collections += 1
        else:
            ref[agency] = {}
            ref[agency][county] = {}
            ref[agency][county][year] = coll

            alt_ref[agency] = {}
            alt_ref[agency][county] = {}
            alt_ref[agency][county][alt_year] = coll
            total_collections += 1
    else:
        # print('multi county: ', county, '// or agency: ', agency)
        continue
print(total_collections)
# print(dupes)

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
        if '/index/scanned/' in key and key[-4:] == '.tif':
            objects.append({'Key':key, 'Size': str(i['Size'])})
    if response['IsTruncated']:
        get_objects(response['NextContinuationToken'])

get_objects()
print(len(objects))
total_size = 0
total_processed = 0
# iterate the s3 scanned files and disassemble to find their related collection_id
# from the ref object
for i in objects:
    # print(i)
    parts = i['Key'].split("/")
    county = parts[1]
    agency = parts[-1].split('_')[0]
    year = int(parts[-1].split('_')[1])
    sheet = parts[-1].split('_')[2].replace('.tif', '')
    link = 'https://s3.amazonaws.com/tnris-ls4/%s' % (i['Key'])
    raw_size = i['Size'][:-5]
    total_size += int(i['Size'])
    # print(int(i['Size']))
    try:
        size = str(raw_size[:-1]) + "." + str(raw_size[-1]) + "MB"
    except:
        print('weird size')
        size = ''
        # continue
    # try to get the collection id for the scanned s3 image
    try:
        collection_id = alt_ref[agency][county][year]
        total_processed += 1
    except:
        # print(agency, county, year, sheet)
        try:
            collection_id = alt_ref[agency][county][year]
            total_processed += 1
        except:
            print(agency, county, year, sheet)
            continue
    # insert into the Database
    newUuid = uuid.uuid4()
    timestamp = datetime.datetime.now()
    newQuery = "INSERT INTO photo_index_scanned_ls4_link (id, collection_id, year, size, sheet, link, created, last_modified) VALUES ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s')" % (newUuid, collection_id, year, size, sheet, link, timestamp, timestamp)
    print(newQuery)
    cur.execute(newQuery)
    conn.commit()

print(total_size)
###########
cur.close()
conn.close()
print(str(len(objects)) + ' total scanned indexes in s3')
print(str(total_processed) + ' total indexes added to database')

print("that's all folks!!")
