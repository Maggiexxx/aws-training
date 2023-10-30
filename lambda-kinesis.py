import json 
import boto3
import base64

def send_to_s3 (data, SequenceNumber):
    s3 = boto3.client('s3')
    file_name=f"{SequenceNumber}.json"
    s3_path="send_to_s3_data/"+file_name
    bucket = "myawstraining-setup-bucket"
    response = s3.put_object(Body=data,Bucket=bucket,Key=s3_path)
    return response

def lambda_handler (event, context):
    print (f"event: {event}")
    for record in event[ "Records"]:
        encoded_data=record["kinesis"]["data"] 
        decoded_data=base64.b64decode(encoded_data)
        print(f"decoded_data: {decoded_data}")
        print(type(decoded_data))
        desire_data=json.loads(decoded_data) 
        print(f"data : {desire_data}")
        print(type(desire_data))

        SequenceNumber=record["kinesis"]["sequenceNumber"] 
        result=send_to_s3(decoded_data,SequenceNumber)
        print(f"DUMP DATA TO S3 BUCKET: {result}")