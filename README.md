# Architecture

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/Architecture.PNG)

Build a data flow as architecture as the following steps:

# Step 1: Prepare a MySQL source database with 2 users and wages tables

CREATE TABLE users(user_id INTEGER, first_name VARCHAR(200), last_name VARCHAR(200), PRIMARY KEY (user_id));

CREATE TABLE wages(user_id INTEGER, wage integer, PRIMARY KEY (user_id));

![alt text](https://github.com/nashtech-garage/logbasedcdc-aws-kinesis/blob/main/Images/SourceDatabase.PNG)
