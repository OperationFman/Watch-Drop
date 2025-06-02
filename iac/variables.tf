locals {
  dynamodb_table_name = "${var.project_title}-Subscriptions"
}

variable "project_title" {
  type    = string
  default = "WatchDrop"
}

variable "project_title_lowercase" {
  type    = string
  default = "watch-drop"
}

variable "ses_email" {
  type    = string
  default = "le.watch.drop@gmail.com"
}

# variable "ses_domain" {
#     type    = string
#   default = "watchdrop.com"
# }

variable "owner" {
  type    = string
  default = "Franklin Moon"
}

variable "aws_account_number" {
  type    = string
  default = "355734424613"
}

variable "aws_account_region" {
  type    = string
  default = "ap-southeast-2"
}

variable "tmdb_api_key_value" {
  description = "The actual value of your TMDB API Key, ensure you set this up locally and in Secrets Manager."
  type        = string
  sensitive   = true
}

variable "environment" {
  type    = string
  default = "Production"
}
