locals {
  dynamodb_table_name = "${var.project_title}-Subscriptions"
}

variable "project_title" {
  type        = string
  description = "e.g: WatchDrop"
}

variable "project_title_lowercase" {
  type        = string
  description = "e.g: watch-drop"
}

variable "ses_domain" {
  type        = string
  description = "e.g: watchdrop.org"
}

variable "ses_receiving_email_address" {
  type        = string
  description = "e.g: subscribe@watchdrop.org"
}

variable "owner" {
  type        = string
  description = "e.g: Franklin Moon"
}

variable "aws_account_number" {
  type        = string
  description = "AWS account ID number"
}

variable "aws_account_region" {
  type        = string
  description = "e.g: ap-southeast-2"
}

variable "tmdb_api_key_value" {
  description = "TMDB API Key from The Movie Database. Ensure you set this up in your terraform.tfvars file"
  type        = string
  sensitive   = true
}

variable "schedule_cron" {
  description = "The cron expression for when you want the TMDB scan to run e.g: cron(0 8 * * ? *) for 8 AM UTC daily"
  type        = string
}

variable "environment" {
  type        = string
  description = "e.g: Production or Development"
}
