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
