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
client = boto3.client('s3')

# iterate through, copy existing images and rename with uuid
def s3_images_to_db(bucket):

    kwargs = {'Bucket': bucket}
    docs = 'documents/'
    images = 'images/'
    unique_images = []
    unique_docs = []
    total_count = 0
    img_count = 0
    doc_count = 0
    slash_count = 0

    base_url = 'https://tnris-org-static.s3.amazonaws.com/'

    # Database Connection Info
    database = os.environ.get('DB_NAME')
    username = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')

    # connection string
    conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

    # db table names
    image_table = 'tnris_image_url'
    doc_table = 'tnris_doc_url'

    # connect to the database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # sql statement to get both collection_id and thumbnail_image fields
    image_query = "SELECT image_id, image_name, image_url FROM %s;" % image_table
    doc_query = "SELECT doc_id, doc_name, doc_url FROM %s;" % doc_table

    # execute sql statements
    # cur.execute(image_query)
    cur.execute(doc_query)

    # get response from both collection and image table queries
    db_response = cur.fetchall()

    fixes = []

    while True:
        resp = client.list_objects_v2(**kwargs)

        for obj in resp['Contents']:
            key = obj['Key']
            total_count += 1

            # if key.startswith(images) and key not in unique_images and key is not None:
            #     unique_images.append(base_url + key.strip())
            #     img_count += 1
            #     image_id = uuid.uuid4()
            #     image_name = key.rsplit('/')[-1]
            #     print(image_name)
            #     image_url = base_url + key.strip()
            #     timestamp = datetime.datetime.now()
            #
            #     # update the aws postgres rds db with new image names/urls
            #     cur.execute("INSERT INTO {table} ({id},{name},{url},{create},{modify}) VALUES ('{v1}','{v2}','{v3}','{v4}','{v5}');".format(
            #         table=image_table,
            #         id='image_id',
            #         name='image_name',
            #         url='image_url',
            #         create='created',
            #         modify='last_modified',
            #         v1=image_id,
            #         v2=image_name,
            #         v3=image_url,
            #         v4=timestamp,
            #         v5=timestamp)
            #     )
            #     try:
            #         conn.commit()
            #     except:
            #         fixes.append(key)

            if key.startswith(docs) and key not in unique_docs and key is not None:
                unique_docs.append(base_url + key.strip())
                doc_count += 1
                doc_id = uuid.uuid4()
                doc_name = key.rsplit('/')[-1]
                print(doc_name)
                doc_url = base_url + key.strip()
                timestamp = datetime.datetime.now()

                # update the aws postgres rds db with new image names/urls
                cur.execute("INSERT INTO {table} ({id},{name},{url},{create},{modify}) VALUES ('{v1}','{v2}','{v3}','{v4}','{v5}');".format(
                    table=doc_table,
                    id='doc_id',
                    name='doc_name',
                    url='doc_url',
                    create='created',
                    modify='last_modified',
                    v1=doc_id,
                    v2=doc_name,
                    v3=doc_url,
                    v4=timestamp,
                    v5=timestamp)
                )
                try:
                    conn.commit()
                except:
                    fixes.append(key)

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

    print('total count ---->', total_count, 'images:', img_count, 'docs:', doc_count)

    print(fixes)

    # print('unique images:', unique_images)
    # print('unique docs:', unique_docs)

# execute function
s3_images_to_db('tnris-org-static')
