def lambda_handler(event, context):
    # TODO implement
    import uuid
    import boto3
    from botocore.exceptions import ClientError
    #print ("this is the event {}".format(event))
    message = event['Records'][0]['Sns']['Message']
    myuuid = uuid.uuid4()

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserPasswordReset')
    title = "The Big New Movie"
    year = 2015

    response = table.put_item(
    Item={
            'id': message,
            'uuid': str(myuuid)
        }
    )

    SENDER = "Sender Name <noreply@csye6225-spring2018-guraoa.me>"
    RECIPIENT =  message
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
    #print ("the ses event is {}".format(ses_event.get_identity_mail_from_domain_attributes(['Identities'])))

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
    
