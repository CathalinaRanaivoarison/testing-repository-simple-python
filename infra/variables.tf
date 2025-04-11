variable "aws_region" {
  default = "eu-west-3"
}

variable "app_name" {
  default = "scalable-flask-app"
}

variable "container_port" {
  default = 8888
}

variable "aws_account_id" {
  description = "AWS Account ID"
}
