#--- lambda_module/locals --- 

locals {
  api_gw_stage           = "beta"
  api_execute_report_arn = "${replace(aws_api_gateway_deployment.opensky-api-gateway-deployment.execution_arn, local.api_gw_stage, "*")}/*/report/"
}
