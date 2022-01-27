

import json
import os
import sys
import time

import boto3

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

# Create the DB Schema (here just table package)


@timeit
def example_create_table():
    print('===== Example - create schema from DDL file =====')
    execute_statement(f'create database if not exists {database_name}')
    table_ddl_script_file = 'table_package.txt'
    print(f"Creating table from DDL file: {table_ddl_script_file}")
    with open(table_ddl_script_file, 'r') as ddl_script:
        ddl_script_content = ddl_script.read()
        execute_statement(ddl_script_content)
    # populate table w/ some data for querying
    execute_statement('delete from package')
    for i in range(100, 110):
        execute_statement(
            f'insert into package (package_name, package_version) values ("package-{i}", "version-1")')
        execute_statement(
            f'insert into package (package_name, package_version) values ("package-{i}", "version-2")')


try:
    with open(os.path.join(sys.path[0], 'create_table.sql'), 'r') as sql_script:
        sql_script_content = sql_script.read()
        response = execute_statement(sql_script_content)
        print(json.dumps(response))
        print(
            f'Number of records updated: {response["numberOfRecordsUpdated"]}')
    with open(os.path.join(sys.path[0], 'insert_sample.sql'), 'r') as sql_script:
        sql_script_content = sql_script.read()
        response = execute_statement(sql_script_content)
        print(json.dumps(response))
        print(
            f'Number of records updated: {response["numberOfRecordsUpdated"]}')
except Exception as e:
    print(e)
