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

    # categories dictionary --- key is old and value is new
    cat_dict = {
                'Bathymetry':'Elevation',
                'Boundary':'Basemap',
                'Cultural':'Basemap',
                'Demographics':'Basemap',
                'Environmental':'Basemap',
                'Floodplain':'Hydrography',
                'Geology':'Basemap',
                'Natural Regions':'Basemap',
                'Topographic Map':'Basemap',
                'Transportation':'Basemap'
                }

    # use type dictionary --- key is old and value is new
    use_dict = {
                'Analysis':'Research',
                'Cartography':'Basemap',
                'Feature Extraction':'Remove',
                'General Large Scale Geologic Information and Mapping':'Basemap',
                'Historical Use':'Research',
                'Location':'Research',
                'Planning':'Research'
                }

    # connect to the database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # category db table names
    # category_type_table = 'category_type'
    # category_relate_table = 'category_relate'

    # use db table names
    use_type_table = 'use_type'
    use_relate_table = 'use_relate'

    # sql statements
    # category_type_query = "SELECT category_type_id, category FROM %s;" % category_type_table
    # category_relate_query = "SELECT category_type_id, collection_id, category_relate_id FROM %s;" % category_relate_table
    use_type_query = "SELECT use_type_id, use_type FROM %s;" % use_type_table
    use_relate_query = "SELECT use_type_id, collection_id, use_relate_id FROM %s;" % use_relate_table

    # variables
    relate_dict = {}
    counter = 0
    category_dict = {}
    reverse_cat_dict = {}

    error_list = []

    # take response and build dict
    # cur.execute(category_type_query)
    cur.execute(use_type_query)
    db_response = cur.fetchall()

    for x in db_response:
        # category_dict[x[0]] = x[1]
        # reverse_cat_dict[x[1]] = x[0]
        new_use_dict[x[0]] = x[1]
        reverse_new_use_dict[x[1]] = x[0]

    # print(category_dict)
    print(new_use_dict)

    # cur.execute(category_relate_query)
    cur.execute(use_relate_query)
    db_response = cur.fetchall()

    for i in db_response:
        # cat_name = category_dict[i[0]]
        use_name = new_use_dict[i[0]]
        relate_id = i[2]

        # if cat_name in cat_dict.keys():
        if cat_name in use_dict.keys():
            # new_cat_name = cat_dict[cat_name]
            new_use_name = use_dict[use_name]
            # print(cat_name, new_cat_name)
            new_cat_uuid = reverse_cat_dict[new_cat_name]
            # print(new_cat_uuid)

            # update relate table with new ids
            cur.execute("UPDATE {table} SET {field} = '{new_id}' WHERE category_relate_id = '{relate_id}';".format(
                table=category_relate_table,
                relate_id=relate_id,
                field='category_type_id',
                new_id=new_cat_uuid)
            )

            try:
                conn.commit()
            except:
                error_list.append(relate_id)

    print(error_list)

# execute
if __name__ == '__main__':
    update_db()
