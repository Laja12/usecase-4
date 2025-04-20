variable "lambda_package" {}
variable "function_name" {}
variable "iam_role" {}
variable "handler" {}
variable "runtime" {}
variable "environment_variables" {
  type = map(string)
  default = {}
}
