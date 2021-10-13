import boto3
from boto3.dynamodb.conditions import Key


class DynamoService(object):

    def __init__(self):
        self.resource = boto3.resource('dynamodb')

    def get_resource(self):
        return self.resource

    def get_pvs_statement(self, file_type):
        table = self.resource.Table('PvsStatement')

        response = table.query(
            KeyConditionExpression=Key('fileType').eq(file_type)
        )

        return response['Items']
