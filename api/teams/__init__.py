"""
Author: Dhruva Agrawal
Author E-mail: dhruva_agrawal@outlook.com
"""

from flask import Blueprint, request, Response
import json

from utils import difference_between_lists
from utils.entity import fetch_entity_list, fetch_entity_details
from utils.teams import create_team_entry, create_users_for_team, fetch_user_list_from_team, delete_users_from_team
from utils.update_entity import update_entity_details

teams = Blueprint('teams', __name__, url_prefix='/teams')


@teams.route('', methods=['POST'])
def create_team() -> str:
    """
    :param request_body: A json string with the team details
    {
      "name" : "<team_name>",
      "description" : "<some description>",
      "admin": "<id of a user>"
    }
    :return: A json string with the response {"id" : "<team_id>"}

    Constraint:
        * Team name must be unique
        * Name can be max 64 characters
        * Description can be max 128 characters
    """
    body = json.loads(request.get_data())
    request_param_keys_needed = ['name', 'description', 'admin']
    diff_list = difference_between_lists(list(body.keys()), request_param_keys_needed)
    if len(diff_list) == 0:
        is_team_name_verified, team_id, error_message = create_team_entry(body)
        if is_team_name_verified:
            response = {
                'status': 201,
                'body': {
                    'error': {},
                    'id': team_id
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


@teams.route('', methods=['GET'])
def list_teams() -> str:
    """
    :return: A json list with the response.
    [
      {
        "name": "<team_name>",
        "description": "<some description>",
        "creation_time": "<some date:time format>",
        "admin": "<id of a user>"
      }
    ]
    """
    team_list = fetch_entity_list(entity_type='team')
    response = {
        'status': 200,
        'body': {
            'error': {},
            'teams': team_list
        }
    }
    return json.dumps(response)


@teams.route('/<string:id>', methods=['GET'])
def describe_team(id) -> str:
    """
    :param id: team_id

    Response: A json string with the response
    {"name":"<team_name>", "description":"<some description>", "creation_time":"<some date:time format>", "admin": "<id of a user>"}

    """
    team_info = fetch_entity_details(entity_type='team', id=id)
    response = {
        'status': 200,
        'body': {
            'error': {},
            'team_info': team_info
        }
    }
    return json.dumps(response)


@teams.route('/<string:id>', methods=['PUT'])
def update_team(id) -> str:
    """
    :param id: team_id
    :param request_body: A json string with the team details
      {
        "name" : "<team_name>",
        "description" : "<team_description>",
        "admin": "<id of a user>"
      }
    :return:

    Constraint:
        * Team name must be unique
        * Name can be max 64 characters
        * Description can be max 128 characters
    """
    body = json.loads(request.get_data())
    request_param_keys_needed = ['name', 'description', 'admin']
    diff_list = difference_between_lists(list(body.keys()), request_param_keys_needed)
    if len(diff_list) == 0:
        is_team_name_verified, error_message = update_entity_details(entity_type='team', entity_details=body, id=id)
        if is_team_name_verified:
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


@teams.route("/<string:id>/users", methods=['POST'])
def add_users_to_team(id):
    """
    :param id: Team ID
    :param request: A json string with the team details
    {
      "users" : ["user_id 1", "user_id2"]
    }

    :return:

    Constraint:
    * Cap the max users that can be added to 50
    """
    body = json.loads(request.get_data())
    user_list = body['users']
    if len(user_list) <= 50:
        is_created, error_message = create_users_for_team(id=id, user_list=user_list)
    else:
        response = {
            'status': 400,
            'body': {
                'error': {'args': len(user_list)},
                'message': 'The provided number of users exceed the max limit of 50.'
            }
        }


@teams.route('/<string:id>/users', methods=['GET'])
def list_team_users(id):
    """
    :param id: Team ID

    :return:
    [
      {
        "id" : "<user_id>",
        "name" : "<user_name>",
        "display_name" : "<display name>"
      }
    ]
    """
    team_list = fetch_user_list_from_team(id=id)
    response = {
        'status': 200,
        'body': {
            'error': {},
            'teams': team_list
        }
    }
    return json.dumps(response)


@teams.route('/<string:id>/users', methods=['DELETE'])
def remove_users_from_team(id):
    """
    :param id: Team ID
    :param request: A json string with the team details
    {
      "users" : ["user_id 1", "user_id2"]
    }

    :return:
    """
    body = json.loads(request.get_data())
    user_list = body['users']
    delete_users_from_team(id=id)
    response = {
        'status': 204,
        'body': {
            'error': {},
            'message': f'These users have been successfully removed: {", ".join(user_list)}'
        }
    }
