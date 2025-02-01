"""functions utils"""
import json
from datetime import datetime
from flask import Response, request  # pylint: disable=import-error

class FormatResponse:
    """class to format response"""
    def __init__(self, allowed_origin, app, user_request="", method="GET"):
        self.user_request = user_request
        self.method = method
        self.allowed_origin = allowed_origin
        self.app = app

    def set_user_request(self, user_request):
        """setter"""
        self.user_request = user_request

    def set_method(self, method):
        """setter"""
        self.method = method

    def generate_response(self,code,message,data=None,root=False, log=True): # pylint: disable=too-many-arguments
        """
        Cette fonction permet :
        de structurer la réponse de l'api
        de générer les logs
        de définir les origines autorisées

        elle retourne :
        un objet response
        """
        try:
            allow_origin = json.loads(self.allowed_origin)
        except Exception as exp:  # pylint: disable=W0703
            code = 500
            message = f"ALLOW_ORIGIN must be a JSON list string : {exp}"
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if code // 100 == 2:
            status = "successful"
        else:
            status = "Failed"
        message = f"{message} (api-sentiments-analysis)"
        response = {"status": status, "msg": message}
        if log is True:
            self.app.logger.info(
                "datetime=%s,request=%s,status code=%s,reponse=%s,message=%s",
                dt_string, self.user_request, code, response, message
            )
        if root is True:
            response = data
        else:
            if isinstance(data, dict):
                response = {**response, **data}
            else:
                response["data"] = data

        response_json = json.dumps(response)
        response = Response(response_json, status=code, mimetype='application/json')
        origin = request.headers.get('Origin')
        if origin is not None and (origin in allow_origin):
            response.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = self.method
        return response
