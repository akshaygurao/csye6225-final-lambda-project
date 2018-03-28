def lambda_handler(event, context):
    import uuid
    import boto3
    import os
    from botocore.exceptions import ClientError

    #get email id as message from sns
    message = event['Records'][0]['Sns']['Message']
    #print(message)

    #generate uuid
    myuuid = uuid.uuid4()

    #initialize dynamodb
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserPasswordReset')


    #check if email id exists in dynamodb
    email_id = ''
    try:
        email_id = table.get_item(hash_key=message)
        print(email_id)
    except:
        email_id = ''

    if email_id != '':
        print("Email id exists in dynamo db")
        return "No action required"

    else:
        response = table.put_item(
        Item={
            'id': message,
            'uuid': str(myuuid)
            }
        )
#    "Sender Name <noreply@csye6225-spring2018-guraoa.me>"
        mysender = "no-reply@" + os.environ['domain']
        SENDER = "Sender Name <" + mysender +  ">"
        print("Sender",SENDER)
        password_reset_link = "http://" + os.environ['domain'] + "/reset?email=" + message + "token=" + str(uuid)
        print("Password reset link", password_reset_link)
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
        <p> Your password reset link is : </p>
        """
        + "<a href = ' " + password_reset_link + " '> Password Reset Link</a>"
        """
        </p>
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
