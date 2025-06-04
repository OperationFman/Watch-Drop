resource "aws_cloudwatch_event_rule" "tmdb_scanner_schedule" {
  name                = "${var.project_title_lowercase}-tmdb-scanner-schedule"
  schedule_expression = var.schedule_cron

  tags = {
    Project     = var.project_title
    ManagedBy   = var.owner
    Environment = var.environment
  }
}

resource "aws_cloudwatch_event_target" "tmdb_scanner_target" {
  rule      = aws_cloudwatch_event_rule.tmdb_scanner_schedule.name
  arn       = aws_lambda_function.tmdb_scanner_lambda.arn
  target_id = "${var.project_title_lowercase}-scanner-lambda-target" 
}

resource "aws_lambda_permission" "allow_eventbridge_to_invoke_scanner" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tmdb_scanner_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.tmdb_scanner_schedule.arn
}
