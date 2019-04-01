import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    rds=boto3.client('rds')
    response=rds.describe_db_instances()
    for instance in response["DBInstances"]:
        rds_tags=rds.list_tags_for_resource(ResourceName=instance['DBInstanceArn'])
        for tag in rds_tags['TagList']:
            state=str(instance['DBInstanceStatus'])
            now=datetime.now()
            if(tag['Key']=='AutoStartSchedule' and state=='stopped'):
                if(tag['Value']==str(now.hour)):
                    rds.start_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'])
            elif(tag['Key']=='AutoStopSchedule' and state=='available'):
                if(tag['Value']==str(now.hour)):
                    rds.stop_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'])
