# Signed URL File Gateway - Final Laboratory Project

**Secure, serverless, and ephemeral file sharing — built the AWS way.**

This project delivers a minimal yet production-grade file gateway service that allows users to **upload** and **download** files to/from a completely private S3 bucket — without ever exposing the bucket publicly.

Using **pre-signed URLs**, the system provides time-limited, cryptographically secure access:
- Direct client-to-S3 uploads (15-minute expiration)
- Time-bound downloads via HTTP 307 redirect (1-hour expiration)

### Key Benefits
- **Security-first**: Private bucket + signed URLs = least exposure
- **Cost-efficient**: Serverless (pay-per-request), no EC2 instances
- **Scalable**: Handles bursts without manual scaling
- **Reproducible**: 100% Infrastructure as Code with AWS SAM
- **Simple**: Only two endpoints, clean API design

This implementation was developed as the final laboratory project for an AWS course, demonstrating best practices in serverless architecture, least-privilege security, and temporary access patterns.
## Features

- **POST /upload** → Generates a pre-signed PUT URL for direct client-to-S3 upload
- **GET /files/{objectKey}** → Returns 307 Temporary Redirect to a pre-signed GET URL (expires in 1 hour)
- No file content passes through Lambda or API Gateway
- Least-privilege IAM permissions
- Fully reproducible with AWS SAM (Infrastructure as Code)
- No public bucket exposure

## Architecture Diagram

![Architecture](images/workflowproject.png)


## Project Structure
```text
file-gateway-lab/
├── template.yaml          # AWS SAM template (Infrastructure as Code)
├── src/
│   └── app.py             # Lambda handler for both endpoints
├── README.md              # This file
└── images/
    └── workflowproject.png
```

## Prerequisites

- AWS account with permissions to create: S3, API Gateway, Lambda, IAM, CloudFormation
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed
- AWS CLI configured (`aws configure`)

## Deployment

```bash
# 1. Clone the repository
git clone https://github.com/PrisWen/aws-lab4.git

# 2. Build the SAM application
sam build

# 3. Deploy (interactive guided mode)
sam deploy --guided
```

## Testing with curl
### 1. Get pre-signed upload URL

```bash
curl -X POST https://deploy-proy4.execute-api.us-east-1.amazonaws.com/prod/upload \
  -H "Content-Type: application/json" \
  -d '{"filename": "my-document.pdf", "content_type": "application/pdf"}'
{
  "object_key": "uploads/550e8400-e29b-41d4-a716-446655440000_my-document.pdf",
  "upload_url": "https://file-gateway-...s3.amazonaws.com/uploads/...pdf?X-Amz-Algorithm=..."
}
```


### 2. Upload file directly to S3

```bash
curl --request PUT \
  --upload-file ./my-document.pdf \
  "https://file-gateway-...s3.amazonaws.com/uploads/...pdf?X-Amz-Algorithm=..."
```


### 3. Download file (follow redirect)

```bash
# -L follows redirects automatically
curl -L https://deploy-proy4.execute-api.us-east-1.amazonaws.com/prod/files/uploads/550e8400-e29b-41d4-a716-446655440000_my-document.pdf \
  -o downloaded-file.pdf
```

Or open in a browser:

https://deploy-proy4.execute-api.us-east-1.amazonaws.com/prod/files/uploads/550e8400-e29b-41d4-a716-446655440000_my-document.pdf

→ Browser redirects and downloads directly from S3.


## Cleanup (Important!)

Delete the stack to avoid ongoing AWS charges:

```bash
sam delete --stack-name file-gateway
```


## Security & Design Notes

- Private S3 bucket with all public access blocked
- Time-limited signed URLs
  - Upload: 15 minutes
  - Download: 60 minutes
- Least-privilege IAM
  - Lambda can only `PutObject` and `GetObject` on `uploads/*`
- **307 Temporary Redirect**
  - Preserves the original HTTP method (`GET`)
  - Modern standard for temporary redirects
- No authentication layer
  - Intentional minimal design for lab/demo purposes

## Documentation

It includes:

- Architecture explanation & diagram
- Endpoint examples
- Code walkthrough
- Rationale for design choices

[Documentation (Google Doc)](https://docs.google.com/document/d/1AlrEa7FXxZNZ6l4xEMJUwdb3QSHHpzJnM5z3lR--HAM/edit?usp=sharing)

