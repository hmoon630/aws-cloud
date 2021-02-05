#!/bin/bash
yum update -y
yum install -y python3 pip3 git
cd /home/ec2-user
git clone https://github.com/hmoon630/aws-cloud.git
cd aws-cloud/week2
pip3 install boto3
python3 ./app.py > /home/ec2-user/result.txt
