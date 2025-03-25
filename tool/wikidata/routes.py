from flask import Blueprint, request, jsonify
from .wikidata import make_wd_api_search_request, get_wikidata_entity_data
from .languages import getLanguages

wikidata = Blueprint('wikidata', __name__)


@wikidata.route('/api/v1/search', methods=['GET', 'POST'])
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


@wikidata.route('/api/v1/get-items')
def get_items_data():

    try:
        ids = request.args.get('ids')
        languages = request.args.get('languages')

        entity_data = get_wikidata_entity_data(languages=languages, ids=ids)
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
