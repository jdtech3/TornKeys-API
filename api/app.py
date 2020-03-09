import flask
from flask_api import *
from flask_api.status import *
from pony.orm.core import TransactionIntegrityError

from db.db import get_member, create_member
from api.keys import ALLOWED_API_KEYS

app = FlaskAPI(__name__)

__version__ = '0.1.0-beta'


@app.route('/api')
def home():
    return 'TornKeys API v0.1.0-beta'


@app.route('/api/get', methods=['GET'])
def get_info():
    args = flask.request.args

    if args.get('key') in ALLOWED_API_KEYS:
        _id = args.get('id')

        member_by_discord_id = get_member(_id, by='discord_id')
        member_by_torn_id = get_member(_id, by='torn_id')

        if member_by_discord_id is None and member_by_torn_id is None:
            return {'error': 'Invalid Discord ID or Torn ID'}, HTTP_400_BAD_REQUEST

        if member_by_discord_id is not None:
            return {
                'api_key': member_by_discord_id['api_key'],
                'discord_id': member_by_discord_id['discord_id'],
                'torn_id': member_by_discord_id['torn_id']
            }

        if member_by_torn_id is not None:
            return {
                'api_key': member_by_torn_id['api_key'],
                'discord_id': member_by_torn_id['discord_id'],
                'torn_id': member_by_torn_id['torn_id']
            }

    else:
        return {'error': 'Invalid API key'}, HTTP_401_UNAUTHORIZED


@app.route('/api/new', methods=['GET', 'POST'])
def new_member():
    if flask.request.method == 'POST':
        args = flask.request.args

        if args.get('key') in ALLOWED_API_KEYS:
            api_key = args.get('api_key')
            try:
                discord_id = int(args.get('discord_id'))
                torn_id = int(args.get('torn_id'))
            except ValueError:
                return {'error': 'Discord ID and Torn ID must be int'}, HTTP_400_BAD_REQUEST

            try:
                create_member(api_key=api_key, discord_id=discord_id, torn_id=torn_id)
            except TransactionIntegrityError:
                return {'error': 'API key, Discord ID and/or Torn ID already exists'}, HTTP_400_BAD_REQUEST

            return {'success': True}

        else:
            return {'error': 'Invalid API key'}, HTTP_401_UNAUTHORIZED

    return {'error': 'Use POST method to add new records'}, HTTP_400_BAD_REQUEST


if __name__ == '__main__':
    app.run(port=5050)
