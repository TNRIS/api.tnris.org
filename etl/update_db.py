'''
script to update data.tnris.org category and use types in rds postgres db
1/7/19
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

    # old categories dictionary --- key is old and value is new
    old_cat_new_cat_dict = {
                            'Bathymetry':'Elevation',
                            'Boundary':'Basemap',
                            'Cultural':'Basemap',
                            'Demographics':'Basemap',
                            'Environmental':'Basemap',
                            'Floodplain':'Hydrography',
                            'Geology':'Basemap',
                            'Land Use Land Cover':'Land Use',
                            'Natural Regions':'Basemap',
                            'Orthoimagery':'Imagery',
                            'Topographic Map':'Basemap',
                            'Transportation':'Basemap'
                            }

    # old_uses = ['Analysis', 'Cartography', 'Feature Extraction', 'General Large Scale Geologic Information and Mapping', 'Historical Use', 'Location', 'Planning']

    # connect to the database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # category db table names
    category_type_table = 'category_type'
    category_relate_table = 'category_relate'
    # use db table names
    # use_type_table = 'use_type'
    # use_relate_table = 'use_relate'

    # sql statements
    category_type_query = "SELECT category_type_id, category FROM %s;" % category_type_table
    category_relate_query = "SELECT category_type_id FROM %s;" % category_relate_table
    # use_type_query = "SELECT use_type_id, use_type FROM %s;" % use_type_table
    # use_relate_query = "SELECT use_type_id FROM %s;" % use_relate_table

    query_list = [category_type_query, category_relate_query]

    change_list = []
    keep_dict = {}
    new_dict = {}
    new_list = []
    all_relates = []
    count = 0
    # print(cat_type)

    # take category type response and generate dict with current ids and new type values
    for i in query_list:
        cur.execute(i)
        db_response = cur.fetchall()
        for x in db_response:
            # limit to type response to create dict
            if len(x) == 2:
                for key, val in old_cat_new_cat_dict.items():
                    # if category response equals key, create current dict
                    if x[1] == key:
                        change_list.append(x[0])
                        # new_cat_dict[x[0]] = val
                    elif x[1] == val:
                        # keep_list.append(x[0])
                        keep_dict[x[0]] = val
                    elif x[1] != val and val not in new_list:
                        # id = str(uuid.uuid4())
                        new_list.append(val)
                        # new_dict[id] = val

                # create uuid for new_dict
                for item in new_list:
                    id = str(uuid.uuid4())
                    new_dict[id] = item

            # limit to relate response to update relate table first
            if len(x) == 1:
                all_relates.append(x)
                # for key, val in new_cat_dict.items():
                #     print(key)
                #     if x[0] == key:
                #         new_relate = x[0]
                #         print(new_relate)
                #         print('value =', val)

                        # update relate table with new ids
                        # cur.execute("UPDATE {table} SET {field} = '{new_id}';".format(
                        #     table=category_relate_table,
                        #     field='category_type_id',
                        #     new_id=new_relate)
                        # )
                        #
                        # try:
                        #     conn.commit()
                        # except:
                        #     cat_list.append()


    # print(change_list)
    # print(keep_dict)
    # print(new_list)
    print(new_dict)
    # print(all_relates)


    # print(current_cat_dict)
    # print(count)
    # print(new_cat_dict)


    # iterate through category types and find those matching old_categories
    # for i[1] in cat_type:
    #     print(i)
    #         print(v)
    #         for k, v in category_dict:
    #         if k == i[1]:
    #             print(v)
    #             cat_matches.append(i[0])
    #             count += 1




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
