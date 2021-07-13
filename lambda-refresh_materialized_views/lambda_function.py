# --------------- IMPORTS ---------------
import os, psycopg2, time

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

    if 'materialized_view' in event.keys():
        if((type(event['materialized_view']) is list) or (type(event['materialized_view']) is tuple)):
            for view in event['materialized_view']:
                query = "REFRESH MATERIALIZED VIEW %s with DATA;" % (view)
                print(query)
                cur.execute(query)
                conn.commit()
        else:
            print('waiting 15 seconds to ensure database saves are complete...')
            time.sleep(15)
            query = "REFRESH MATERIALIZED VIEW %s with DATA;" % (event['materialized_view'])
            print(query)
            cur.execute(query)
            conn.commit()
    else:
        queries = [
            "REFRESH MATERIALIZED VIEW collection_catalog_record with DATA;",
            "REFRESH MATERIALIZED VIEW compiled_historical_collection with DATA;",
            "REFRESH MATERIALIZED VIEW areas with DATA;",
            "REFRESH MATERIALIZED VIEW resource_management with DATA;",
            "REFRESH MATERIALIZED VIEW master_systems_display with DATA;"
            "REFRESH MATERIALIZED VIEW catalog_collection_meta with DATA;"
        ]

        for q in queries:
            print(q)
            cur.execute(q)
            conn.commit()

    cur.close()
    conn.close()
    print("that's all folks!!")

if __name__ == '__main__':
    lambda_handler(event='event', context='context')
