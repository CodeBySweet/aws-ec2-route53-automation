import boto3
import json

# Define AWS clients
ec2_client = boto3.client('ec2')
route53_client = boto3.client('route53')

# Configuration
INSTANCE_ID = "INSTANCE_ID"  # Replace with your EC2 instance ID
HOSTED_ZONE_ID = "HOSTED_ZONE_ID"  # Replace with your Route 53 Hosted Zone ID
RECORD_NAME_1 = "RECORD_NAME_1"  # First A record to update
RECORD_NAME_2 = "RECORD_NAME_2"  # Second A record to update
TTL = 300  # TTL for the DNS record

def lambda_handler(event, context):
    try:
        # Get instance details
        reservations = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])["Reservations"]
        instance = reservations[0]["Instances"][0]
        state = instance["State"]["Name"]

        if state == "running":
            public_ip = instance.get("PublicIpAddress")
            
            if not public_ip:
                print("Instance is running but has no public IP.")
                return {
                    "statusCode": 400,
                    "body": json.dumps("Instance has no public IP")
                }
            
            print(f"Updating Route 53: {RECORD_NAME_1} -> {public_ip}")
            print(f"Updating Route 53: {RECORD_NAME_2} -> {public_ip}")

            # Prepare Route 53 update request for the first A record
            response_1 = route53_client.change_resource_record_sets(
                HostedZoneId=HOSTED_ZONE_ID,
                ChangeBatch={
                    "Comment": "Auto-updating EC2 public IP",
                    "Changes": [
                        {
                            "Action": "UPSERT",
                            "ResourceRecordSet": {
                                "Name": RECORD_NAME_1,
                                "Type": "A",
                                "TTL": TTL,
                                "ResourceRecords": [{"Value": public_ip}]
                            }
                        }
                    ]
                }
            )

            # Prepare Route 53 update request for the second A record
            response_2 = route53_client.change_resource_record_sets(
                HostedZoneId=HOSTED_ZONE_ID,
                ChangeBatch={
                    "Comment": "Auto-updating EC2 public IP",
                    "Changes": [
                        {
                            "Action": "UPSERT",
                            "ResourceRecordSet": {
                                "Name": RECORD_NAME_2,
                                "Type": "A",
                                "TTL": TTL,
                                "ResourceRecords": [{"Value": public_ip}]
                            }
                        }
                    ]
                }
            )

            return {
                "statusCode": 200,
                "body": json.dumps("Route 53 updated successfully for both records")
            }
        
        else:
            print(f"Instance is in state: {state}. No update needed.")
            return {
                "statusCode": 200,
                "body": json.dumps("Instance is not running, no action taken")
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }