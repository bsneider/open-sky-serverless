################################################################################
# Supporting Resources
################################################################################

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = local.name
  cidr = "10.99.0.0/18"

  azs              = ["${local.region}a", "${local.region}b", "${local.region}c"]
  public_subnets   = ["10.99.0.0/24", "10.99.1.0/24", "10.99.2.0/24"]
  private_subnets  = ["10.99.3.0/24", "10.99.4.0/24", "10.99.5.0/24"]
  database_subnets = ["10.99.7.0/24", "10.99.8.0/24", "10.99.9.0/24"]
}

module "s3" {
  source           = "./modules/s3"
  load_lambda_arn  = module.lambda.load_invoke_arn
  load_lambda_name = module.lambda.load_name
}

module "rds" {
  source                      = "./modules/rds"
  name                        = local.name
  vpc_id                      = module.vpc.vpc_id
  database_subnets            = module.vpc.database_subnets
  private_subnets_cidr_blocks = module.vpc.private_subnets_cidr_blocks
}

module "lambda" {
  source            = "./modules/lambda"
  api_gw_source_arn = module.api_gw.api_gw_source_arn
  db_arn            = module.rds.mysql_cluster_arn
  s3_arn            = module.s3.s3_arn
  rds_creds_arn     = module.rds.db_credentials_secret_arn
  bucket_name       = module.s3.bucket_name
  file_name         = "flightlist_20190101_20190131.csv.gz"
}

module "api_gw" {
  source            = "./modules/api_gw"
  scrape_invoke_arn = module.lambda.scrape_invoke_arn
  load_invoke_arn   = module.lambda.load_invoke_arn
  report_invoke_arn = module.lambda.report_invoke_arn
  scrape_name       = module.lambda.scrape_name
  load_name         = module.lambda.load_name
  report_name       = module.lambda.report_name
}
