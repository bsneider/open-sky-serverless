resource "aws_api_gateway_rest_api" "opensky-api-gateway" {
  name        = "OpenSkyAPI"
  description = "API to CRUD opensky events"
  body        = data.template_file.swagger.rendered
}

data "template_file" "swagger" {
  template = file("${path.module}/swagger_file.yaml")
  vars = {
    region            = data.aws_region.current.name
    scrape_invoke_arn = var.scrape_invoke_arn
    etl_invoke_arn    = var.etl_invoke_arn
    report_invoke_arn = var.report_invoke_arn
  }
}

resource "aws_api_gateway_deployment" "opensky-api-gateway-deployment" {
  rest_api_id = aws_api_gateway_rest_api.opensky-api-gateway.id
  stage_name  = local.api_gw_stage
}

# # Lambda
resource "aws_lambda_permission" "apigw_lambda_report" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.report_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = local.api_execute_report_arn
  #  "arn:aws:execute-api:${var.myregion}:${var.accountId}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method.http_method}${aws_api_gateway_resource.resource.path}"
}
# arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:909067940010:function:report/invocations
