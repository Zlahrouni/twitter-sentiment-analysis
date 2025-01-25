"""
functions to get vm env
"""
from flask import request #pylint: disable=import-error
from modele.check_feeling import check_feeling as checkFeeling
from utils.errors.errors import (
    ExternalTypeError,
    ExternalValueError
)



def check_feeling():
    """
    check vars env of check_feeling
    """

    feeling_list = request.json.get('feeling')
    if len(feeling_list) == 0:
        raise ExternalValueError("feeling must be a defined")
    if not isinstance(feeling_list, list):
        raise ExternalTypeError("feeling must be a list")


    return checkFeeling(feeling=feeling_list)
