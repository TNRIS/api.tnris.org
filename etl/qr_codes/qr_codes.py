#
#
#
# FOR CREATING QR CODES FOR HISTORICAL COLLECTIONS
# THESE ARE USED ON THE PHYSICAL BOXES OF FRAMES IN THE PHOTO ROOM
#
#
#
#
#

import boto3
import os
import psycopg2
from urllib import request

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('', scope)

gc = gspread.authorize(credentials)


database = os.environ.get('DB_NAME')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

conn_string = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (database, username, host, password, port)

# connect to database
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# get all historical collections
q = """
SELECT historical_collection.id,
       historical_collection.to_date,
       agency.abbreviation
       FROM historical_collection
       LEFT JOIN agency ON agency.id=historical_collection.agency_id
"""
cur.execute(q)
res = cur.fetchall()
errors = []
counter = 0
for r in res:
    # build object for inserting into spreadsheet
    endpoint_url = "https://data.tnris.org/admin/lore/collection/%s/change/" % (r[0])
    google_api_url = "https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl=" + endpoint_url
    upload_key = "%s/assets/qr_code.png" % (r[0])
    qr_url = "https://s3.amazonaws.com/data.tnris.org/%s" % (upload_key)
    year = str(r[1].strftime("%Y"))
    agency = r[2]
    label = agency + " " + year
    qr_image = '=image("%s")' % (qr_url)
    dict = {
        'uuid': r[0],
        'endpoint_url': endpoint_url,
        'google_api_url': google_api_url,
        'qr_url': qr_url,
        'year': year,
        'agency': agency,
        'label': label,
        'qr_image': qr_image
    }
    # download image
    path = "/tmp/qr_code.png"
    request.urlretrieve(google_api_url, path)

    # upload to s3 Bucket
    s3 = boto3.resource('s3')
    s3.Bucket('data.tnris.org').upload_file(path, upload_key)

    # update database qr_code field
    cur.execute("UPDATE historical_collection SET qr_code_url = '{url}' WHERE id = '{col_id}';".format(
        url=qr_url,
        col_id=r[0])
    )
    try:
        conn.commit()
    except:
        errors.append(r)

    # add to google sheet
    wks = gc.open('qr_codes_historical_archive').sheet1
    new_row = [r[0], endpoint_url, google_api_url, qr_url, year, agency, label, qr_image]
    wks.append_row(new_row, value_input_option='USER_ENTERED')

    counter += 1
    print(counter, r[0])
print('historical collections: %s' % len(res))


#########

###########
cur.close()
conn.close()
print("ERRORS:--------------------------")
for e in errors:
    print(e)
print("that's all folks!!")
