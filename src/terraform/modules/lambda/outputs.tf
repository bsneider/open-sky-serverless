output "scrape_invoke_arn" {
  description = "arn of lambda to take csv.gz and move it to s3"
  value       = aws_lambda_function.scrape.invoke_arn
}

output "etl_invoke_arn" {
  description = "arn of lambda to take csv.gz from s3 and load it to db"
  value       = aws_lambda_function.etl.invoke_arn
}

output "report_invoke_arn" {
  description = "arn of lambda that returns results of the report"
  value       = aws_lambda_function.report.invoke_arn
}
