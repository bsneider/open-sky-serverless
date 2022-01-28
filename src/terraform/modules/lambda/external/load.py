

import gzip
import json
import time

import boto3
from botocore.exceptions import ClientError

# Update these 3 parameters for your environment
database_name = 'flight'
db_cluster_arn = "${db_cluster_arn}"
db_credentials_secrets_store_arn = "${rds_creds_arn}"
# This is the Data API client that will be used in our examples below
session = boto3.Session(region_name='us-east-1')
rds_client = session.client(service_name='rds-data')
s3 = session.resource('s3')
bucket = "${bucket_name}"
# --------------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------------

# https://stackoverflow.com/questions/58192747/aws-aurora-serverless-communication-link-failure


def _wait_for_serverless():
    delay = 5
    max_attempts = 10

    attempt = 0
    while attempt < max_attempts:
        attempt += 1

        try:
            execute_statement('SELECT 1')
            return
        except ClientError as ce:
            error_code = ce.response.get("Error").get('Code')
            error_msg = ce.response.get("Error").get('Message')

            # Aurora serverless is waking up
            if error_code == 'BadRequestException' and 'Communications link failure' in error_msg:
                print('Sleeping ' + str(delay) +
                      ' secs, waiting RDS connection')
                time.sleep(delay)
            else:
                raise ce

    raise Exception('Waited for RDS Data but still getting error')
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


sql_script_content = '''CREATE TABLE IF NOT EXISTS flightlist(
pk BIGINT NOT NULL AUTO_INCREMENT
,callsign     VARCHAR(30)
,number       VARCHAR(30)
,icao24       VARCHAR(6)
,registration VARCHAR(15)
,typecode     VARCHAR(20)
,origin       VARCHAR(8)
,destination  VARCHAR(15)
,firstseen    varchar(26)
,lastseen     varchar(26)
,day          varchar(26)
,latitude_1   VARCHAR(30) 
,longitude_1  VARCHAR(30) 
,altitude_1   VARCHAR(30) 
,latitude_2   VARCHAR(30) 
,longitude_2  VARCHAR(30) 
,altitude_2   VARCHAR(30)
,PRIMARY KEY (pk)
);'''


def create_table():
    print('creating table if not exists')

    response = execute_statement(sql_script_content)
    print(json.dumps(response))
    print(
        f'Number of records updated: {response["numberOfRecordsUpdated"]}')


def lambda_handler(event, context):
    _wait_for_serverless()
    create_table()
    print('# 1 read file')
    try:
        name = event['Records'][0]['s3']['object']['key']
        obj = s3.Object(bucket, name).get()['Body']
    except Exception as e:
        print(e)

    # 1 read file
    row_count = 0
    # insert_start = 'INSERT INTO flightlist(callsign,number,icao24,registration,typecode,origin,destination,firstseen,lastseen,day,latitude_1,longitude_1,altitude_1,latitude_2,longitude_2,altitude_2) values'
    insert_start = 'INSERT INTO flightlist(icao24,destination,lastseen) values'
    insert_stmt = ''
    max_insert_len = 65536
    with gzip.open(obj, 'rt') as f:
        for row in f:
            if row_count == 0:
                row_count += 1
                continue
            if insert_stmt == '':
                insert_stmt = insert_start
            row = row.split(',')
            indices = [2, 6, 8]
            needed_cols = [row[val] for val in indices]
            data = "','".join(needed_cols)
            insert_len = len(insert_stmt)
            next_line = f"('{data}'),"
            if insert_len + len(next_line) >= max_insert_len:
                try:
                    insert_stmt = insert_stmt.rstrip(',')
                    execute_statement(insert_stmt)
                except Exception as e:
                    print(f'exception {e}')
                    break
                finally:
                    print('next batch')
                    insert_stmt = insert_start

            insert_stmt = insert_stmt + next_line
        # don't forget the last batch
        insert_stmt = insert_stmt.rstrip(',')
        execute_statement(insert_stmt)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "load complete"
    }
