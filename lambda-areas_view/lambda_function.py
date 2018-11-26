# --------------- IMPORTS ---------------
import urllib3
import json
import csv
import boto3
import os

# --------------- Main handler ------------------

def lambda_handler(event, context):
    print(event)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    url = 'https://data.tnris.org/api/v1/areas'
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

    # write the records to a csv
    print('writing csv')
    fieldnames = results[0].keys()
    print('Fieldnames: ', fieldnames)
    count = 0
    temp_csv = '/tmp/areas_view.csv'
    with open(temp_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
            count += 1
    print("%s rows written." % str(count))

    # upload the csv to s3
    print('uploading to s3')
    client = boto3.client('s3')
    client.upload_file(temp_csv, 'data.tnris.org', 'areas_view.csv', ExtraArgs={'ACL':'public-read'})

    # delete the local csv
    print('removing local csv file')
    os.remove(temp_csv)


    print("that's all folks!!")

if __name__ == '__main__':
    lambda_handler(event='event', context='context')
