import boto3
from concurrent.futures import ThreadPoolExecutor

# Initialize EC2 client
ec2 = boto3.client('ec2')

def check_instance(instance_id):
    """
    Check the status of a single EC2 instance.
    """
    try:
        response = ec2.describe_instance_status(InstanceIds=[instance_id])
        if response['InstanceStatuses']:
            state = response['InstanceStatuses'][0]['InstanceState']['Name']
            print(f"{instance_id} - {state}")
        else:
            print(f"{instance_id} - No status available (possibly stopped)")
    except Exception as e:
        print(f"Error checking {instance_id}: {e}")

def main():
    """
    Collect all EC2 instance IDs and check their status in parallel.
    """
    instance_ids = []

    # Use paginator to handle large volumes
    paginator = ec2.get_paginator('describe_instances')
    for page in paginator.paginate():
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])

    print(f"Found {len(instance_ids)} instances.")

    # Use threading for speed (tune max_workers based on scale)
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_instance, instance_ids)

if __name__ == "__main__":
    main()

