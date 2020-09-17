terraform {
  backend "s3" {
    region  = "eu-west-1"
    bucket  = "video-messaging-terraform-state"
    key     = "video-messaging-processor-ec2/terraform.tfstate"
  }
}

provider "aws" {
  region = "eu-west-1"
}

data "aws_caller_identity" "current" {}

module "ec2" {
  source = "./ec2"
}