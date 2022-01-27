output "mysql_cluster_master_password" {
  sensitive = true
  value     = module.rds.mysql_cluster_master_password
}

output "mysql_cluster_master_username" {
  sensitive = true
  value     = module.rds.mysql_cluster_master_username
}
