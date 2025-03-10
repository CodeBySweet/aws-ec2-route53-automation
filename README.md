# Lambda Function to Update Route 53 DNS Record on EC2 State Change

This guide provides step-by-step instructions to set up a Lambda function that automatically updates two Route 53 DNS records whenever an EC2 instance changes its state (e.g., starts or stops). This ensures that your DNS records always point to the correct public IP address of your EC2 instance.

---

## Prerequisites

- An AWS account with sufficient permissions to create IAM roles, Lambda functions, and EventBridge rules.
- An EC2 instance with a public IP address.
- A Route 53 hosted zone and two DNS records (`RECORD_NAME_1` and `RECORD_NAME_2`) that you want to update automatically.

---

## Step 1: Create an IAM Role for Lambda

1. **Navigate to the IAM Console:**
   - Go to the [IAM Console](https://console.aws.amazon.com/iam/).

2. **Create a New Role:**
   - Click on **Roles** in the left-hand menu.
   - Click **Create role**.
   - Select **AWS service** as the trusted entity type.
   - Choose **Lambda** as the service that will use this role.
   - Click **Next: Permissions**.

3. **Attach Policies:**
   - Attach the following policies to the role:
     - `AmazonEC2ReadOnlyAccess`
     - `AmazonRoute53FullAccess`
   - Click **Next: Tags** (optional).
   - Click **Next: Review**.

4. **Name the Role:**
   - Provide a name for the role, e.g., `Lambda-EC2-Route53-Update-Role`.
   - Click **Create role**.

---

## Step 2: Create the Lambda Function

1. **Navigate to the Lambda Console:**
   - Go to the [Lambda Console](https://console.aws.amazon.com/lambda/).

2. **Create a New Function:**
   - Click **Create function**.
   - Choose **Author from scratch**.
   - Provide a name for the function, e.g., `Update-Route53-DNS`.
   - Select the **Python 3.x** runtime.
   - Under **Permissions**, expand **Change default execution role**.
   - Select **Use an existing role** and choose the role you created in Step 1.
   - Click **Create function**.

3. **Add the Python Code:**
   - In the **Function code** section, replace the default code with the following code from the [`lambda_function.py`](lambda_function.py)

   - Replace the following placeholders with your actual values:
     - `INSTANCE_ID`: Your EC2 instance ID.
     - `HOSTED_ZONE_ID`: Your Route 53 hosted zone ID.
     - `RECORD_NAME_1`: The first DNS record name (e.g., `example1.com.`).
     - `RECORD_NAME_2`: The second DNS record name (e.g., `www.example1.com.`).

4. **Deploy the Function:**
   - Click **Deploy** to save and deploy the function.

---

## Step 3: Create an EventBridge Rule

1. **Navigate to the EventBridge Console:**
   - Go to the [EventBridge Console](https://console.aws.amazon.com/events/).

2. **Create a New Rule:**
   - Click **Create rule**.
   - Provide a name for the rule, e.g., `EC2-State-Change-Rule`.
   - Under **Event source**, select **Event pattern**.
   - Choose **AWS events** as the event source.

3. **Define the Event Pattern:**
   - Use the following event pattern to trigger the Lambda function on EC2 instance state changes:

     ```json
     {
       "source": ["aws.ec2"],
       "detail-type": ["EC2 Instance State-change Notification"],
       "detail": {
         "state": ["running", "stopped"]
       }
     }
     ```

4. **Set the Target:**
   - Under **Targets**, click **Add target**.
   - Select **Lambda function** as the target type.
   - Choose the Lambda function you created in Step 2.

5. **Create the Rule:**
   - Click **Create**.

---

## Step 4: Test the Setup

1. **Stop and Start Your EC2 Instance:**
   - Go to the [EC2 Console](https://console.aws.amazon.com/ec2/).
   - Select your instance and stop it.
   - Wait for the instance to stop, then start it again.

2. **Verify the Route 53 DNS Records:**
   - Go to the [Route 53 Console](https://console.aws.amazon.com/route53/).
   - Check the DNS records (`RECORD_NAME_1` and `RECORD_NAME_2`) you configured in the Lambda function.
   - Ensure that both records have been updated with the new public IP address of the EC2 instance.

---

## Conclusion

You have successfully set up a Lambda function that automatically updates two Route 53 DNS records whenever your EC2 instance changes its state. This ensures that your DNS records always point to the correct public IP address of your EC2 instance.

For further customization, you can modify the Lambda function to handle additional scenarios or integrate with other AWS services.