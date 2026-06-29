import boto3
from concurrent.futures import ThreadPoolExecutor
import datetime

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

# --- EC2 Idle Check ---
def is_idle(instance_id):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=7)
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start,
        EndTime=end,
        Period=3600,
        Statistics=['Average']
    )
    datapoints = metrics.get('Datapoints', [])
    if datapoints:
        avg_cpu = sum(dp['Average'] for dp in datapoints) / len(datapoints)
        return avg_cpu < 5.0
    return False

def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopped {instance_id}")

# --- Volumes Cleanup ---
def cleanup_volumes():
    volumes = ec2.describe_volumes(Filters=[{'Name':'status','Values':['available']}])
    for v in volumes['Volumes']:
        if not any(t['Key']=='DoNotDelete' and t['Value']=='true' for t in v.get('Tags', [])):
            ec2.delete_volume(VolumeId=v['VolumeId'])
            print(f"Deleted volume {v['VolumeId']}")

# --- Snapshots Cleanup ---
def cleanup_snapshots():
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    for s in snapshots['Snapshots']:
        start_time = s['StartTime'].replace(tzinfo=None)
        if start_time < cutoff:
            if not any(t['Key']=='DoNotDelete' and t['Value']=='true' for t in s.get('Tags', [])):
                ec2.delete_snapshot(SnapshotId=s['SnapshotId'])
                print(f"Deleted snapshot {s['SnapshotId']}")

# --- Elastic IPs Cleanup ---
def cleanup_eips():
    addresses = ec2.describe_addresses()
    for a in addresses['Addresses']:
        if 'InstanceId' not in a:
            ec2.release_address(AllocationId=a['AllocationId'])
            print(f"Released Elastic IP {a['PublicIp']}")

# --- Lambda Handler ---
def lambda_handler(event, context):
    # EC2 Idle Cleanup
    instance_ids = []
    paginator = ec2.get_paginator('describe_instances')
    for page in paginator.paginate():
        for r in page['Reservations']:
            for i in r['Instances']:
                if i['State']['Name'] == "running":
                    instance_ids.append(i['InstanceId'])

    batch_size = 50
    for i in range(0, len(instance_ids), batch_size):
        batch = instance_ids[i:i+batch_size]
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda id: stop_instance(id) if is_idle(id) else None, batch)

    # Housekeeping
    cleanup_volumes()
    cleanup_snapshots()
    cleanup_eips()
