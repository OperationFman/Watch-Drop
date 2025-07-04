terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.39.1"
    }
  }

  backend "s3" {
    bucket  = "watch-drop-terraform-state-355734424613"
    key     = "watch-drop/terraform.tfstate"
    region  = "ap-southeast-2"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_account_region
}
