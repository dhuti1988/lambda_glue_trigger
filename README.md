# lambda_glue_trigger
AWS Lambda Function for sensing files and triggering glue crawler

## GitHub Actions deployment

This repo includes a workflow at `.github/workflows/deploy-lambda.yml` that:
- Builds a zip containing `lambda_file_processor.py`
- Deploys by calling `aws lambda update-function-code` (and can optionally `create-function` if the Lambda is missing)

### Required GitHub Secrets

Set these in your GitHub repo under Settings → Secrets and variables → Actions:

- **`AWS_REGION`** (or `AWS_DEFAULT_REGION`): e.g. `us-east-1`  
  (can be set as a **Secret** or a **Variable**)
- **`LAMBDA_FUNCTION_NAME`**: the existing Lambda function name (or full ARN)  
  (can be set as a **Secret** or a **Variable**)

Auth (access keys):
- **`AWS_ACCESS_KEY_ID`**
- **`AWS_SECRET_ACCESS_KEY`**

Optional (only needed if the Lambda function does not exist yet):
- **`LAMBDA_EXECUTION_ROLE_ARN`**: IAM role ARN for the Lambda execution role (Secret or Variable)

### One-time AWS configuration

Configure these in the Lambda function settings:
- **Handler**: `lambda_file_processor.lambda_handler`
- **Environment variables**:
  - `CRAWLER_NAME_CUSTOMER_ORDER`
  - `CRAWLER_NAME_CUSTOMER_MASTER`

