"""
Docs API

"""

import os
import sys
import logging
from flask import Flask, request #pylint: disable=import-error
import bdd.managers
from bdd.mysql import MySQLManager
from utils.format_response import FormatResponse
from utils.check_env import (
    check_env_exists,
    check_env_is_json
)
from utils.error_handlers.error_handlers import register_error_handlers
from utils.error_handlers.mysql_error_handlers import register_mysql_error_handlers
app = Flask(__name__)

#####             recupération des logs                #####
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

required_variables = [
    "ALLOW_ORIGIN",
    "MYSQL_DATABASE",
    "MYSQL_ROOT_PASSWORD",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_ROOT_HOST",
]

# all json env vars
json_required_variables = [
    "ALLOW_ORIGIN"
]

# check existence of env var
error = check_env_exists(required_variables)
if error is not None:
    app.logger.error(error)
    sys.exit(70)

# check if all json env vars are valid json
error = check_env_is_json(json_required_variables)
if error is not None:
    app.logger.error(error)
    sys.exit(70)

###IMPORT FUNCTIONS IF ENV IS VALID

from controller.feelings import ( # pylint: disable=wrong-import-position
    check_feeling as check_feeling_ctr,
)

### DATABASE ###
# MYSQL 

MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_ROOT_HOST = os.environ.get("MYSQL_ROOT_HOST")

### CONFIG ###
ALLOW_ORIGIN = os.environ.get("ALLOW_ORIGIN").replace('\\"', '"')
DEBUG = os.environ.get("DEBUG_MODE", False)
DEBUG = str(DEBUG).lower()
DEBUG = bool(DEBUG in ['true', '1', 'yes','oui'])

# Initialize responser
FORMAT_RESPONSE = FormatResponse(
    allowed_origin=ALLOW_ORIGIN,
    app=app
)

@app.before_request
def before_request_func():
    """
    Check bdd connexions
    """
    if bdd.managers.MYSQL_CLIENT is None:
        bdd.managers.MYSQL_CLIENT = MySQLManager(
            host="localhost",
            user=MYSQL_USER, 
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        print("instanciate mysql manager")
    if not bdd.managers.MYSQL_CLIENT.is_connected():
        bdd.managers.MYSQL_CLIENT.connect()
        print("connected to mysql")


@app.route("/ping/", methods=["GET"])
def get_ping():
    """
    Cette fonction permet
    de tester l'api
    """
    return '{"success":true}', 200, {'ContentType':'application/json'}

@app.route('/check_feeling/', methods=['POST'])
def check_feeling():
    """
    check feeling with modeles ia
    """
    FORMAT_RESPONSE.set_user_request("POST /check_feeling/")
    FORMAT_RESPONSE.set_method("POST")

    list_feeling = check_feeling_ctr()

    return FORMAT_RESPONSE.generate_response(
        code=200,
        message="Feelings getted",
        data=list_feeling
    )

register_error_handlers(app, FORMAT_RESPONSE)
register_mysql_error_handlers(app, FORMAT_RESPONSE)

if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=8080)
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
