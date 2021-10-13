from app.main import Main


def lambda_handler(event, context):

    return Main().execute(file_type=event['file_type'])


# if __name__ == '__main__':
#
#     event = {
#         'file_type': 'EEVD'
#     }
#
#     lambda_handler(event, None)
