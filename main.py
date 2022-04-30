"""
Author: Dhruva Agrawal
Author E-mail: dhruva_agrawal@outlook.com
"""

import json

from app import create_app
from utils import create_dbs

app = create_app()


@app.route('/', methods=['GET'])
def main():
    return json.dumps({
        'status': 200,
        'body': { 'message': 'Service is up and running.' }
    })


@app.route('/site-map', methods=['GET'])
def site_map():
    return app.url_map


if __name__ == '__main__':
    create_dbs()
    app.run(debug=True, port=5008)

