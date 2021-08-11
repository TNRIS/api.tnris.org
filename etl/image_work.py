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
import datetime

# s3 variables used in all three functions
old_names = ['overview.jpg', 'urban.jpg', 'thumbnail.jpg', 'natural.jpg']
client = boto3.client('s3')

# iterate through, copy existing images and rename with uuid
def get_s3_images(bucket, suffix=''):

    kwargs = {'Bucket': bucket}
    count = 0

    while True:
        resp = client.list_objects_v2(**kwargs)

        for obj in resp['Contents']:
            if obj['Key'].endswith(suffix):
                key_path = obj['Key']
                image = key_path.rsplit('/')[-1].rstrip()

                if image in old_names:
                    count += 1
                    new_name = key_path.replace(image, str(uuid.uuid4()) + suffix)
                    # print(bucket + '/' + key_path)
                    # print(str(count) + ': ' + key_path + ' --> ' + new_name)
                    print('#{c} copying {k} to new file {n}...'.format(c=count, k=key_path, n=new_name))
                    client.copy_object(Bucket=bucket, CopySource=bucket + '/' + key_path, Key=new_name)


        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

# delete all images with old names
def delete_old(bucket, suffix=''):

    kwargs = {'Bucket': bucket}
    count = 0

    while True:
        resp = client.list_objects_v2(**kwargs)

        for obj in resp['Contents']:
            key_path = obj['Key']
            image = key_path.rsplit('/')[-1].rstrip()
            if key_path.endswith(suffix) and image in old_names:
                count += 1
                print('#{c} deleting {k}...'.format(c=count, k=key_path))
                client.delete_object(Bucket=bucket, Key=key_path)

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

# update the aws postgres rds db with new image names/urls
def update_db(bucket, suffix=''):

    # Database Connection Info
    database = os.environ.get('DB_NAME')
    username = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    # connection string
    conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)
    # db table names
    collection_table = 'collection'
    image_table = 'image'
    # s3 stuff to be used later
    kwargs = {'Bucket': bucket}
    base_url = 'https://s3.amazonaws.com/data.tnris.org/'
    # connect to the database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    # sql statement to get both collection_id and thumbnail_image fields
    collection_query = "SELECT collection_id, thumbnail_image FROM %s;" % collection_table
    image_query = "SELECT image_id, image_url, collection_id FROM %s;" % image_table
    # execute sql statements
    # cur.execute(collection_query)
    cur.execute(image_query)
    # get response from both collection and image table queries
    db_response = cur.fetchall()

    add_images = []
    unique_cols = []
    # print(db_response)
    while True:
        # s3 stuff
        s3_resp = client.list_objects_v2(**kwargs)
        count = 0
        for obj in s3_resp['Contents']:
            key = obj['Key']
            if key.endswith(suffix) and key is not None:
                print(key)
                img_id = uuid.UUID(key.split('/')[-1].rstrip(suffix).strip())
                img_url = base_url + key.strip()
                col_id = uuid.UUID(key.split('/')[0].strip())
                timestamp = datetime.datetime.now()

                # print("inserting image {}".format(count))
                # cur.execute("INSERT INTO {table} ({id},{url},{create},{modify},{col}) VALUES ('{v1}','{v2}','{v3}','{v4}','{v5}');".format(
                #     table=image_table,
                #     id='image_id',
                #     url='image_url',
                #     create='created',
                #     modify='last_modified',
                #     col='collection_id',
                #     v1=img_id,
                #     v2=img_url,
                #     v3=timestamp,
                #     v4=timestamp,
                #     v5=col_id)
                # )
                # try:
                #     conn.commit()
                # except:
                #     add_images.append(col_id)

                cur.execute("UPDATE {table} SET {field} = '{url}' WHERE collection_id = '{col_id}';".format(
                    table=collection_table,
                    field='thumbnail_image',
                    url=img_url,
                    col_id=col_id)
                )

                try:
                    conn.commit()
                except:
                    add_images.append(col_id)

                # cur.execute("INSERT INTO {table};".format(table=image_table))
                # if col_id not in unique_cols:
                #     unique_cols.append(col_id)
                # if col_id not in unique_cols:
                    # unique_cols.append(id)

                # img_id = key.split('/')[-1].rstrip(suffix).strip()
                # img_url = base_url + key.strip()
                # add_images = add_images.append([img_id, img_url, col_id])
                # cur.execute("INSERT INTO {table} ({id},{url},{col}) VALUES ({v_id}, {v_url}, {v_col});".format(table=image_table, id=image_id, url=image_url, col=collection_id, v_id=img_id, v_url=img_url, v_col=col_id)

        try:
            kwargs['ContinuationToken'] = s3_resp['NextContinuationToken']
        except KeyError:
            break

    print('Bad collections...')
    print(add_images)

    # for item in db_response:
    #     image_id, image_url, collection_id = item
    #     print(image_url)
    #     cur.execute("INSERT INTO {table} ({id},{url},{col}) VALUES ({v_id}, {v_url}, {v_col});".format(table=image_table, id=image_id, url=image_url, col=collection_id, v_id=img_id, v_url=img_url, v_col=col_id)


    # print(str(count) + ": " + col_id + ",\n" + img_id + ",\n" + img_url + ",\n")

    # db stuff
    # for item in db_response:
    #     image_id, image_url, collection_id = item
    #     print('|', image_id, '|', image_url, '|', collection_id, '|')

    # if thumb.find('thumbnail.jpg') and id == collection:
    #     update_thumb = "UPDATE %s SET thumbnail_image = %s;" % tablename, thumb
    #     print(str(count) + ': ' + str(id) + ' == ' + str(collection) + '; updating with ' + str(image))
    #     cur.execute(update_thumb)


# execute functions
# get_s3_images('data.tnris.org', '.jpg')
# delete_old('data.tnris.org', '.jpg')

update_db('data.tnris.org', '.jpg')
