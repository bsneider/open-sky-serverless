import json
import time

import boto3
from botocore.exceptions import ClientError

destination_sql = '''select destination
from flight.flightlist 
where destination is not null and destination<>''
group by destination
order by COUNT(destination) desc
Limit 1;'''

row_count_sql = '''SELECT Count(1) FROM flight.flightlist'''

max_lastseen_sql = '''SELECT STR_TO_DATE(lastseen, '%Y-%m-%d %H:%i:%s+%TZ') AS max_lastseen 
from flight.flightlist order by 1 desc limit 1;'''

unique_icao24 = '''select count(distinct icao24) from flight.flightlist'''

database_name = 'flight'
db_cluster_arn = "${db_cluster_arn}"
db_credentials_secrets_store_arn = "${rds_creds_arn}"
region_name = "${region_name}"
# This is the Data API client that will be used in our examples below
session = boto3.Session(region_name=region_name)
rds_client = session.client(service_name='rds-data')


def execute_statement(sql, sql_parameters=[]):
    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_store_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=sql,
        parameters=sql_parameters
    )
    return response


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


def lambda_handler(event, context):
    _wait_for_serverless()
    row_count = list(execute_statement(row_count_sql)
                     ['records'][0][0].values())[0]
    lastseen = list(execute_statement(max_lastseen_sql)
                    ['records'][0][0].values())[0]
    dest = list(execute_statement(destination_sql)
                ['records'][0][0].values())[0]
    uniq_transponders = list(execute_statement(unique_icao24)[
                             'records'][0][0].values())[0]
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "row_count ": str(row_count),
            "last_transponder_seen_at": lastseen,
            "most_popular_destination": dest,
            "count_of_unique_transponders": str(uniq_transponders)
        })
    }
