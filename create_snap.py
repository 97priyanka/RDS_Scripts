import boto3
import os
from datetime import datetime
from datetime import timedelta
def lambda_handler(event, context):
    
    rds = boto3.client('rds')
    response = rds.describe_db_instances()
    for db in response['DBInstances']:
        
        instance_arn = db['DBInstanceArn']
        db_tags = rds.list_tags_for_resource(ResourceName=instance_arn)
        for tag in db_tags['TagList']:
            if tag['Key'] == 'backup' and tag['Value']=='yes' :
                
                db_instance=db['DBInstanceIdentifier']
                retention_days=int(os.environ['Retention_days'])     
                deletion_date=str(datetime.date(datetime.now()) + timedelta(days=retention_days)) 
                now=datetime.now()
                todays_date=str(datetime.date(datetime.now()))
                date_time = now.strftime("%d-%m-%Y-%H-%M-%S")
                snap_name=db_instance+date_time
                rds.create_db_snapshot(DBSnapshotIdentifier=snap_name,DBInstanceIdentifier=db_instance,Tags=[{'Key': 'Retention_days','Value': deletion_date},{'Key':'Todays_date','Value': todays_date}])
            
            else :
                print("No instance with tag backup-true.")
