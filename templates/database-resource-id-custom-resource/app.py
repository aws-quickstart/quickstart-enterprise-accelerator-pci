import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import cfnresponse
import boto3
rds = boto3.client('rds')

def lambda_handler(event, context):
    try:
        #https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-cfnresponsemodule#w2ab1c21c10d183c21c17c11c13b5
        request_type=event['RequestType']
        logger.info("Request type %s",request_type)
        response = rds.describe_db_instances(
            DBInstanceIdentifier=event['ResourceProperties']['DatabaseInstanceId']
        )
        database_resource_id=response["DBInstances"][0]["DbiResourceId"]
        responseData = {}
        responseData['DbiResourceId']=database_resource_id
        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            responseData
        )
    except Exception:
        logger.exception("Error with Database Resource Id Custom Resource")
        responseData = {}
        responseData['Status':'FAILED']
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            responseData
        )
