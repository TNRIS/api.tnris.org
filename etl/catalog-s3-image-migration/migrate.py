# file is for the initial migration of the images path'd within the Collection table
# over to the s3 bucket and then update the image url within the Collection table
# git clone tnris.org repo required!
import os
import boto3
import psycopg2
# import string

# Database Connection Info
database = os.environ.get('DB_NAME')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

# requires an environment variable that is a path to the local tnris.org repo
# NO trailing slash!
tnris_repo = os.environ.get('TNRIS_REPO')
repo_static = tnris_repo + '/static'
print(repo_static)

# connect to database
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# query collection table id, name, and image fields
tablename = 'collection'
query = "SELECT collection_id, name, overview_image, thumbnail_image, natural_image, urban_image, supplemental_report_url, lidar_breaklines_url, tile_index_url FROM %s;" % tablename
cur.execute(query)
response = cur.fetchall()

# counters for QA
img_counter = 0
url_counter = 0
bad_keys = []

# iterate records
s3 = boto3.resource('s3')
for c in response:
    id, name, over, thb, nat, urb, sup_url, lb_url, ti_url = c
    imgs = [over, thb, nat, urb]
    urls = [sup_url, lb_url, ti_url]
    print(name)
    # handle images
    for idx, i in enumerate(imgs):
        if i is not None:
            # setup upload variables
            local = os.path.join(repo_static, i)
            if idx == 0:
                key_nm = 'overview.jpg'
                fld_nm = 'overview_image'
            elif idx == 1:
                key_nm = 'thumbnail.jpg'
                fld_nm = 'thumbnail_image'
            elif idx == 2:
                key_nm = 'natural.jpg'
                fld_nm = 'natural_image'
            elif idx == 3:
                key_nm = 'urban.jpg'
                fld_nm = 'urban_image'
            else:
                raise
            key = "%s/assets/%s" % (id, key_nm)
            # s3 upload
            # s3.meta.client.upload_file(local, 'data.tnris.org', key)
            # print("%s upload success!" % key)
            img_counter += 1
            # update image path in collection table
            new_path = "https://s3.amazonaws.com/data.tnris.org/" + key
            query = "UPDATE %s SET %s = '%s' WHERE collection_id = '%s';" % (tablename, fld_nm, new_path, id)
            # print(query)
            # cur.execute(query)
            # conn.commit()

    # handle urls
    for idx, u in enumerate(urls):
        if u is not None:
            # setup s3 cp variables
            key_nm = name.lower().replace(', ', '-').replace(' & ', '-').replace(' ', '-').replace('(', '').replace(')', '').replace('\\', '-').replace('/', '-').replace('&', '').replace(',', '-')
            if idx == 0:
                key = "%s/assets/%s-supplemental-report.zip" % (id, key_nm)
                fld_nm = 'supplemental_report_url'
            elif idx == 1:
                key = "%s/assets/%s-lidar-breaklines.zip" % (id, key_nm)
                fld_nm = 'lidar_breaklines_url'
            elif idx == 2:
                key = "%s/assets/%s-tile-index.zip" % (id, key_nm)
                fld_nm = 'tile_index_url'
            else:
                raise
            # this snippet was used during testing to verify the key_nm formatting
            # didn't contain any other non-normal characters
            # letters = list(string.ascii_lowercase)
            # letters.extend(('0','1','2','3','4','5','6','7','8','9','-','.'))
            # for ltr in key_nm:
            #     if ltr not in letters:
            #         print(key_nm, key)

            # s3 cp
            src_key = u.replace("https://tnris-datadownload.s3.amazonaws.com/", '')
            src = {
                'Bucket': 'tnris-datadownload',
                'Key': src_key
            }
            try:
                s3.meta.client.copy(src, 'data.tnris.org', key)
                print("%s copy success!" % key)
            except:
                bad_keys.append(src_key)
            url_counter += 1
            # update url path in collection table
            new_path = "https://s3.amazonaws.com/data.tnris.org/" + key
            query = "UPDATE %s SET %s = '%s' WHERE collection_id = '%s';" % (tablename, fld_nm, new_path, id)
            # print(query)
            # cur.execute(query)
            # conn.commit()


cur.close()
conn.close()

print('image count:', img_counter)
print('url count:', url_counter)
print(bad_keys)
print("that's all folks!!")
