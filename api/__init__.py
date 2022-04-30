"""
Author: Dhruva Agrawal
Author E-mail: dhruva_agrawal@outlook.com
"""

from flask import Blueprint
import json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/health', methods=['GET'])
def health():
    return json.dumps({
        'status': 200,
        'body': { 'message': 'Health check API.' }
    })

