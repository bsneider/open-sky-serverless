## Create S3 bucket

resource "aws_s3_bucket" "s3" {
  bucket_prefix = "open-sky-raft-galore-easter-egg-"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_object" "flightlist" {
  bucket = aws_s3_bucket.s3.id
  key    = "flightlist_20190101_20190131.csv.gz"
  source = "${path.module}/external/flightlist_20190101_20190131.csv.gz"
  # etag   = filemd5("${path.module}/external/flightlist_20190101_20190131.csv.gz")

}

# resource "aws_lambda_permission" "allow_bucket" {
#   statement_id  = "AllowExecutionFromS3Bucket"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.func.arn
#   principal     = "s3.amazonaws.com"
#   source_arn    = aws_s3_bucket.bucket.arn
# }



# resource "aws_s3_bucket_notification" "bucket_notification" {
#   bucket = aws_s3_bucket.bucket.id

#   lambda_function {
#     lambda_function_arn = aws_lambda_function.func.arn
#     events              = ["s3:ObjectCreated:*"]
#     filter_prefix       = "AWSLogs/"
#     filter_suffix       = ".log"
#   }

#   depends_on = [aws_lambda_permission.allow_bucket]
# }
