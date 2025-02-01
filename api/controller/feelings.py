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
    new_tweets_list = request.json.get('new_tweets', [])
    if len(new_tweets_list) == 0:
        raise ExternalValueError("new_tweets must be a defined")
    if not isinstance(new_tweets_list, list):
        raise ExternalTypeError("new_tweets must be a list")

    return checkFeeling(new_tweets=new_tweets_list)
