data "template_file" "t_file" {
  count = length(local.source_files)

  template = file(element(local.source_files, count.index))
}

data "archive_file" "lambdzip" {
  type        = "zip"
  output_path = "tf_lambda.zip"
  source {
    filename = basename(local.source_files[0])
    content  = data.template_file.t_file.0.rendered
  }
  source {
    filename = basename(local.source_files[1])
    content  = data.template_file.t_file.1.rendered
  }
  source {
    filename = basename(local.source_files[2])
    content  = data.template_file.t_file.2.rendered
  }
}

resource "aws_iam_role" "scrape_to_s3" {
  name                 = "scrape_to_s3"
  max_session_duration = 3600
  assume_role_policy   = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  tags = {
    Name = "scrape_to_s3"
  }
}


data "template_file" "scrape_to_s3_policy" {
  template = file("${path.module}/scrape_to_s3_policy.json")

  vars = {
    s3_arn = "${var.s3_arn}"
  }
}

resource "aws_iam_policy" "scrape_to_s3_policy" {
  policy = data.template_file.scrape_to_s3_policy.rendered
}

resource "aws_iam_role_policy_attachment" "scrape_to_s3" {
  role       = aws_iam_role.scrape_to_s3.name
  policy_arn = resource.aws_iam_policy.scrape_to_s3_policy.arn
}

resource "aws_lambda_function" "scrape" {
  function_name    = "scrape"
  handler          = "scrape.lambda_handler"
  filename         = "tf_lambda.zip"
  source_code_hash = data.archive_file.lambdzip.output_base64sha256
  role             = aws_iam_role.scrape_to_s3.arn
  memory_size      = 2048
  runtime          = "python3.8"
  timeout          = 300
  tracing_config {
    mode = "PassThrough"
  }
}


resource "aws_iam_role" "s3_to_rds" {
  name                 = "s3_to_rds"
  max_session_duration = 3600
  assume_role_policy   = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  tags = {
    Name = "s3_to_rds"
  }
}

data "template_file" "s3_to_rds_policy" {
  template = file("${path.module}/s3_to_rds_policy.json")

  vars = {
    s3_arn  = "${var.s3_arn}",
    rds_arn = "${var.db_arn}"
  }
}

resource "aws_iam_policy" "s3_to_rds_policy" {
  policy = data.template_file.s3_to_rds_policy.rendered
}

resource "aws_iam_role_policy_attachment" "s3_to_rds_policy" {
  role       = aws_iam_role.s3_to_rds.name
  policy_arn = resource.aws_iam_policy.s3_to_rds_policy.arn
}

resource "aws_lambda_function" "etl" {
  function_name    = "etl"
  handler          = "load.lambda_handler"
  filename         = "tf_lambda.zip"
  source_code_hash = data.archive_file.lambdzip.output_base64sha256
  role             = aws_iam_role.s3_to_rds.arn
  memory_size      = 2048
  runtime          = "python3.8"
  timeout          = 300
  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_iam_role" "report_from_rds" {
  name                 = "report_from_rds"
  max_session_duration = 3600
  assume_role_policy   = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  tags = {
    Name = "report_from_rds"
  }
}

data "template_file" "report_from_rds_policy" {
  template = file("${path.module}/report_from_rds_policy.json")

  vars = {
    rds_arn = "${var.db_arn}"
  }
}

resource "aws_iam_policy" "report_from_rds_policy" {
  policy = data.template_file.report_from_rds_policy.rendered
}

resource "aws_iam_role_policy_attachment" "report_from_rds_policy" {
  role       = aws_iam_role.report_from_rds.name
  policy_arn = resource.aws_iam_policy.report_from_rds_policy.arn
}

resource "aws_lambda_function" "report" {
  function_name    = "report"
  handler          = "report.lambda_handler"
  filename         = "tf_lambda.zip"
  source_code_hash = data.archive_file.lambdzip.output_base64sha256
  role             = aws_iam_role.report_from_rds.arn
  memory_size      = 2048
  runtime          = "python3.8"
  timeout          = 300
  tracing_config {
    mode = "PassThrough"
  }
}
