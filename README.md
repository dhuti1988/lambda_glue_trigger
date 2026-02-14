# lambda_glue_trigger
AWS Lambda Function for sensing files and triggering glue crawler

## GitHub Actions deployment

This repo includes a workflow at `.github/workflows/deploy-lambda.yml` that:
- Builds a zip containing `lambda_file_processor.py`
- Deploys by calling `aws lambda update-function-code` on an **existing** Lambda function in your AWS account

### Required GitHub Secrets

Set these in your GitHub repo under Settings → Secrets and variables → Actions:

- **`AWS_REGION`**: e.g. `us-east-1`
- **`LAMBDA_FUNCTION_NAME`**: the existing Lambda function name (or full ARN)

Choose ONE auth method:

- **Option A (OIDC assume-role)**:
  - **`AWS_ROLE_ARN`**: IAM role ARN that GitHub Actions can assume (requires AWS-side OIDC setup)

- **Option B (access keys)**:
  - **`AWS_ACCESS_KEY_ID`**
  - **`AWS_SECRET_ACCESS_KEY`**

### One-time AWS configuration

Configure these in the Lambda function settings:
- **Handler**: `lambda_file_processor.lambda_handler`
- **Environment variable**: `CRAWLER_NAME`

