

import time

import boto3

# Update these 3 parameters for your environment
database_name = 'example-terraform-mysql'
db_cluster_arn = 'example-terraform-mysql.cluster-c5fwgo4gpfdq.us-east-1.rds.amazonaws.com'
db_credentials_secrets_store_arn = 'arn:aws:secretsmanager:us-east-1:123456789012:secret:dev-AuroraUserSecret-DhpkOI'

# This is the Data API client that will be used in our examples below
rds_client = boto3.client('rds-data')

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
    sql = 'insert into package (package_name, package_version) values (:package_name, :package_version)'
    sql_parameters = [
        {'name': 'package_name', 'value': {'stringValue': f'package-2'}},
        {'name': 'package_version', 'value': {'stringValue': 'version-1'}}
    ]
    response = execute_statement(sql, sql_parameters)
    print(
        f'Number of records updated: {response["numberOfRecordsUpdated"]}')
except Exception as e:
    print(e)
