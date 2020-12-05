"""
WebServer utilities
"""

import json
import traceback

from tornado import web, httpserver


class ServiceException(web.HTTPError):
    pass


class ServiceEndpoint(web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, DELETE, PUT, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Origin, Content-Type, Accept, Authorization, X-Request-With")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Content-Type', 'application/json')

    def data_received(self, chunk):
        pass

    def options(self, *args, **kwargs):
        self.set_status(200)
        self.finish()

    def write_error(self, status_code, **kwargs):
        """
            Returns a JSON error to the user. (with traceback in case debug is set to true)
        :param status_code:
        :param kwargs:
        :return:
        """
        self.set_header('Content-Type', 'application/json')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self.finish(json.dumps({
                'error': {
                    'code': status_code,
                    'message': self._reason,
                    'traceback': lines,
                }
            }))
        else:
            self.finish(json.dumps({
                'error': {
                    'code': status_code,
                    'message': self._reason,
                }
            }))


class ServerStartUp:
    def __init__(self, service_name=None):
        print(f"Service {service_name} starting up...")

    def start(self, application):
        server = httpserver.HTTPServer(application)

        return server
