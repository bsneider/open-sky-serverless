# Quick Start

- [Quick Start](#quick-start)
  - [TLDR](#tldr)
  - [Setup AWS CLI with name profile](#setup-aws-cli-with-name-profile)
  - [Clone repo](#clone-repo)
    - [ssh](#ssh)
    - [https](#https)
  - [Update locals with AWS Profile, and Region](#update-locals-with-aws-profile-and-region)
  - [Run terraform apply](#run-terraform-apply)
  - [Wait for data to load (15 mins)](#wait-for-data-to-load-15-mins)
  - [Query the report api](#query-the-report-api)

## TLDR

edit src/terraform/locals.tf with your aws profile

```sh
git clone git@github.com:bsneider/open-sky-serverless.git
cd open-sky-serverless
sh quick-start.sh 
```

## Setup AWS CLI with name profile

[https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)

The profile needs many permissions(rds-data, iam, s3, lambda, vpc, api gateway,... etc.). This could be substituted for AWS_ACCESS_KEY and AWS_SECRECT_ACCESS_KEY and SESSION_TOKEN.

## Clone repo

### ssh

`git clone git@github.com:bsneider/open-sky-serverless.git`

### https

`git clone https://github.com/bsneider/open-sky-serverless.git`

## Update locals with AWS Profile, and Region

```hcl
# /src/terraform/locals.tf

locals {
name = "example-\${replace(basename(path.cwd), "\_", "-")}"
region = "us-east-1"
profile = "change-me-to-your-profile"
}
```

## Run terraform apply

`terraform apply -auto-approve`

## Wait for data to load (15 mins)

can query the report api as the data loads. A point for increased performance would be sharding the extra large file and then having many lambdas editing at once

## Query the report api

`curl -X GET https://w9jjois4m3.execute-api.us-east-1.amazonaws.com/beta/report`

If first curl says timeout exception, not a problem, just run it again. The serverless aurora is just waking up. While the lambda has the ability to wait for the db to warm up, the api gw times out after 29 seconds. This could be bypassed in a production system.