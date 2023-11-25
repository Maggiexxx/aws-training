import json
import smtplib
import os
import boto3
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "smtp.gmail.com"
smtp_port = 465

smtp_username = "maggiexiang412@gmail.com"
smtp_password = "esmk iogm lhiv fvhs"

send_to = "maggiex412@gmail.com"
send_from = "maggiexiang412@gmail.com"

def send_email(msg):
    
    message = msg
    
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_username, smtp_password)
    
    server.sendmail(send_from, send_to, message)
    server.quit()


def lambda_handler(event, context):
    
    print(f'body: {event}')
    
    for Record in event["Records"]:
        body = Record['body']
        deser_body =json.loads(body)
        message = deser_body ['Message']

        send_email(message) 
        send_to_sns(message)

def send_to_sns(msg):
    client = boto3.client('sns')
    snsArn = 'arn:aws:sns:us-east-1:163713723397:Ca-Send-Email-Topic'

    response = client.publish(
        TopicArn = snsArn,
        Message = msg,
        Subject = 'Schema Change Detected'
    )