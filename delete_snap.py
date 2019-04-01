import boto3
from datetime import datetime
def lambda_handler(event, context):
    rds = boto3.client('rds')
    now=str(datetime.date(datetime.now()))
    response = rds.describe_db_snapshots()
    for snap in response['DBSnapshots']:
        
        snapshot_arn = snap['DBSnapshotArn']
        snap_tags = rds.list_tags_for_resource(ResourceName=snapshot_arn)
        for tag in snap_tags['TagList']:
            if tag['Key'] == 'Retention_days' and tag['Value']==now :
                
                snap_instance=snap['DBSnapshotIdentifier']
                rds.delete_db_snapshot(DBSnapshotIdentifier=snap_instance)
                
            else :
                print("No Snapshot with retention date of today.")
                
                
