variable "aws_region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "ap-south-1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "table_name" {
  description = "DynamoDB table name"
  type        = string
  default     = "aws-serverless-task-api-dev"
}
