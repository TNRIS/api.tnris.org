'''
1) get_s3_images function iterates through all data.tnris.org s3 bucket collection ids (keys),
copies each image and renames the copy to a new uuid.

2) delete_old function to delete the old image name jpgs in s3.

3) update_db function adds record to Django image table with:
    - image_id = new uuid generated from get_s3_images function
    - collection_id = collection_id
    - image_url = new url
   this function also replaces the existing collection table thumbnail_image records with the new uuid names.
'''
import os
import boto3, uuid
import psycopg2

old_names = ['overview.jpg', 'urban.jpg', 'thumbnail.jpg', 'natural.jpg']

# iterate through, copy existing images and rename with uuid
# def get_s3_images(bucket, suffix=''):
#     client = boto3.client('s3')
#     kwargs = {'Bucket': bucket}
#     count = 0
#
#     while True:
#         resp = client.list_objects_v2(**kwargs)
#
#         for obj in resp['Contents']:
#             if obj['Key'].endswith(suffix):
#                 key_path = obj['Key']
#                 image = key_path.rsplit('/')[-1].rstrip()
#
#                 if image in old_names:
#                     count += 1
#                     new_name = key_path.replace(image, str(uuid.uuid4()) + suffix)
#                     # print(bucket + '/' + key_path)
#                     # print(str(count) + ': ' + key_path + ' --> ' + new_name)
#                     print('#{c} copying {k} to new file {n}...'.format(c=count, k=key_path, n=new_name))
#                     client.copy_object(Bucket=bucket, CopySource=bucket + '/' + key_path, Key=new_name)
#
#
#         try:
#             kwargs['ContinuationToken'] = resp['NextContinuationToken']
#         except KeyError:
#             break

# delete all images with old names
# def delete_old(bucket, suffix=''):
#     client = boto3.client('s3')
#     kwargs = {'Bucket': bucket}
#     count = 0
#
#     while True:
#         resp = client.list_objects_v2(**kwargs)
#
#         for obj in resp['Contents']:
#             key_path = obj['Key']
#             image = key_path.rsplit('/')[-1].rstrip()
#             if key_path.endswith(suffix) and image in old_names:
#                 count += 1
#                 print('#{c} deleting {k}...'.format(c=count, k=key_path))
#                 client.delete_object(Bucket=bucket, Key=key_path)
#
#         try:
#             kwargs['ContinuationToken'] = resp['NextContinuationToken']
#         except KeyError:
#             break

# update the aws postgres rds db with new image names/urls
def update_db():
    # Database Connection Info
    database = 'data.tnris.org'
    username = 'tnris'
    password = os.environ.get('DB_PASSWORD')
    host = 'localhost'
    port = '9000'

    print(database, username, password, host, port)

    conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

    # connect to database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # s3 boto client
    client = boto3.client('s3')




# execute functions
# get_s3_images('data.tnris.org', '.jpg')
# delete_old('data.tnris.org', '.jpg')
update_db()
