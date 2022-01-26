import boto3
import os

S3_KEY = 'taxi_2020-06.csv'
S3_BUCKET = 'playground-datasets'
TARGET_FILE = 'unknown_payment_type.csv'

s3_client = boto3.client(service_name='s3')


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
            FROM S3Object
"""

    result = s3_client.select_object_content(Bucket=S3_BUCKET,
                                             Key=S3_KEY,
                                             ExpressionType='SQL',
                                             Expression=query,
                                             InputSerialization={
                                                 'CSV': {'FileHeaderInfo': 'Use'}},
                                             OutputSerialization={'CSV': {}})

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
