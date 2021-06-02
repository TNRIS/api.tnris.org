# --------------- IMPORTS ---------------
import urllib3, json, psycopg2, os

# Database Connection Info
database = os.environ.get('MAPSERVER_DB_NAME')
username = os.environ.get('MAPSERVER_DB_USER')
password = os.environ.get('MAPSERVER_DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

# --------------- Main handler ------------------

def lambda_handler(event, context):
    print(event)
    # """
    # Use the /areas TNRIS api endpoint to grab the latest resource-to-area-type
    # relationships for collections and update the mapserver rds table: areas_view
    # """
    conn = psycopg2.connect(dbname=database, user=username, password=password, host=host, port=port)
    cur = conn.cursor()

    try:
        # setup api url
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
        url = 'https://api.tnris.org/api/v1/areas'
        results = []

        # iteratively go get all records from the API
        def go_getter(url):
            r = http.request('GET', url)
            data = json.loads(r.data)
            results.extend(data['results'])
            print(len(results))
            if data['next'] is not None:
                go_getter(data['next'])
            else:
                return

        print('getting records from api')
        go_getter(url)

        # iterate API response and update database table
        print('updating database table')
        counter = 1
        for r in results:
            print(counter, 'of', len(results), ':::', r['area_type_id'], r['area_type_name'], r['area_type'])
            # check to see if this is a new or existing record
            check_query = "select area_type_id from areas_view where area_type_id = '%s' limit 1;" % (r['area_type_id'])
            cur.execute(check_query)
            res = cur.fetchone()

            # replace None values
            for k in r.keys():
                if r[k] is None:
                    r[k] = ''
                if "'" in r[k]:
                    print('replacing single quote', r[k], r[k].replace("'", "''"))
                    r[k] = r[k].replace("'", "''")
            
            # if record exists, we'll do an update query
            if res is not None:
                update_query = (
                    """UPDATE areas_view
                    SET area_type_name='%s', area_type='%s', download='%s', historical='%s',
                    outside_entity='%s', "order"='%s', collections='%s'
                    WHERE area_type_id = '%s';""" % (
                        r['area_type_name'], r['area_type'], r['download'], r['historical'],
                        r['outside_entity'], r['order'], r['collections'], r['area_type_id']
                    )
                )
                # print(update_query)
                cur.execute(update_query)
                conn.commit()
            # if record doesn't exist, we'll do an insert query
            else:
                print('%s is new. adding...' % (r['area_type_id']))
                insert_query = (
                    """INSERT INTO areas_view
                    (area_type_name, area_type, download, historical,
                    outside_entity, "order", collections, area_type_id)
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
                    """ % (
                        r['area_type_name'], r['area_type'], r['download'], r['historical'],
                        r['outside_entity'], r['order'], r['collections'], r['area_type_id']
                    )
                )
                # print(insert_query)
                cur.execute(insert_query)
                conn.commit()
            counter += 1

    except Exception as e:
        print('ERROR:', e)

    # refresh the materialized view to present the data updates
    print('refreshing the materialized view: "download_areas"')
    refresh_query = "REFRESH MATERIALIZED VIEW download_areas with DATA;"
    cur.execute(refresh_query)
    conn.commit()

    print('closing database connection.')
    conn.close()
    
    print("that's all folks!!")
    return

if __name__ == '__main__':
    lambda_handler(event='event', context='context')
