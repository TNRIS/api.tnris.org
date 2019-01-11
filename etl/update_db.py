'''
script to update data.tnris.org category and use types in rds postgres db
1/7/19
'''

# imports
import os, datetime, csv
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
    use_relate_query = "SELECT use_type_id, use_relate_id FROM %s;" % use_relate_table

    # variables
    counter = 0
    response_dict = {}
    reverse_response_dict = {}
    error_list = []

    # take responses and build dicts
    # cur.execute(category_type_query)
    cur.execute(use_type_query)
    db_response = cur.fetchall()

    for x in db_response:
        response_dict[x[0]] = x[1]
        reverse_response_dict[x[1]] = x[0]

    # cur.execute(category_relate_query)
    # cur.execute(use_relate_query)
    # db_response = cur.fetchall()
    csv_file = 'source_data/use_relate.csv'
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        # print(csv_reader)
        print(use_dict.keys())

        for i in csv_reader:
            print(i)

            name = response_dict[i['use_type_id']]
            relate_id = i['use_relate_id']

        # run this sql to load data back to postgres db
        #     try:
        #         cur.execute("INSERT INTO {table} (use_relate_id, created, last_modified, collection_id, use_type_id) VALUES ('{column1}', '{column2}', '{column3}', '{column4}', '{column5}');".format(
        #                     table=use_relate_table,
        #                     column1=i['use_relate_id'],
        #                     column2=i['created'],
        #                     column3=i['last_modified'],
        #                     column4=i['collection_id'],
        #                     column5=i['use_type_id'])
        #                     )
        #
        #         conn.commit()
        #
        #     except:
        #         error_list.append("'" + relate_id + "'")
        #
        # print(error_list)

            # if name in cat_dict.keys():
            print(name)
            if name in use_dict.keys():
                print("YES!")
                # new_name = cat_dict[name]
                new_name = use_dict[name]

                new_uuid = reverse_response_dict[new_name]

                print(new_uuid)

                try:
                    # update category relate table with new ids
                    # cur.execute("UPDATE {table} SET {field} = '{new_id}' WHERE category_relate_id = '{relate_id}';".format(
                    #     table=category_relate_table,
                    #     relate_id=relate_id,
                    #     field='category_type_id',
                    #     new_id=new_uuid)
                    # )

                    # update use relate table with new ids
                    cur.execute("UPDATE {table} SET {field} = '{new_id}' WHERE use_relate_id = '{relate_id}';".format(
                        table=use_relate_table,
                        relate_id=relate_id,
                        field='use_type_id',
                        new_id=new_uuid)
                    )

                    conn.commit()

                except:
                    # cur.close()
                    # cur = conn.cursor()
                    #
                    # query = "DELETE FROM {table} WHERE use_relate_id = '{relate_id}';".format(
                    #     table=use_relate_table,
                    #     relate_id=relate_id)
                    #
                    # print(query)
                    #
                    # cur.execute(query)
                    #
                    # conn.commit()

                    error_list.append("'" + relate_id + "'")

        print(error_list)


# execute
if __name__ == '__main__':
    update_db()
