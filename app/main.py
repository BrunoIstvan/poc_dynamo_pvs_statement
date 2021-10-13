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
        """
        Executa todo o processamento
        :param file_type: Tipo de arquivo
        :return:
        """

        message = []

        # recupera os dados da base
        requests = self.get_requests(file_type)

        # extrai todos os id_requests
        ids_requests = set(pv.id_request for pv in requests)

        # para cada id_request
        for id_request in ids_requests:

            request, statement_request_model = self.extract_request_model(file_type, id_request, requests)

            headquarters, pvs_headquarters = self.extract_headquarters_data(request, requests)

            # para cada matriz
            for headquarter in pvs_headquarters:

                headquarter_model, pvs_establishments = self.extract_establishment_data(headquarter, headquarters)

                # adiciona os pvs filiais na lista de pvs da matriz
                headquarter_model.append_establishments(list(pvs_establishments))

                # adiciona a matriz na lista de matrizes
                statement_request_model.append_headquarter(headquarter_model)

            # adiciona o request model na lista de mensagens
            message.append(statement_request_model)

        # content = json.dumps(message, cls=StatementRequestEncoder)
        # print(content)

        x = 2
        list_of_lists = [message[i:i + x] for i in range(0, len(message), x)]

        for item in list_of_lists:
            item = json.dumps(item, cls=StatementRequestEncoder)
            self.sqs_service.send_message(item)

        return {'result': 'OK'}

    def get_requests(self, file_type):
        """
        Recupera os dados dos id_requests e pvs do banco de dados e
        converte os dados do banco para lista de objetos PvsStatementModel
        :param file_type: Tipo de arquivo
        :return: Dados contendo os requests vindos do banco de dados
        """
        # recupera os dados dos id_requests e pvs do banco de dados
        models = self.dynamo_service.get_pvs_statement(file_type)
        # converte os dados do banco para lista de objetos PvsStatementModel
        requests = PvsStatementModel.get_data(data=models)
        # retorna dados
        return requests

    def extract_establishment_data(self, headquarter, headquarters):
        """
        Monta o model de matriz, recupera todos os models dos estabelecimentos e
        recupera todos os pvs de estabelecimentos
        :param headquarter:
        :param headquarters:
        :return: Model e lista de estabelecimentos
        """
        # monta o model de matriz
        headquarter_model = StatementHeadquarterModel(pv_headquarter=headquarter)

        # recupera todos os models dos estabelecimentos
        establishments = list(filter(lambda e: e.pv_headquarter == headquarter, headquarters))

        # recupera todos os pvs de estabelecimentos
        pvs_establishments = set(pv.pv_establishment for pv in establishments)

        # retorna model e lista de estabelecimentos
        return headquarter_model, pvs_establishments

    def extract_headquarters_data(self, request, requests):
        """
        Recupera as matrizes e extrai todos os pv_headquarters
        :param request:
        :param requests:
        :return: Model e lista de matrizes
        """
        # recupera as matrizes
        headquarters = list(filter(lambda h: h.id_request == request[0].id_request, requests))

        # extrai todos os pv_headquarters
        pvs_headquarters = set(pv.pv_headquarter for pv in headquarters)

        # retorna model e lista de matrizes
        return headquarters, pvs_headquarters

    def extract_request_model(self, file_type, id_request, requests):
        """
        Filtra request pelo id_request e monta objeto que será enviado na fila
        :param file_type: Tipo de arquivo
        :param id_request: Id da solicitação
        :param requests:
        :return: Model e lista de requests
        """
        # filtra request pelo id_request
        request = list(filter(lambda r: r.id_request == id_request, requests))

        # monta objeto que será enviado na fila
        statement_request_model = StatementRequestModel(
            id_request=id_request,
            file_type=file_type,
            pv_requester=request[0].pv_requester
        )

        # retorna model e lista de requests
        return request, statement_request_model
