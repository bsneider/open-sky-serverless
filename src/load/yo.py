import gzip
import json
from uuid import uuid4
import boto3
import os
import csv
import sys

session = boto3.Session(
    profile_name='iamadmin-production', region_name='us-east-1')
s3 = session.resource('s3')
dynamodb = session.resource('dynamodb')

bucket = 'open-sky-raft-galore-easter-egg-20220127121428936900000004'
key = 'flightlist_20190101_20190131.csv.gz' #os.environ['key']
tableName = 'ttt' #os.environ['table']

# bucket = os.environ['bucket']
# key = os.environ['key']
# tableName = os.environ['table']

def lambda_handler(event, context):


   #get() does not store in memory
   try:
       obj = s3.Object(bucket, key).get()['Body']
   except:
       print("S3 Object could not be opened. Check environment variable. ")
   try:
       table = dynamodb.Table(tableName)
   except:
       print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   batch_size = 10000
   batch = []

   #DictReader is a generator; not stored in memory
   with gzip.open(obj, 'rt') as f:
      for row in csv.DictReader(f):
         row['test'] = str(uuid4())
         if len(batch) >= batch_size:
            write_to_dynamo(batch)
            batch.clear()
         batch.append(row)

      if batch:
         write_to_dynamo(batch)

   return {
      'statusCode': 200,
      'body': json.dumps('Uploaded to DynamoDB Table')
   }


def write_to_dynamo(rows):
   try:
      table = dynamodb.Table(tableName)
   except:
      print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   try:
      with table.batch_writer() as batch:
         for i in range(len(rows)):
            batch.put_item(
               Item=rows[i]
            )
   except Exception as e:
      print(e)
      print("Error executing batch_writer")

lambda_handler(None, None)