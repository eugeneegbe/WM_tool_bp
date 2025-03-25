from wikidata.client import Client
from .utils import make_api_request, build_search_result
from tool import config


def make_wd_api_search_request(type='item', search='', language='en'):
    '''
        make a request to wikidata api 
    '''
    
    own_params = {
        'action': 'wbsearchentities',
        'type': type,
        'search': search,
        'language': language,
        'format': 'json'
    }


    wd_search_results = make_api_request(config['API_URL'], own_params)
    search_result_data = build_search_result(wd_search_results['search'])
    return search_result_data


def get_wikidata_entity_data(ids, props='', languages=''):

    own_params = {
        'action': 'wbgetentities',
        'props': props,
        'languages': languages,
        'ids': ids,
        'format': 'json'
    }

    entityies_data = make_api_request(config['API_URL'], own_params)

    if not entityies_data['entities']:
        return None

    return entityies_data['entities']


def get_entity_data(wd_id):
    try:
        client = Client()
        entity_data = client.get(wd_id, load=True).data
        return entity_data
    except Exception as e:
        return {'message': e.message}


def get_item_label(wd_item, lang_code):

    entity_data = get_entity_data(wd_item)['labels']
    if lang_code not in entity_data.keys():
        return 'Nan'
    else:
        return entity_data[lang_code]['value']
