# AWS EC2 Route 53 Automation

Automatically update Route 53 DNS records with the new public IP address of an EC2 instance after it is stopped and started.

---

## Overview
This solution uses:
- **AWS Lambda**: To update Route 53 DNS records.
- **EventBridge**: To trigger the Lambda function on EC2 instance state changes.
- **IAM Roles**: To grant necessary permissions for EC2 and Route 53.

---

## Prerequisites
1. An EC2 instance.
2. A Route 53 hosted zone.
3. An IAM role with permissions for EC2 and Route 53.

---

## Steps to Set Up

### 1. Create an IAM Role for Lambda
- Attach the following policies:
  - `AmazonEC2ReadOnlyAccess`
  - `AmazonRoute53FullAccess`

### 2. Create the Lambda Function
- Use the provided Python code to create a Lambda function.
- Assign the IAM role created in Step 1.

### 3. Create an EventBridge Rule
- Set up a rule to trigger the Lambda function on EC2 instance state changes (`running` and `stopped`).

### 4. Test the Setup
- Stop and start your EC2 instance.
- Verify that the Route 53 DNS record is updated with the new public IP.

---

## Lambda Function Code
The Lambda function code is available in the [`lambda_function.py`](lambda_function.py) file.

