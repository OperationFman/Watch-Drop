data "archive_file" "tmdb_scanner_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambdas/tmdb_scanner"
  output_path = "${path.module}/tmdb_scanner_lambda.zip"
}

resource "aws_lambda_function" "tmdb_scanner_lambda" {
  function_name = "${var.project_title_lowercase}-tmdb-scanner-lambda"

  role = aws_iam_role.lambda_role.arn

  filename         = data.archive_file.tmdb_scanner_lambda_zip.output_path
  source_code_hash = data.archive_file.tmdb_scanner_lambda_zip.output_base64sha256

  handler = "main.lambda_handler"
  runtime = "python3.9"

  timeout     = 300
  memory_size = 128

  environment {
    variables = {

      TMDB_API_SECRET_NAME = aws_secretsmanager_secret.tmdb_api_key_secret.name # Use the secret's name

      DYNAMODB_TABLE_NAME    = local.dynamodb_table_name
      SES_SENDER_LAMBDA_NAME = "${var.project_title_lowercase}-ses-sender-lambda"
    }
  }

  tags = {
    Project     = var.project_title
    ManagedBy   = var.owner
    Environment = var.environment
  }
}
