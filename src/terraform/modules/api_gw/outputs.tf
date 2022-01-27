# aws_db_subnet_group
output "api_gw_source_arn" {
  description = "The /*/* portion grants access from any method on any resource"
  value       = "${replace(aws_api_gateway_deployment.opensky-api-gateway-deployment.execution_arn, local.api_gw_stage, "*")}/*/events/*"
}
