# --------------- IMPORTS ---------------
import boto3
import re

log_bucket = os.environ.get('log_bucket')
dynamodb_table = os.environ.get('dynamodb_table')

# --------------- Main handler ------------------

def lambda_handler(event, context):
    print(event)
    logfile = event['Records'][0]['s3']['object']['key']
    print(logfile)
    # set aside variables of parsed fields for each logfile line
    s3_log_format = r'(\S+) (\S+) \[(.*?)\] (\S+) (\S+) (\S+) (\S+) (\S+) "([^"]+)" (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) "([^"]+)" "([^"]+)"';
    s3_log_format = re.compile(s3_log_format)
    s3_names = ["bucket_owner", "bucket", "datetime", "ip", "requestor_id", "request_id", "operation", "key", "http_method_uri_proto", "http_status", "s3_error", "bytes_sent", "object_size", "total_time", "turn_around_time", "referer", "user_agent"]
    # configure direction to dynamodb table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table)
    with table.batch_writer() as batch:
        # get the logfile (which caused the event) out of s3
        s3 = boto3.resource('s3')
        obj = s3.Object(log_bucket, logfile)
        # read the logfile contents and break into lines
        content = obj.get()['Body'].read()
        lines = content.splitlines()
        counter = 1
        for l in lines:
            match = s3_log_format.match(l.decode('utf-8'))
            if match is not None:
                # turn parsed line into dictionary and create id for it
                tmp = [match.group(n + 1) for n in range(17)]
                result = zip(s3_names, tmp)
                line_obj = dict(result)
                line_obj['DownloadId'] = logfile.replace('data.tnris.org/', '') + "-Line" + str(counter)
                # split the downloaded files' key to dismantle details
                try:
                    splitten = line_obj['key'].split('/')
                    line_obj['collection_id'] = splitten[0]
                    line_obj['download_type'] = splitten[1]
                    line_obj['filename'] = splitten[2]
                    # if a dataset download, use filename to split out more details
                    if line_obj['download_type'] == 'resources':
                        line_obj['collection_shorthand'] = filename.replace('.zip', '').split("_")[0]
                        line_obj['area_code'] = filename.replace('.zip', '').split("_")[1]
                        line_obj['resource_type'] = filename.replace('.zip', '').split("_")[2]
                        print(line_obj['key'])
                        batch.put_item(Item=line_obj)
                        counter += 1
                    # if a supplemental download, use filename to split out more details
                    if line_obj['download_type'] == 'assets' and '.zip' in line_obj['filename']:
                        if 'supplemental-report' in line_obj['filename']:
                            line_obj['supplemental_download'] = 'supplemental-report'
                        elif 'lidar-breaklines' in line_obj['filename']:
                            line_obj['supplemental_download'] = 'lidar-breaklines'
                        elif 'tile-index' in line_obj['filename']:
                            line_obj['supplemental_download'] = 'tile-index'
                        print(line_obj['key'])
                        batch.put_item(Item=line_obj)
                        counter += 1
                except Exception as e:
                    print('ERROR!')
                    print(e)
    print("that's all folks!!")

if __name__ == '__main__':
    lambda_handler(event='event', context='context')
