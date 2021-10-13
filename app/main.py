import json

from app.dynamo_service import DynamoService
from app.models.PvsStatementModel import PvsStatementModel
from app.models.StatementHeadquarterModel import StatementHeadquarterModel
from app.models.StatementRequestModel import StatementRequestModel, StatementRequestEncoder
from app.sqs_service import SQSService


class Main(object):

    def __init__(self):
        self.dynamo_service = DynamoService()
        self.sqs_service = SQSService()

    def execute(self, file_type):

        message = []

        # recupera os dados dos id_requests e pvs do banco de dados
        models = self.dynamo_service.get_pvs_statement(file_type)

        # converte os dados do banco para lista de objetos PvsStatementModel
        requests = PvsStatementModel.get_data(data=models)

        # extrai todos os id_requests
        ids_requests = set(pv.id_request for pv in requests)

        # para cada id_request
        for id_request in ids_requests:

            request = list(filter(lambda r: r.id_request == id_request, requests))

            # monta objeto que será enviado na fila
            statement_request_model = StatementRequestModel(
                id_request=id_request,
                file_type=file_type,
                pv_requester=request[0].pv_requester
            )

            # recupera as matrizes
            headquarters = list(filter(lambda h: h.id_request == request[0].id_request, requests))

            # extrai todos os pv_headquarters
            pvs_headquarters = set(pv.pv_headquarter for pv in headquarters)

            # para cada matriz
            for headquarter in pvs_headquarters:

                # monta o model de matriz
                headquarter_model = StatementHeadquarterModel(pv_headquarter=headquarter)

                # recupera todos os models dos estabelecimentos
                establishments = list(filter(lambda e: e.pv_headquarter == headquarter, headquarters))
                # recupera todos os pvs de estabelecimentos
                pvs_establishments = set(pv.pv_establishment for pv in establishments)
                # adiciona os pvs filiais na lista de pvs da matriz
                headquarter_model.append_establishments(list(pvs_establishments))
                # adiciona a matriz na lista de matrizes
                statement_request_model.append_headquarter(headquarter_model)

            # adiciona o request model na lista de mensagens
            message.append(statement_request_model)

        print(json.dumps(message, cls=StatementRequestEncoder, indent=4))

        return {'result': 'OK'}
