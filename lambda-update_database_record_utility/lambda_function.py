# --------------- IMPORTS ---------------
import os, psycopg2

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
    table = event['table']
    field = event['field']
    value = event['value']
    try:
        where = event['where']
    except:
        print('No "where" key in event!!!')
        event['where'] = None
    # connect to database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    if isinstance(value, str):
        value = "'" + value + "'"

    q = "UPDATE %s SET %s = %s;" % (table, field, value)

    if event['where'] != None:
        q = q.replace(";", " WHERE %s;" % where)

    print(q)
    cur.execute(q)
    conn.commit()

    cur.close()
    conn.close()
    print("that's all folks!!")

if __name__ == '__main__':
    lambda_handler(event='event', context='context')
