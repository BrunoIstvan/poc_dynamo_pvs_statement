import boto3


class SQSService(object):

    def __init__(self):
        self.client = boto3.client('sqs')

    def send_message(self, content):
        response = self.client.send_message(QueueUrl='sqs-test', MessageBody=content)
        return response['MessageId']
