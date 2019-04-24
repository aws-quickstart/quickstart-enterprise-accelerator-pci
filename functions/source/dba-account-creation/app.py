#https://docs.aws.amazon.com/code-samples/latest/catalog/python-secretsmanager-secrets_manager.py.html

import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import pymysql

import boto3
secretsmanager = boto3.client('secretsmanager')

import json

#rds settings
#DatabaseEndpointURL
rds_host  = os.environ["DatabaseEndpointURL"]
#DatabaseCredentialsSecretsArn
get_secret_value_response = secretsmanager.get_secret_value(
    SecretId=os.environ["DatabaseCredentialsSecretsArn"],
)
credentials=json.loads(get_secret_value_response["SecretString"])
name = credentials["username"]
password = credentials["password"]

#Please specify the region certificate to ensure that the connection is to the intended region. For now using the combined certificate bundle.
#Certificates available from here https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html#UsingWithRDS.SSL.IntermediateCertificates
s3 = boto3.client('s3')
certificate_file='rds-combined-ca-bundle.pem'
certificate_full_path=os.path.join('/tmp',certificate_file)
s3.download_file('rds-downloads', 'rds-combined-ca-bundle.pem', certificate_full_path)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, connect_timeout=5, ssl={'ca':certificate_full_path})
except:
    logger.exception("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    with conn.cursor() as cursor:
        cursor.execute("CREATE USER sample_dba IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';")
        print(cursor.fetchone())
        cursor.execute("GRANT USAGE ON *.* TO 'sample_dba'@'%' REQUIRE SSL;")
        print(cursor.fetchone())
        cursor.execute("FLUSH PRIVILEGES;")
        print(cursor.fetchone())

    return "Created sample_dba database user"

