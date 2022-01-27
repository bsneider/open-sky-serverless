output "s3_arn" {
  value = aws_s3_bucket.s3.arn
}

output "bucket_name" {
  value = aws_s3_bucket.s3.id
}
