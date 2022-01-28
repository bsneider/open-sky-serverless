output "scrape_invoke_arn" {
  description = "arn of lambda to take csv.gz and move it to s3"
  value       = aws_lambda_function.scrape.invoke_arn
}

output "scrape_name" {
  value = aws_lambda_function.scrape.function_name
}

output "load_invoke_arn" {
  description = "arn of lambda to take csv.gz from s3 and load it to db"
  value       = aws_lambda_function.load.invoke_arn
}

output "load_arn" {
  value = aws_lambda_function.load.arn
}

output "load_name" {
  value = aws_lambda_function.load.function_name
}

output "report_invoke_arn" {
  description = "arn of lambda that returns results of the report"
  value       = aws_lambda_function.report.invoke_arn
}

output "report_name" {
  description = "name of lambda that returns results of the report"
  value       = aws_lambda_function.report.function_name
}
