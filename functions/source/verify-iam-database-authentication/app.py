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

#Please specify the region certificate to ensure that the connection is to the intended region.
#Certificates available from here https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html#UsingWithRDS.SSL.IntermediateCertificates
certificate_file='rds-ca-2015-root.pem'
certificate_full_path=os.path.join(os.environ['LAMBDA_TASK_ROOT'],certificate_file)

#https://dev.mysql.com/doc/mysql-security-excerpt/5.5/en/cleartext-pluggable-authentication.html
#https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
#https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
import mysql.connector
def lambda_handler(event, context):
    try:
        cursor=None
        token_database=rds.generate_db_auth_token(rds_host,rds_port,user_name)
        with closing(mysql.connector.connect(user=user_name,password=token_database,host=rds_host,auth_plugin='mysql_clear_password',ssl_ca=certificate_full_path,ssl_verify_cert=True)) as connection:
            cursor=connection.cursor()
            cursor.execute("SELECT 1")
            return "Verified ability to establish IAM Database Authentication"
    except:
        logger.exception("ERROR: Unexpected error: Could not connect to MySQL instance.")
        sys.exit()
    finally:
        cursor.close()

