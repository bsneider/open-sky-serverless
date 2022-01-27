## Create S3 bucket

resource "aws_kms_key" "mykey" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
}

resource "aws_s3_bucket" "s3" {
  bucket_prefix = "open-sky-raft-galore-easter-egg-"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.mykey.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }
  #enable uploading from lambdas and api gw. Will set to * for now

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
  etag   = filemd5("${path.module}/external/flightlist_20190101_20190131.csv.gz")

}
