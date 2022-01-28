# /src/terraform/locals.tf
locals {
  name    = "example-${replace(basename(path.cwd), "_", "-")}"
  region  = "us-east-1"
  profile = "iamadmin-production"
}
