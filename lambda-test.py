import uuid
import boto3
import os
from botocore.exceptions import ClientError
import datetime
import time


def lambda_handler(event, context):
    #get email id as message from sns
    message = event['Records'][0]['Sns']['Message']
    try:
        myuuid = str(uuid.uuid4())
        now = int(time.time())
        #print (now)
        ttl_time = int(now + 60*2) #make this 20 later on. just 2 for testing
        #initialize dynamodb
        print(now)
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('csye6225')
        response = table.put_item(Item={'ID':message,'token':myuuid,'ttl':ttl_time},ConditionExpression= "(ID = :id AND #t < :now) OR (ID <> :id)",ExpressionAttributeNames={"#t": "ttl"},ExpressionAttributeValues={":id" : message, ":now" : now})
        make_email(message,myuuid)
    except ClientError as e:
        print (e)
        if (e.response['Error']['Code']) == 'ConditionalCheckFailedException':
            print ("Active token already exists in the database")
        else:
            print ("Please contact Administrator")


def make_email(message,myuuid):
    mysender = "notifyme@" + os.environ['domain']
    SENDER = "Sender Name <" + mysender +  ">"
    password_reset_link = "http://" + os.environ['domain'] + "/reset?email=" + message + "&token=" + myuuid
    #print ("Password reset link", password_reset_link)
    RECIPIENT =  message
    AWS_REGION = "us-east-1"
    SUBJECT = "Amazon SES Test (SDK for Python)"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto)."
                )
    BODY_HTML = """
    <html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    <p> Your password reset link is : <a href={code}> Password Reset Link</a> </p>
    </p>
    </body>
    </html>
                """.format(code = password_reset_link)
    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,

        )

    except ClientError as e:
        print(e.response['Error']['Message'])
