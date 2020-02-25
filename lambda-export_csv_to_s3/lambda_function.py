# --------------- IMPORTS ---------------
import io, os, sys, psycopg2
import boto3
import datetime, csv

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

    # s3 variables
    s3 = boto3.client('s3')
    bucket = 'tnris-public-data'
    sub = 'api.tnris.org/lore-csv-export/'
    resp = s3.list_objects(Bucket=bucket)

    ##################################################################################
    # this part of the lambda checks if more than 16 files are in the bucket object
    # and deletes the oldest file(s) every time it goes to add a new one to make sure
    # no more than 16 files (4 months) are saved at any time.
    file_list = []
    delete_list = []
    # change num variable below to be the number of files you want to keep in s3
    num = 2

    for obj in resp['Contents']:
        if sub in obj['Key']:
            k = obj['Key']
            if k.split('/')[-1] != '':
                name = k.split('/')[-1]
                file_list.append(name)
                if len(file_list) > num:
                    # sort to make sure oldest items are first in list (due to file name)
                    file_list.sort()
                    # catch possibility of more than one over the num limit
                    diff = len(file_list) - num
                    delete_list = file_list[:diff]

    # delete file(s) from s3
    # for d in delete_list:
    #     dkey = sub + d
    #     response = s3.delete_object(
    #         Bucket=bucket,
    #         Key=dkey,
    #     )

    print('DELETED: {}'.format(delete_list))

    ##################################################################################
    # this section of the lambda function will grab the current data from the
    # compiled_historical_collection view in the database and copy it to a csv and
    # save it in s3 object with key 'api.tnris.org/lore-csv-export/' + file name

    # connect to database
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # variables
    db_view = 'compiled_historical_collection'
    x = datetime.datetime.now()
    file = x.strftime('%Y%m%d') + '_compiled_historical_collection.csv'

    print(file)

    # use postgres copy function to grab db_view and delimit with comma, include header info
    sql = "COPY (SELECT * FROM %s) TO STDOUT WITH CSV DELIMITER ',' HEADER;" % (db_view)

    print(sql)

    # write sql to .csv file
    with open('/home/john/Desktop/' + file, 'w') as csv_file:
        # the_writer = csv.writer(csv_file)
        cur.copy_expert(sql, csv_file)
        # resource.Object(bucket, csv_file).put(Body=the_file.getvalue())

    # file = str(file)
    # cur.copy_expert(sql, file)
    # resource.Object(bucket, file).put(Body=file.getvalue())

    # boto stuff
    # response = self.client.put_object(
    #     Bucket='tnris-public-data',
    #     ACL='public-read',
    #     ContentType='text/csv',
    #     Key=key,
    #     Body=file
    # )

    # completed
    print("goodbye :-}")

if __name__ == '__main__':
    lambda_handler(event='event', context='context')
