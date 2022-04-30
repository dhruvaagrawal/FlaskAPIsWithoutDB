"""
Author: Dhruva Agrawal
Author E-mail: dhruva_agrawal@outlook.com
"""

from flask import Blueprint, request, Response
import json

from utils import difference_between_lists
from utils.entity import fetch_entity_details, fetch_entity_list
from utils.update_entity import update_entity_details
from utils.users import create_user_entry, fetch_team_detail_from_user

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('', methods=['POST'])
def create_user() -> str:
    """
    :param request_body: A json string with the user details
    {
      "name" : "<user_name>",
      "display_name" : "<display name>"
    }
    :return: A json string with the response {"id" : "<user_id>"}

    Constraint:
        * name must be unique
        * name can be max 64 characters
        * display name can be max 64 characters
    """
    body = json.loads(request.get_data())
    request_param_keys_needed = ['name', 'display_name']
    diff_list = difference_between_lists(list(body.keys()), request_param_keys_needed)
    if len(diff_list) == 0:
        is_user_name_verified, user_id, error_message = create_user_entry(body)
        if is_user_name_verified:
            response = {
                'status': 201,
                'body': {
                    'error': {},
                    'id': user_id
                }
            }
        else:
            response = {
                'status': 400,
                'body': {
                    'error': {'args': error_message},
                    'message': 'Invalid details provided.'
                }
            }
    else:
        response = {
            'status': 400,
            'body': {
                'error': {'args': diff_list},
                'message': 'Incorrect number of parameters provided.'
            }
        }
    return json.dumps(response)


@users.route('', methods=['GET'])
def list_users() -> str:
    """
    :return: A json list with the response
    [
      {
        "name" : "<user_name>",
        "display_name" : "<display name>",
        "creation_time" : "<some date:time format>"
      }
    ]
    """
    user_list = fetch_entity_list(entity_type='user')
    response = {
        'status': 200,
        'body': {
            'error': {},
            'users': user_list
        }
    }
    return json.dumps(response)


@users.route('/<string:id>', methods=['GET'])
def describe_user(id) -> str:
    """
    :param id: team_id

    :return: A json string with the response
    {
      "name" : "<user_name>",
      "description" : "<some description>",
      "creation_time" : "<some date:time format>"
    }
    """
    user_info = fetch_entity_details(entity_type='user', id=id)
    response = {
        'status': 200,
        'body': {
            'error': {},
            'user_info': user_info
        }
    }
    return json.dumps(response)


@users.route('/<string:id>', methods=['PUT'])
def update_user(id) -> str:
    """
    :param id: user_id
    :param request: A json string with the user details
      {
        "name" : "<user_name>",
        "display_name" : "<display name>"
      }
    :return:

    Constraint:
        * name cannot be updated
        * name can be max 64 characters
        * display name can be max 128 characters
    """
    body = json.loads(request.get_data())
    request_param_keys_needed = ['name', 'display_name']
    diff_list = difference_between_lists(list(body.keys()), request_param_keys_needed)
    if len(diff_list) == 0:
        is_user_name_verified, error_message = update_entity_details(entity_type='user', entity_details=body, id=id)
        if is_user_name_verified:
            response = {
                'status': 201,
                'body': {
                    'error': {},
                    'id': id
                }
            }
        else:
            response = {
                'status': 400,
                'body': {
                    'error': {'args': error_message},
                    'message': 'Invalid details provided.'
                }
            }
    else:
        response = {
            'status': 400,
            'body': {
                'error': {'args': diff_list},
                'message': 'Incorrect number of parameters provided.'
            }
        }
    return json.dumps(response)


@users.route('/<string:id>/teams', methods=['GET'])
def get_user_teams(id) -> str:
    """
    :param id: User ID

    :return: A json list with the response.
    [
      {
        "name" : "<team_name>",
        "description" : "<some description>",
        "creation_time" : "<some date:time format>"
      }
    ]
    """
    team_list = fetch_team_detail_from_user(id=id)
    response = {
        'status': 200,
        'body': {
            'error': {},
            'teams': team_list
        }
    }
    return json.dumps(response)
