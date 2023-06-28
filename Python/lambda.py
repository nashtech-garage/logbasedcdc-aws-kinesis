import sys
import logging
import pymysql
import json
import boto3
import base64

# rds settings
rds_host  = "cdc-mysql-database.cdzebrfwijuh.ap-southeast-1.rds.amazonaws.com"
user_name = "admin"
password = "12345678"
db_name = "sink_mysql_db"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(host=rds_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event, context):
    # TODO implement
    kinesis = boto3.client('kinesis')
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        # do something with the data
        # print(data['row']['values']['user_id'])
        table = data['table']
        type = data['type']
        
        item_count = 0
        
        print(type)
        
        user_id = ""
        first_name = ""
        last_name = ""
        wage = 0
        
        if table == "users":
            if type == "WriteRowsEvent":
                print("1")
                user_id = data['row']['values']['user_id']
                first_name = data['row']['values']['first_name']
                last_name = data['row']['values']['last_name']
                sql_string = f"insert into users (user_id, first_name, last_name) values({user_id}, '{first_name}', '{last_name}')"
            elif type == "UpdateRowsEvent":
                print("2")
                user_id = data['row']['after_values']['user_id']
                first_name = data['row']['after_values']['first_name']
                last_name = data['row']['after_values']['last_name']
                sql_string = f"update users set first_name='{first_name}', last_name='{last_name}' where user_id={user_id}"
            elif type == "DeleteRowsEvent":
                print("3")
                user_id = data['row']['values']['user_id']
                sql_string = f"delete from users where user_id={user_id}"
            else:
                logger.error("ERROR: Invalid event!")
                sys.exit()
        elif table == "wages":
            if type == "WriteRowsEvent":
                print("1")
                user_id = data['row']['values']['user_id']
                wage = data['row']['values']['wage']
                sql_string = f"insert into wages (user_id, wage) values({user_id}, {wage})"
            elif type == "UpdateRowsEvent":
                print("2")
                user_id = data['row']['after_values']['user_id']
                wage = data['row']['after_values']['wage']
                sql_string = f"update wages set wage={wage} where user_id={user_id}"
            elif type == "DeleteRowsEvent":
                print("3")
                user_id = data['row']['values']['user_id']
                sql_string = f"delete from wages where user_id={user_id}"
            else:
                logger.error("ERROR: Invalid event!")
                sys.exit()
        else:
                logger.error("ERROR: Invalid table!")
                sys.exit()
        
        # user_wages
        full_name = first_name + " " + last_name
        if type == "WriteRowsEvent" or type == "UpdateRowsEvent":
            print("12")
            sql_string_insert = f"insert into user_wages (user_id, full_name, wage) values({user_id}, '{full_name}', '{wage}') ON DUPLICATE KEY "
            if full_name != " ":
                sql_string_update = f"UPDATE full_name = '{full_name}'"
            if wage != 0:
                sql_string_update = f"UPDATE wage={wage}"
            sql_string_user_wages = sql_string_insert + sql_string_update
        elif type == "DeleteRowsEvent":
            print("3")
            sql_string_user_wages = f"delete from user_wages where user_id={user_id}"
        else:
            logger.error("ERROR: Invalid event!")
            sys.exit()
        
        #sql_string = f"insert into users (user_id, first_name, last_name) values({user_id}, '{first_name}', '{last_name}')"
        
        print(sql_string)

        with conn.cursor() as cur:
            cur.execute(sql_string)
            cur.execute(sql_string_user_wages)
            conn.commit()
            #logger.info("The following items have been added to the database:")
            #logger.info(data['row']['values'])

        conn.commit()

    return "Done"
