import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    rds=boto3.client('rds')
    response=rds.describe_db_instances()
    for instance in response["DBInstances"]:
        rds_tags=rds.list_tags_for_resource(ResourceName=instance['DBInstanceArn'])
        flag=0
        for tag in rds_tags['TagList']:
            state=str(instance['DBInstanceStatus'])
            now=datetime.now()
            if(tag['Key']=='AutoStopSchedule' and state=='running'):
                if(tag['Value']==str(now.hour)):
                    flag=1
                    rds.stop_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'])
                
        if flag==0:
            print("This instance is in "+state+" state and do not allow auto stop action.")
                    
