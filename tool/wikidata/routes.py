from flask import Blueprint, request, jsonify, session
from .wikidata import (make_wd_api_search_request, get_wikidata_entity_data,
                       make_wikidata_edit)
from .languages import getLanguages
from tool import config

from tool.models import User


wikidata = Blueprint('wikidata', __name__)


@wikidata.route('/api/v1/search', methods=['POST'])
def get_search_Items():
    term = request.args.get('term')
    type = request.args.get('type')
    language = request.args.get('language')

    if term is None and type is None:
        return jsonify({'message': 'Please add language and/or a search term'}), 403

    try:
        search_data = make_wd_api_search_request(language=language, search=term, type=type)
        return  jsonify(search_data)
    except Exception as e:
        return jsonify({'error': str(e)})


@wikidata.route('/api/v1/items')
def get_items_data():

    try:
        ids = request.args.get('ids')
        languages = request.args.get('languages')
        props = request.args.get('props')
        entity_data = get_wikidata_entity_data(languages=languages, ids=ids, props=props)
        return jsonify([entity_data])

    except Exception as e:
        return jsonify({'error': str(e)})


@wikidata.route('/api/v1/languages', methods=['GET', 'POST'])
def get_languages():

    try:
        languages = getLanguages()
        return jsonify(languages)
    except Exception as e:
        return jsonify({'error': str(e)})


@wikidata.route('/api/v1/edit', methods=['POST'])
def postContribution():

    latest_base_rev_id = 0

    id = request.form.get('id')
    action = request.form.get('action')
    language = request.form.get('language')
    lang_label = request.form.get('l18n')
    upload_file = request.files['data'].read() if request.files else b''

    file_name = request.files['data'].filename if request.files else None
    data = upload_file if action == 'wbsetclaim' else request.form.get('data')

    valid_actions = [
        'wbsetclaim',
        'wbsetlabel',
        'wbsetdescription'
    ]

    if action not in valid_actions:
        jsonify({'message': 'Incorrect edit type'}, 401)

    try:
        # are you tracking contributions? - create one here
        n = 0

    except Exception as e:
        return jsonify(str(e))
    auth_obj = {
        "consumer_key": config['CONSUMER_KEY'],
        "consumer_secret": config['CONSUMER_SECRET'],
        "access_token": session.get('access_token')['key'],
        "access_secret": session.get('access_token')['secret'],
    }

    latest_edit_info = make_wikidata_edit(session['username'], language, id, lang_label,
                       file_name, data, action, auth_obj)
    
    if not latest_edit_info.get('rev_id'):
        jsonify({'message': 'failure'}, 401)

    # keep last based rev info in session
    session['last_rev'] = latest_edit_info
    # attempt to save contribtion

    return jsonify(str(latest_base_rev_id), 200)


@wikidata.route('/api/v1/lastrev', methods=['GET'])
def get_last_user_rev():

    try:
        return jsonify(session.get('last_rev'))

    except Exception as e:
        return jsonify({'error': str(e)})
