import json
import os
import re

import boto3

S3_KEY = 'flightlist_20190101_20190131.csv.gz'
S3_BUCKET = 'fuck-shit-upppppp-lfggg-s3-select'
TARGET_FILE = './result.csv'


session = boto3.Session(profile_name='iamadmin-production')
s3_client = session.client(service_name='s3')


#   - row_count: The number of rows in the RDS table for the dataset
#   - last_transponder_seen_at: The maximum value for `lastseen` in the data
#   - most_popular_destination: The most commonly seen value for `destination`
#   - count_of_unique_transponders: a unique count of the `icao24` field

# TO_TIMESTAMP(s.\"timestamp\", 'yMMdd''T''Hmmss.SSS''Z''') 2019-01-15 14:36:25+00:00
# transform_values(multimap_agg(unique_id, 1), (k, v) -> cardinality(v))
query = """SELECT 
            count(*)
            ,MAX(TO_TIMESTAMP(lastseen, 'y-MM-dd H:mm:ssXXX'))
            ,'' as most_popular_destination
            , COUNT(DISTINCT icao24) as 1
        FROM S3Object"""

# S3.Client.select_object_content
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.select_object_content
result = s3_client.select_object_content(Bucket=S3_BUCKET,
                                         Key=S3_KEY,
                                         ExpressionType='SQL',
                                         Expression="SELECT CAST(TO_TIMESTAMP(lastseen, 'y-MM-dd H:mm:ssXXX') as int) from S3Object limit 3",
                                         RequestProgress={
                                             'Enabled': True
                                         },
                                         InputSerialization={
                                             'CSV': {
                                                 'FileHeaderInfo': 'USE',
                                             },
                                             'CompressionType': 'GZIP',
                                         },
                                         OutputSerialization={
                                             'JSON': {
                                                 'RecordDelimiter': ','
                                             }
                                         })
print('here')
print(result)
# print(json.dumps(result['Payload']))
# remove the file if exists, since we append filtered rows line by line
if os.path.exists(TARGET_FILE):
    os.remove(TARGET_FILE)

with open(TARGET_FILE, 'a+') as filtered_file:
    # write header as a first line, then append each row from S3 select
    filtered_file.write(
        'ID,pickup,dropoff,passenger_count,distance,tip,total\n')
    for record in result['Payload']:
        if 'Records' in record:
            res = record['Records']['Payload'].decode('utf-8')
            print(res)
            filtered_file.write(res)
