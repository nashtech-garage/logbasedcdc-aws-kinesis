# Introduction

I build a streaming data solution for log-based CDC with MySQL, AWS Kinesis, AWS Lambda, and Python.

# Architecture

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/Architecture.PNG)

Build a data flow as architecture as the following steps:



# Step 1: Prepare a MySQL source database with 2 users and wages tables

CREATE TABLE users(user_id INTEGER, first_name VARCHAR(200), last_name VARCHAR(200), PRIMARY KEY (user_id));

CREATE TABLE wages(user_id INTEGER, wage integer, PRIMARY KEY (user_id));

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/SourceDatabase.PNG)



# Step 2: Create an AWS Kinesis stream

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/KinesisStream.PNG)



# Step 3: Run Python script to catch the CDC events (insert, update, and delete) from MySQL source database and send events to Kinesis stream

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/Python.PNG)

Python script is at Python/mysql_to_kinesis.py



# Step 4: Create a RDS MySQL target database 3 users, wages, and user_wages tables

CREATE TABLE users(user_id INTEGER, first_name VARCHAR(200), last_name VARCHAR(200), PRIMARY KEY (user_id));

CREATE TABLE wages(user_id INTEGER, wage integer, PRIMARY KEY (user_id));

CREATE TABLE user_wages(user_id INTEGER, full_name VARCHAR(200), wage integer, PRIMARY KEY (user_id));

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/RDSMySQL.PNG)



# Step 5: Create an AWS Lambda function with trigger on Kinesis stream and include Python script to consume CDC events to RDS MySQL target database

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/Lambda.PNG)

Lambda Python script is at Python/lambda.py



# Step 6: Insert, update, and delete on MySQL source database. Then check changes on RDS MySQL target database

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/TargetDatabase.PNG)
