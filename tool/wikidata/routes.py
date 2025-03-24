from flask import Blueprint, request, jsonify
from .search import make_wd_api_search_request


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
