# --------------- IMPORTS ---------------
import psycopg2
import os
import urllib3, json, uuid

# Database Connection Info
database = os.environ.get('DB_NAME')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

# --------------- Main handler ------------------

def lambda_handler(event, context):
    print(event)
    # connect to database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    tablename = 'etl_scanned_index'
    query = "SELECT collection.collection_id, collection.name, collection.esri_open_data_id From collection LEFT JOIN template_type on collection.template_type_id = template_type.template_type_id WHERE template_type.template = 'outside-entity';"
    cur.execute(query)

    response = cur.fetchall()

    for r in response:
        esri_open_data_id = r[2]
        collection_id = r[0]
        if esri_open_data_id is not None:
            print(r)
            apiUrl = 'https://www.arcgis.com/sharing/rest/content/groups/%s?f=pjson' % esri_open_data_id
            print(apiUrl)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            http = urllib3.PoolManager()
            req = http.request('GET', apiUrl)
            data = json.loads(req.data)
            services = data['items']
            if len(services) > 0:
                cur.execute("DELETE FROM outside_entity_services WHERE collection_id = '%s'" % collection_id)
                for s in services:
                    title = s['title']
                    url = s['url']
                    if url is not None:
                        print(title)
                        cur.execute("INSERT INTO {table} ({id},{url},{col},{name}) VALUES ('{v1}','{v2}','{v3}','{v4}');".format(
                            table='outside_entity_services',
                            id='service_id',
                            url='service_url',
                            col='collection_id',
                            name='service_name',
                            v1=uuid.uuid4(),
                            v2=url,
                            v3=collection_id,
                            v4=title)
                        )
                        try:
                            conn.commit()
                        except:
                            print('bad!')

    cur.close()
    conn.close()
    print("that's all folks!!")

if __name__ == '__main__':
    lambda_handler(event='event', context='context')
