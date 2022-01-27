terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.63"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region  = "us-east-1"
  profile = "iamadmin-production"
  default_tags {
    tags = {
      Owner       = "user"
      Environment = "dev"
    }
  }
}
