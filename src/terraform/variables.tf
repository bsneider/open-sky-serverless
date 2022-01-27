
locals {
  name   = "example-${replace(basename(path.cwd), "_", "-")}"
  region = "us-east-1"

}
