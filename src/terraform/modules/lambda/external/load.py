

import gzip
import json
import os
import sys
import time

import boto3
from botocore.exceptions import NoCredentialsError
from botocore.vendored import requests

# Update these 3 parameters for your environment
database_name = 'flight'
db_cluster_arn = 'arn:aws:rds:us-east-1:909067940010:cluster:example-terraform-mysql'
db_credentials_secrets_store_arn = 'arn:aws:secretsmanager:us-east-1:909067940010:secret:rds_creds-DTfeZs'

# This is the Data API client that will be used in our examples below
session = boto3.Session(
    profile_name='iamadmin-production', region_name='us-east-1')
rds_client = session.client(service_name='rds-data')

# --------------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------------

# Timing function executions


def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print(f'Function: {f.__name__}')
        print(f'*  args: {args}')
        print(f'*  kw: {kw}')
        print(f'*  execution time: {(te-ts)*1000:8.2f} ms')
        return result
    return timed


@timeit
def execute_statement(sql, sql_parameters=[]):
    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_store_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=sql,
        parameters=sql_parameters
    )
    return response


# https://aws.amazon.com/blogs/database/using-the-data-api-to-interact-with-an-amazon-aurora-serverless-mysql-database/
# Source https://erangad.medium.com/upload-a-remote-image-to-s3-without-saving-it-first-with-python-def9c6ee1140
# https://stackoverflow.com/questions/40741282/cannot-use-requests-module-on-aws-lambda
# https://docs.aws.amazon.com/cli/latest/reference/rds-data/execute-statement.html

def lambda_handler(event, context):
    create_table()
    print('# 1 read file')
    # 1 read file
    row_count = 0
    count = 0
    batch_size = 300
    insert_start = 'INSERT INTO flightlist(callsign,number,icao24,registration,typecode,origin,destination,firstseen,lastseen,day,latitude_1,longitude_1,altitude_1,latitude_2,longitude_2,altitude_2) values'
    insert_stmt = ''
    with gzip.open(os.path.join(sys.path[0], "flightlist_20190101_20190131.csv.gz"), 'rb') as f:
        for row in f:
            if row_count == 0:
                row_count += 1
                continue
            count += 1
            if insert_stmt == '':
                insert_stmt = insert_start
            if count >= batch_size:
                try:
                    insert_stmt = insert_stmt.rstrip(',')
                    execute_statement(insert_stmt)
                except Exception as e:
                    print(f'exception {e}')
                    break
                finally:
                    print('next batch')
                    count = 0
                    insert_stmt = insert_start
            row = row.decode().rstrip().replace(
                '+00:00', '').replace(',', "','")
            insert_stmt = insert_stmt + f"('{row}'),"


# def prepare_row(row, header):
#     # INSERT INTO flightlist(callsign,number,icao24,registration,typecode,origin,destination,firstseen,lastseen,day,latitude_1,longitude_1,altitude_1,latitude_2,longitude_2,altitude_2) VALUES ('HVN19',NULL,'888152',NULL,NULL,'YMML','LFPG',STR_TO_DATE('2018-12-31 00:43:16+00:00','%Y-%m-%d %H:%i:%s+%TZ'),STR_TO_DATE('2019-01-01 04:56:29+00:00','%Y-%m-%d %H:%i:%s+%TZ'),STR_TO_DATE('2019-01-01 00:00:00+00:00','%Y-%m-%d %H:%i:%s+%TZ'),'-37.65948486328130','144.80442128282900',304.8,'48.99531555175780','2.610802283653850','-53.34');
#     # sql = 'insert into package (package_name, package_version) values (:package_name, :package_version)'
#     datetime_fields = ['firstseen', 'lastseen', 'day']
#     entry = []
#     for i, item in enumerate(row.split(',')):
#         col_name = header[i]
#         if col_name in datetime_fields:
#             item = item.split('+')[0]
#         e = {'name': f'{col_name}', 'value': {
#                      'stringValue': f'{item}'}}
#         entry.append(e)
#     return entry


def create_table():
    with open(os.path.join(sys.path[0], 'create_table.sql'), 'r') as sql_script:
        sql_script_content = sql_script.read()
        response = execute_statement(sql_script_content)
        print(json.dumps(response))
        print(
            f'Number of records updated: {response["numberOfRecordsUpdated"]}')


try:

    print('start')
    lambda_handler(None, None)
    print('finish')
    # with open(os.path.join(sys.path[0], 'insert_sample.sql'), 'r') as sql_script:
    #     sql_script_content = sql_script.read()
    #     response = execute_statement(sql_script_content)
    #     print(json.dumps(response))
    #     print(
    #         f'Number of records updated: {response["numberOfRecordsUpdated"]}')
except Exception as e:
    print(e)
