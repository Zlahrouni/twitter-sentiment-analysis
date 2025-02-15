"""
common functions for api
"""

import json
from datetime import datetime
import re
import requests
from utils.errors.errors import (
    InternalError,
    InternalValueError,
    WrongTokenError,
    CallApiError,
    CallApiAuthError,
    NotFoundError
)

def format_datetime_in_yaml(data):
    """
    Cette fonction permet :
    de convertir mes formats date en chaine de caractère dans un yaml
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.strftime('%Y-%m-%dT%H:%M:%S')
            elif isinstance(value, (list, dict)):
                format_datetime_in_yaml(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):  # pylint: disable=W0612
            format_datetime_in_yaml(item)
    return data

def is_cidr(input_str):
    """
    Cette fonction permet :
    de vérifier que la chaine donnee respect bien le format cidr
    """
    cidr_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$'
    return bool(re.match(cidr_pattern, input_str))

def get_intersection(list1,list2):
    """
    utilisation des ensemble
    afin de trouver les elements communs de deux listes
    """
    try:
        set1 = set(list1)
        set2 = set(list2)
        return list(set1.intersection(set2))
    except Exception as exp:  # pylint: disable=W0703
        raise InternalError(f"error while getting lists intersection : {exp}") from exp

def http_manager(
    url,
    headers,
    detail,
    mode="get",
    timeout=5,
    data=None,
    params=None,
    auth=None
):  # pylint: disable=too-many-arguments, too-many-branches
    """
    gestionnaire de requete centralise
    """
    try:
        if data is not None:
            data = json.dumps(data)
        if mode == "get":
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout,
                data=data,
                params=params,
                auth=auth
                )
        elif mode == "post":
            response = requests.post(
                url,
                headers=headers,
                timeout=timeout,
                data=data,
                params=params,
                auth=auth
            )
        elif mode == "put":
            response = requests.put(
                url,
                headers=headers,
                timeout=timeout,
                data=data,
                params=params,
                auth=auth
            )
        elif mode == "delete":
            response = requests.delete(
                url,
                headers=headers,
                timeout=timeout,
                data=data,
                params=params,
                auth=auth
            )
        else:
            raise InternalValueError("mode non gere par le http manager")
        code = response.status_code
        if code == 204:
            response_data = None
        else:
            response_data = response.json()
        request_error_manager(
            code=code,
            response_data=response_data
        )
        return response_data
    except CallApiError as exp:
        raise CallApiError(exp) from exp
    except CallApiAuthError as exp:
        raise CallApiAuthError(exp) from exp
    except InternalValueError as exp:
        raise InternalValueError(exp) from exp
    except ValueError as exp:
        raise InternalValueError(
            f"Impossible de decoder la reponse {detail} : {response.reason} {exp}"
        ) from exp
    except TimeoutError:
        raise TimeoutError(f"Timeout lors {detail}") from exp
    except WrongTokenError as exp:
        raise WrongTokenError(f"Token invalide lors {detail} : {exp}") from exp
    except requests.exceptions.RequestException as exp:
        raise CallApiError(f"Erreur lors {detail} : {exp}") from exp
    except Exception as exp:  # pylint: disable=W0703
        raise CallApiError(f"Erreur lors {detail} : {exp}") from exp

def request_error_manager(code,response_data):
    """error handler for http requests"""
    if code == 401:
        raise WrongTokenError(
            response_data.get("msg", "wrongTokenError")
        )
    if code == 403:
        raise CallApiAuthError(
            response_data.get("msg", "CallApiAuthError")
        )
    if code == 404:
        raise NotFoundError(
            response_data.get("msg", "NotFoundError")
        )
    if code > 299:
        raise CallApiError(
            response_data.get("msg", "CallApiError")
        )
