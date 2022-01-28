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
  region  = local.region
  profile = local.profile
  default_tags {
    tags = {
      Owner       = "user"
      Environment = "dev"
    }
  }
}
