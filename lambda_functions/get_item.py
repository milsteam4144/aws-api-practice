import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MEMBERS')
    
def lambda_handler(event, context):
    try:
        response = table.get_item(Key=event)
        return response["Item"]
    except:
        return ("No item matching that description exists")