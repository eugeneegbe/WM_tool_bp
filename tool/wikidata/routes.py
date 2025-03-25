from flask import Blueprint, request, jsonify
from .wikidata import (make_wd_api_search_request, get_wikidata_entity_data,
                       get_wikidata_entity_statement_props)
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


@wikidata.route('/api/v1/item/statements', methods=['GET', 'POST'])
def get_item_claims():

    try:
        id = request.args.get('id')
        property = request.args.get('property')
        statements = get_wikidata_entity_statement_props(id=id, property=property)
        return jsonify([statements])
    except Exception as e:
        return jsonify({'error': str(e)})
