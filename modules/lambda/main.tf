resource "aws_lambda_function" "this" {
  filename         = var.lambda_package
  function_name    = var.function_name
  role             = var.iam_role
  handler          = var.handler
  runtime          = var.runtime
  source_code_hash = filebase64sha256(var.lambda_package)

  environment {
    variables = var.environment_variables
  }
}
