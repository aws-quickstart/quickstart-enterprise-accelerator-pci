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

#certificate_file='rds-combined-ca-bundle.pem'
certificate_file='rds-ca-2015-root.pem'
#certificate_file='rds-ca-2015-us-west-1.pem'
#certificate_file='rds-ca-2015-us-west-2.pem'
certificate_full_path=os.path.join(os.environ['LAMBDA_TASK_ROOT'],certificate_file)

#https://dev.mysql.com/doc/mysql-security-excerpt/5.5/en/cleartext-pluggable-authentication.html
#https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
#https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
#https://aws.amazon.com/blogs/database/use-iam-authentication-to-connect-with-sql-workbenchj-to-amazon-aurora-mysql-or-amazon-rds-for-mysql/
#Certificates available from here https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html#UsingWithRDS.SSL.IntermediateCertificates

#conn = pymysql.connect(rds_host, user=user_name, passwd=token_database, db=db_name, connect_timeout=5, ssl={'ca':certificate_file})

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

'''
import pymysql
def lambda_handler(event,context):
    try:
        token_database=rds.generate_db_auth_token(rds_host,rds_port,user_name)
        with closing(pymysql.connect(rds_host, user=user_name, passwd=token_database, db=db_name, connect_timeout=5, ssl={'ca':certificate_file},auth_plugin_map={'mysql_clear_password'})) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return "Verified ability to establish IAM Database Authentication"
    except:
        logger.exception("ERROR: Unexpected error: Could not connect to MySQL instance.")
        sys.exit()
'''
