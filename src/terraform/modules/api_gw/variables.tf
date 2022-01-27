variable "scrape_invoke_arn" {
  type        = string
  description = "arn of lambda to take csv.gz and move it to s3"
}

variable "etl_invoke_arn" {
  type        = string
  description = "arn of lambda to take csv.gz from s3 and load it to db"
}

variable "report_invoke_arn" {
  type        = string
  description = "arn of lambda that returns results of the report"
}
