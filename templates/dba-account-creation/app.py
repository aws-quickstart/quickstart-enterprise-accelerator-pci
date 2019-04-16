#https://docs.aws.amazon.com/code-samples/latest/catalog/python-secretsmanager-secrets_manager.py.html

import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import pymysql

import boto3
client = boto3.client('secretsmanager')

import json

#rds settings
#DatabaseEndpointURL
rds_host  = os.environ["DatabaseEndpointURL"]
#DatabaseCredentialsSecretsArn
get_secret_value_response = client.get_secret_value(
    SecretId=os.environ["DatabaseCredentialsSecretsArn"],
)
credentials=json.loads(get_secret_value_response["SecretString"])
name = credentials["username"]
password = credentials["password"]

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, connect_timeout=5)
except:
    logger.exception("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    with conn.cursor() as cur:
        cur.execute("CREATE USER sample_dba IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS'")
        cur.execute("GRANT USAGE ON *.* TO 'sample_dba'@'%' REQUIRE SSL")
        cur.execute("FLUSH PRIVILEGES")

    return "Created sample_dba database user"
