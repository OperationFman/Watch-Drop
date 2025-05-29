locals {
  dynamodb_table_name = "${var.project_title}-Subscriptions"
}

variable "project_title" {
  type    = string
  default = "WatchDrop"
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
