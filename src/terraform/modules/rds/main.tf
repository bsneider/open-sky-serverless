################################################################################
# RDS Aurora Module - MySQL
################################################################################

module "aurora_mysql" {
  source = "terraform-aws-modules/rds-aurora/aws"


  name              = "${var.name}-mysql"
  engine            = "aurora-mysql"
  engine_mode       = "serverless"
  storage_encrypted = true

  vpc_id                = var.vpc_id
  subnets               = var.database_subnets
  create_security_group = true
  allowed_cidr_blocks   = var.private_subnets_cidr_blocks

  monitoring_interval = 60

  apply_immediately   = true
  skip_final_snapshot = true

  db_parameter_group_name         = aws_db_parameter_group.example_mysql.id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.example_mysql.id
  # enabled_cloudwatch_logs_exports = # NOT SUPPORTED

  scaling_configuration = {
    auto_pause               = true
    min_capacity             = 2
    max_capacity             = 16
    seconds_until_auto_pause = 300
    timeout_action           = "ForceApplyCapacityChange"
  }
}

resource "aws_db_parameter_group" "example_mysql" {
  name        = "${var.name}-aurora-db-mysql-parameter-group"
  family      = "aurora-mysql5.7"
  description = "${var.name}-aurora-db-mysql-parameter-group"
}

resource "aws_rds_cluster_parameter_group" "example_mysql" {
  name        = "${var.name}-aurora-mysql-cluster-parameter-group"
  family      = "aurora-mysql5.7"
  description = "${var.name}-aurora-mysql-cluster-parameter-group"
}
