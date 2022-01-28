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
  bucket     = aws_s3_bucket.s3.id
  key        = "flightlist_20190101_20190131.csv.gz"
  source     = "${path.module}/external/flightlist_20190101_20190131.csv.gz"
  depends_on = [aws_s3_bucket_notification.aws_lambda_trigger]
}

# Adding S3 bucket as trigger to my lambda and giving the permissions
resource "aws_s3_bucket_notification" "aws_lambda_trigger" {
  bucket = aws_s3_bucket.s3.id
  lambda_function {
    lambda_function_arn = var.load_lambda_arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv.gz"

  }
  depends_on = [aws_lambda_permission.allow_bucket]
}
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = var.load_lambda_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.s3.id}"
}
