provider "aws" {
  region = "us-east-1"
}

module "dynamodb" {
  source     = "./modules/dynamodb"
  table_name = "microservice-table"
  hash_key   = "id"
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "dynamodb_access" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_function"
  output_path = "${path.module}/lambda_function.zip"
}


module "lambda" {
  source                 = "./modules/lambda"
  function_name          = "microservice-function"
  lambda_package         = data.archive_file.lambda_zip.output_path
  handler                = "index.handler"
  runtime                = "nodejs18.x"
  iam_role               = aws_iam_role.lambda_exec.arn
  environment_variables  = { TABLE_NAME = module.dynamodb.table_name }
}

module "api" {
  source     = "./modules/apigateway"
  api_name   = "microservice-api"
  lambda_arn = module.lambda.lambda_function_arn
  route_key  = "POST /store"
}
