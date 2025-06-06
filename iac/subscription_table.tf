resource "aws_dynamodb_table" "subscriptions_table" {
  name         = local.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_email"
  range_key    = "tmdb_id"

  attribute {
    name = "user_email"
    type = "S"
  }

  attribute {
    name = "tmdb_id"
    type = "S"
  }

  tags = {
    Project     = var.project_title
    Environment = var.environment
    ManagedBy   = var.owner
  }
}
