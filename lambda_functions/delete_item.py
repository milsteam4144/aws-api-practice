import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MEMBERS')
    
def lambda_handler(event, context):
    try:
        response = table.delete_item(Key=event)
        return ("Member successfully deleted")
    except:
        return ("Coud not locate or delete member")