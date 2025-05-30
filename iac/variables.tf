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

variable "environment" {
  type    = string
  default = "Production"
}
