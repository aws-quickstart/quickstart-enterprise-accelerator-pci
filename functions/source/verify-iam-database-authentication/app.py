import sys
import os
from contextlib import closing

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
rds = boto3.client('rds')

rds_host  = os.environ["DatabaseEndpointURL"]
rds_port = os.environ["DatabasePort"]
user_name = os.environ["DatabaseUserName"]

#Please specify the region certificate to ensure that the connection is to the intended region. For now using the combined certificate bundle.
#Certificates available from here https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html#UsingWithRDS.SSL.IntermediateCertificates
s3 = boto3.client('s3')
certificate_file='rds-combined-ca-bundle.pem'
certificate_full_path=os.path.join('/tmp',certificate_file)
s3.download_file('rds-downloads', 'rds-combined-ca-bundle.pem', certificate_full_path)

import pymysql

try:
    token_database=rds.generate_db_auth_token(rds_host,rds_port,user_name)
    conn = pymysql.connect(rds_host, user=user_name, passwd=token_database, connect_timeout=5, ssl={'ca':certificate_full_path})
except:
    logger.exception("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

def lambda_handler(event, context):
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        print(cursor.fetchone())

    return "Verified ability to establish IAM Database Authentication"
