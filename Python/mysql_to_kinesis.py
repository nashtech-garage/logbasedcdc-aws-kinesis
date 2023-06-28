import json
import boto3
from botocore.config import Config

# pymysqlreplication : 
# 		Pure Python Implementation of MySQL replication protocol build on top of PyMYSQL
#		This allow you to receive event like insert, update, delete with their datas and raw SQL queries
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
  # This event is trigger when a row in the database is removed
  DeleteRowsEvent,
  # This event is triggered when a row in the database is changed
  UpdateRowsEvent,
  # This event is triggered when a row in database is added
  WriteRowsEvent,
)

def main():
  # boto3 : You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services
  # session.Session(...) : A session stores configuration state and allows you to create service clients and resources
  #session = boto3.session.Session(profile_name='my-dev-profile')
  session = boto3.session.Session(profile_name='default')
  
  # client(...) : Create a low-level service client by name
  kinesis = session.client(service_name="kinesis", region_name='ap-southeast-1')
  # BinLogStreamReader : Connect to replication stream and read event
  stream = BinLogStreamReader(
    connection_settings= {
      "host": "localhost",
      "port": 3306,
      "user": "test",
      "passwd": "123"},
    server_id=100,
    blocking=True,
    resume_stream=True,
    only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])

  for binlogevent in stream:
    for row in binlogevent.rows:
      event = {"schema": binlogevent.schema,
      "table": binlogevent.table,
      "type": type(binlogevent).__name__,
      "row": row
      }
      
	  # Kinesis.Client.put_records(...) : Writes multiple data records into a Kinesis data stream in a single call
	  # StreamName : The stream name associated with the request
	  # Data : The data blob to put into the record, which is base64-encoded when the blob is serialized
	  # PartitionKey : Determines which shard in the stream the data record is assigned to
	  # json.dumps(...) : If you have a Python object, you can convert it into a JSON string
      kinesis.put_record(StreamName="kinesis.mysql_source_database", Data=json.dumps(event), PartitionKey="default")
      print(json.dumps(event))

if __name__ == "__main__":
   main()