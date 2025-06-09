resource "aws_secretsmanager_secret" "tmdb_api_key_secret" {
  name        = "${var.project_title_lowercase}/tmdb_api_key"
  description = "TMDB API Key for the ${var.project_title} project"

  tags = {
    Project     = var.project_title
    ManagedBy   = var.owner
    Environment = var.environment
  }
}

resource "aws_secretsmanager_secret_version" "tmdb_api_key_secret_version" {
  secret_id     = aws_secretsmanager_secret.tmdb_api_key_secret.id
  secret_string = var.tmdb_api_key_value
}
