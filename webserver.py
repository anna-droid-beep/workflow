import logging.config
import sys

from tornado.ioloop import IOLoop

from helpers.WebServerHelper import ServerStartUp
from helpers.FileHelper import load_config
from api_gateway.APIGateway import APIGateway


logging.config.fileConfig('config/log.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)


def main():
    """
    Runs the API webserver.
    """

    api_cfg = load_config('config/config.json')
    server = ServerStartUp(service_name=api_cfg.API_GATEWAY_NAME)

    application = APIGateway(api_cfg)

    log.info(f"Starting {api_cfg.API_GATEWAY_NAME} on port {api_cfg.PORT_NUMBER}")
    server = server.start(application)
    server.listen(api_cfg.PORT_NUMBER)
    IOLoop.current().start()


if __name__ == "__main__":
    sys.exit(int(main() or 0))
