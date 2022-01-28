# Quick Start

- [Quick Start](#quick-start)
  - [Update terraform.tfvars with profile of console](#update-terraformtfvars-with-profile-of-console)
  - [Run terraform apply](#run-terraform-apply)
  - [Wait for data to load (15 mins)](#wait-for-data-to-load-15-mins)
  - [Query the report api](#query-the-report-api)

## Update terraform.tfvars with profile of console

Update terraform.tfvars #TODO with profile so can run. Need perms for rds-data, iam, s3, lambda, vpc, and api gateway

## Run terraform apply

`terraform apply -auto-approve`

## Wait for data to load (15 mins)

can query the report api as the data loads. A point for increased performance would be sharding the extra large file and then having many lambdas editing at once

## Query the report api

`curl -X GET https://w9jjois4m3.execute-api.us-east-1.amazonaws.com/beta/report`

If first curl says timeout exception, not a problem, just run it again. The serverless aurora is just waking up. While the lambda has the ability to wait for the db to warm up, the api gw times out after 29 seconds. This could be bypassed in a production system.