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

# s3 variables used in all three functions
old_names = ['overview.jpg', 'urban.jpg', 'thumbnail.jpg', 'natural.jpg']
client = boto3.client('s3')

# iterate through, copy existing images and rename with uuid
# def get_s3_images(bucket, suffix=''):
#
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
#
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
def update_db(bucket, suffix=''):

    # Database Connection Info
    database = os.environ.get('DB_NAME')
    username = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')

    conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

    tablename = 'collection'

    print(conn_string)

    # s3 stuff
    kwargs = {'Bucket': bucket}

    # connect to database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    query = "SELECT collection_id, thumbnail_image FROM %s;" % tablename
    cur.execute(query)

    db_response = cur.fetchall()
    count = 0

    while True:
        s3_resp = client.list_objects_v2(**kwargs)

        for obj in s3_resp['Contents']:
            if obj['Key'].endswith(suffix):
                collection_obj = {}
                collection = obj['Key'].split('/')[0]
                image = obj['Key'].rsplit('/')[-1]
                count += 1
                # print(str(count) + ': ' + collection, image)
                # db stuff
                for item in db_response:
                    id, thumb = item
                    if thumb.find('thumbnail.jpg') and id == collection:
                        # update_thumb = "UPDATE %s SET thumbnail_image = %s;" % tablename, thumb
                        print(str(count) + ': ' + str(id) + ' == ' + str(collection) + '; updating with ' + str(image))
                        # cur.execute(update_thumb)



        try:
            kwargs['ContinuationToken'] = s3_resp['NextContinuationToken']
        except KeyError:
            break


# execute functions
# get_s3_images('data.tnris.org', '.jpg')
# delete_old('data.tnris.org', '.jpg')

update_db('data.tnris.org', '.jpg')
