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

message_to_send = "hello world"

def send_email(msg):
    print("this is from smptlib")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_username, smtp_password)
    message = f"""From: {send_to}
To: {send_to}
Subject: Test message

{msg}."""
    server.sendmail(send_from, send_to, message)
    server.quit()


def smtp_send_email(res,acc,reg, db, tb, ch):

    send_to = "maggiex412@gmail.com"
    send_from = "maggiexiang412@gmail.com"    

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Schema Change Detected in Another Region"
    msg['From'] = send_from
    msg['To'] = send_to
    # Create the body of the message (a plain-text and an HTML version).

    html = """\
    <html>
      <head></head>
      <body>
        <p>Schema Change Detected from cross region<br>
            <br>
            Resources is: {resources} <br><br>
            Account is: {account} <br><br>
            Region is: {region} <br><br>
            Database Name is: {databaseName} <br><br>
            Table Name is: {tableName} <br><br>
            Change is: {change} <br><br> 
        </p> 
      </body> 
    </html>
    """.format(resources=res, account= acc, region=reg, databaseName =db, tableName=tb, change=ch)

    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    #Send the message via local SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "maggiexiang412@gmail.com"
    smtp_password = "7781 9662"
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_username, smtp_password)

    server.sendmail(send_from, send_to, msg.as_string())
    server.quit()

def lambda_handler(event, context):
    
    print(f'body: {event}')
    
    for Record in event["Records"]:
        body = Record['body']
        deser_body =json.loads(body)
        message = deser_body ['Message']
        deser_message = json.loads(message)
        resources = deser_message ['resources'][0]
        account = deser_message ['account']
        region = deser_message ['region']
        detail = deser_message ['detail']
        databaseName = deser_message ['detail']['databaseName']
        tableName = deser_message ['detail']['tableName']
        change = deser_message ['detail' ]['typeOfChange']

        smtp_send_email(resources, account, region, databaseName, tableName, change) 
        send_to_sns(change)

def send_to_sns(msg):
    client = boto3.client('sns')
    snsArn = 'arn:aws:sns:us-east-1:163713723397:Ca-Send-Email-Topic'

    response = client.publish(
        TopicArn = snsArn,
        Message = msg,
        Subject = 'Cross Region Schema Change Detected'
    )