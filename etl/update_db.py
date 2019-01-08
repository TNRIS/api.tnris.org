'''
script to update data.tnris.org category and use types in rds postgres db
'''

# imports
import os, datetime
import uuid, psycopg2

# update the aws postgres rds db with new category types
def update_db():

    # Database Connection Info
    database = os.environ.get('DB_NAME')
    username = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')

    # connection string
    conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

    # db table names
    category_type_table = 'category_type'
    category_relate_table = 'category_relate'

    # categories to be changed
    old_categories = ['Bathymetry', 'Boundary', 'Cultural', 'Demographics', 'Elevation', 'Environmental', 'Floodplain', 'Geology', 'Historic Imagery', 'Hydrography',
                        'Land Use Land Cover', 'Lidar', 'Natural Regions', 'Orthoimagery', 'Reference Grid', 'Topographic Map', 'Transportation', 'Weather']

    old_uses = ['Analysis', 'Cartography', 'Feature Extraction', 'General Large Scale Geologic Information and Mapping', 'Historical Use', 'Location', 'Planning']

    # connect to the database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # sql statements
    category_type_query = "SELECT category_type_id, category FROM %s;" % category_type_table
    category_relate_query = "SELECT category_type_id FROM %s;" % category_relate_table
    query_list = [category_type_query, category_relate_query]

    # execute list of sql queries and assign to variables
    for i in query_list:
        cur.execute(i)
        db_response = cur.fetchall()
        for x in db_response:
            if len(x) > 1:
                cat_type = db_response
            else:
                cat_relate = db_response

    # print(cat_type)
    # print(cat_relate)

    # iterate through category types and find those matching old_categories
    for i in cat_type:
        for x in old_categories:
            if i[1] == x:
                cat_match_id = i[0]
                print('matching cat id:', cat_match_id)
            else:
                print('no match')

            for s in cat_relate:
                if s == cat_match_id:
                    print(s, '---', i[0])

    # while True:

    #     db_response = cur.execute(category_type_query)
    #
    #     for r in cat_type:
    #         print(r[1])
    #         print(r)
    #         db_cat_name = r[1]
    #         for i in old_categories:
    #             if i == db_cat_name:
    #                 print(db_cat_name)
    #                 cat_match = db_cat_name
    #                 for

    '''
    while True:

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

                print("inserting image {}".format(count))
                cur.execute("INSERT INTO {table} ({id},{url},{create},{modify},{col}) VALUES ('{v1}','{v2}','{v3}','{v4}','{v5}');".format(
                    table=image_table,
                    id='image_id',
                    url='image_url',
                    create='created',
                    modify='last_modified',
                    col='collection_id',
                    v1=img_id,
                    v2=img_url,
                    v3=timestamp,
                    v4=timestamp,
                    v5=col_id)
                )
                try:
                    conn.commit()
                except:
                    add_images.append(col_id)

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

                cur.execute("INSERT INTO {table};".format(table=image_table))
                if col_id not in unique_cols:
                    unique_cols.append(col_id)
                if col_id not in unique_cols:
                    unique_cols.append(id)

                img_id = key.split('/')[-1].rstrip(suffix).strip()
                img_url = base_url + key.strip()
                add_images = add_images.append([img_id, img_url, col_id])
                cur.execute("INSERT INTO {table} ({id},{url},{col}) VALUES ({v_id}, {v_url}, {v_col});".format(table=image_table, id=image_id, url=image_url, col=collection_id, v_id=img_id, v_url=img_url, v_col=col_id)

        try:
            kwargs['ContinuationToken'] = s3_resp['NextContinuationToken']
        except KeyError:
            break

    print('Bad collections...')
    print(add_images)

    for item in db_response:
        image_id, image_url, collection_id = item
        print(image_url)
        cur.execute("INSERT INTO {table} ({id},{url},{col}) VALUES ({v_id}, {v_url}, {v_col});".format(table=image_table, id=image_id, url=image_url, col=collection_id, v_id=img_id, v_url=img_url, v_col=col_id)


    print(str(count) + ": " + col_id + ",\n" + img_id + ",\n" + img_url + ",\n")

    # db stuff
    # for item in db_response:
    #     image_id, image_url, collection_id = item
    #     print('|', image_id, '|', image_url, '|', collection_id, '|')
    #
    # if thumb.find('thumbnail.jpg') and id == collection:
    #     update_thumb = "UPDATE %s SET thumbnail_image = %s;" % tablename, thumb
    #     print(str(count) + ': ' + str(id) + ' == ' + str(collection) + '; updating with ' + str(image))
    #     cur.execute(update_thumb)

    '''

# execute
if __name__ == '__main__':
    update_db()
