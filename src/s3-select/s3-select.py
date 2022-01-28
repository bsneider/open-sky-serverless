import json
import os

import boto3

S3_KEY = 'flightlist_20190101_20190131.csv.gz'
S3_BUCKET = 'fuck-shit-upppppp-lfggg-s3-select'
TARGET_FILE = 'flightlist_20190101_20190131.csv.gz'


session = boto3.Session(profile_name='iamadmin-production')
s3_client = session.client(service_name='s3')


def lambda_handler(event, context):

    #   - row_count: The number of rows in the RDS table for the dataset
    #   - last_transponder_seen_at: The maximum value for `lastseen` in the data
    #   - most_popular_destination: The most commonly seen value for `destination`
    #   - count_of_unique_transponders: a unique count of the `icao24` field

    # TO_TIMESTAMP(s.\"timestamp\", 'yMMdd''T''Hmmss.SSS''Z''')
    # transform_values(multimap_agg(unique_id, 1), (k, v) -> cardinality(v))
    query = """SELECT 
                count(*) as row_count
                ,MAX(CAST(lastseen AS TIMESTAMP)) as last_transponder_seen_at
                ,'' as most_popular_destination
                , COUNT(DISTINCT icao24)
            FROM S3Object"""

    # S3.Client.select_object_content
    # https: // boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    result = s3_client.select_object_content(Bucket=S3_BUCKET,
                                             Key=S3_KEY,
                                             ExpressionType='SQL',
                                             Expression=query,
                                             InputSerialization={
                                                 'CompressionType': 'GZIP',
                                                 'CSV': {'FileHeaderInfo': 'Use'}},
                                             OutputSerialization={'JSON': {}})
    print('here')
    print(json.dumps(result))
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
                filtered_file.write(res)


lambda_handler()
