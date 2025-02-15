"""functions utils"""
import os
import json

def check_env_exists(required_variables):
    """Function to check if env var exits"""
    missing_variables = [variable for variable in required_variables if not variable in os.environ]
    if missing_variables:
        error = f"Missing params: {', '.join(missing_variables)}"
        return error
    return None

def check_env_is_json(json_required_variables):
    """Function to check if env var is a valid json"""
    missing_variables = []
    for variable in json_required_variables:
        try:
            json.loads(os.environ[variable].replace('\\"', '"'))
        except:  # pylint: disable=bare-except
            missing_variables.append(variable)
    if len(missing_variables) > 0:
        error = f"Following vars must be valid json: {', '.join(missing_variables)}"
        return error
    return None
