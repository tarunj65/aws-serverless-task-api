provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "tasks" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "task_id"

  attribute {
    name = "task_id"
    type = "S"
  }

  tags = {
    Name        = var.table_name
    Environment = var.environment
    Project     = "aws-serverless-task-api"
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "${var.environment}-serverless-task-api-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Environment = var.environment
    Project     = "aws-serverless-task-api"
  }
}


resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "${var.environment}-serverless-task-api-dynamodb-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Scan"
      ]

      Resource = aws_dynamodb_table.tasks.arn
    }]
  })
}


resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}



resource "aws_lambda_function" "task_api" {
  function_name = "${var.environment}-serverless-task-api"

  role    = aws_iam_role.lambda_role.arn
  runtime = "python3.12"

  handler = "function.handler.handler"

  filename         = "${path.module}/../lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda.zip")

  timeout     = 10
  memory_size = 128

  environment {
    variables = {
      TASKS_TABLE = aws_dynamodb_table.tasks.name
    }
  }

  tags = {
    Environment = var.environment
    Project     = "aws-serverless-task-api"
  }
}


resource "aws_apigatewayv2_api" "task_api" {
  name          = "${var.environment}-serverless-task-api"
  protocol_type = "HTTP"

  tags = {
    Environment = var.environment
    Project     = "aws-serverless-task-api"
  }
}


resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.task_api.id
  integration_type = "AWS_PROXY"

  integration_uri = aws_lambda_function.task_api.invoke_arn

  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "task_api" {
  api_id = aws_apigatewayv2_api.task_api.id

  route_key = "ANY /{proxy+}"

  target = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.task_api.id

  name = "$default"

  auto_deploy = true
}


resource "aws_lambda_permission" "api_gateway" {
  statement_id = "AllowAPIGatewayInvoke"

  action = "lambda:InvokeFunction"

  function_name = aws_lambda_function.task_api.function_name

  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.task_api.execution_arn}/*/*"
}



