def lambda_handler(event, context):
    # TODO implement
    import uuid
    import boto3
    from botocore.exceptions import ClientError
    myuuid = uuid.uuid4()
    print('Hello from lambda')
    print("My uuid is",myuuid)
    print(event)
    print("____________________________")
    print(context.aws_request_id)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserPasswordReset')
    title = "The Big New Movie"
    year = 2015

    response = table.put_item(
    Item={
            'id': event["email"],
            'uuid': str(myuuid)
        }
    )

    print("PutItem succeeded:")
    print(response)
    #context.getLogger().log("1",event.getRecords().size())





    SENDER = "Sender Name <gurao.a@husky.neu.edu>"
    RECIPIENT =  event["email"]
    AWS_REGION = "us-east-1"
    SUBJECT = "Amazon SES Test (SDK for Python)"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """
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
    else:
        print("Email sent! Message ID:"),
    print(response['ResponseMetadata']['RequestId'])


    return 'Hello from Lambda'
    
