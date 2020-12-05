import tornado.web
import tornado.escape
import json

from helpers.WebServerHelper import ServiceEndpoint, ServiceException

class WorkflowCreationService(ServiceEndpoint):

    def initialize(self, api_cfg):
        self.api_cfg = api_cfg

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            arg1= json_request["arg1"]
            deploy_file_name = json_request.get("optional_arg", None)
        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)

        res = {
            "key": arg1
        }
        return json.dumps(res)
