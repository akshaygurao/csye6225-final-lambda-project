def lambda_handler(event, context):
    # TODO implement
    import uuid
    import boto3
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
            'email': 'vighnesh@gmail.com',
            'uuid': str(myuuid)
        }
    )

    print("PutItem succeeded:")
    print(response)
    #context.getLogger().log("1",event.getRecords().size())
    return 'Hello from Lambda'
    
