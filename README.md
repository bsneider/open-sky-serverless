# open-sky-serverless

- [open-sky-serverless](#open-sky-serverless)
  - [Assignment - Terraform AWS Deployment](#assignment---terraform-aws-deployment)
    - [Research / Architecture Decisions](#research--architecture-decisions)
    - [Prerequisite](#prerequisite)
    - [Requirements](#requirements)
    - [Deliverable](#deliverable)
    - [Gift Card](#gift-card)

## Assignment - Terraform AWS Deployment

### Research / Architecture Decisions

[Research/Architecture Decisions](/docs/research.md)

---

### Prerequisite

- An active AWS Account (Free Tier is sufficient)
- Terraform CLI
- AWS CLI

### Requirements

You are tasked to create a Terraform manifest that will deploy infrastructure to AWS for a simple data based microservice. The Terraform configuration should create an RDS database, S3 bucket, Lambda function and any other necessary infrastructure components. The microservice will pull a sample dataset from a file stored in S3 to RDS and provide an API to view the data.

It is recommended to use [this dataset from the OpenSky Network](https://zenodo.org/record/5377831) but any dataset may be used.

- Create a Terraform manifest that will provision an RDS database, S3 bucket, Lambda microservice and any other required components for access.
- Write a Lambda microservice in your preferred language that consumes any files uploaded to a designated S3 bucket and ingests them into an RDS database.
- Write a Lambda API endpoint that provides a JSON summary of the data, including how many rows are ingested and other useful metrics. If the provided dataset is used, these metrics could look like:
  - row_count: The number of rows in the RDS table for the dataset
  - last_transponder_seen_at: The maximum value for `lastseen` in the data
  - most_popular_destination: The most commonly seen value for `destination`
  - count_of_unique_transponders: a unique count of the `icao24` field
- Write a basic shell script that uses the Terraform & AWS CLIs to initialize, provision and deploy these resources. It should also handle uploading the chosen dataset to S3 after completion. The script should be something simple enough to include within CICD execution block (ex: a `.gitlab-ci.yml` “script” block).

### Deliverable

- The repo should have a good README explanation for us to get the project running on our own AWS account and review the Tasks.
- We will run the project using the startup script provided. Everything should be deployed with this one command or otherwise be explained in the README.
- Instructions on how to access the summary API once it has been deployed.
- A GitHub repo with read permissions given to GitHub users `rafty8s`, `omnipresent07`, and `potto007` ([how to invite collaborators](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository#inviting-a-team-or-person))

### Gift Card

Our sincere hope is for you to complete this tech challenge and embark upon a journey with Raft to help the change how Big Data is handled today in the DoD. But we understand that it is not ok to demand free work during the interview process. As a result of this tech challenge you will be provided a \$200 Amazon Gift card regardless of whether you accept the offer.
