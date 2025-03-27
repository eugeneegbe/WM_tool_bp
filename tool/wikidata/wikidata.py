import requests
from wikidata.client import Client
from .utils import make_api_get_request, build_search_result, make_api_post_request
from tool.main.utils import generate_csrf_token
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


    wd_search_results = make_api_get_request(config['API_URL'], own_params)
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

    entityies_data = make_api_get_request(config['API_URL'], own_params)

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


def build_edit_params(username, language, id, lang_label, file_name,
                      data, action, auth_object, csrf_token):
    base_params = {
        'format': 'json',
        'token': csrf_token,
        'summary': username + '@' + config['APP_NAME']
    }

    if action in ['wbsetlabel', 'wbsetdescription']:
        base_params['action'] = action
        base_params['language'] = language
        base_params['value'] = data
        base_params['id'] = id
    
    else:
        # set edit options for other actions e.g claim
        base_params['action'] = 'wbcreateclaim'
        base_params['entity'] =  id
        base_params['property'] = 'P443'  #example
        base_params['snaktype'] =  'value'
        base_params['value'] = '"' + str(file_name) + '"'

    return base_params


def set_item_label(params, auth_token):
    return make_api_post_request(config['API_URL'], params, auth_token=auth_token)


def set_item_description(params, auth_token):
    return make_api_post_request(config['API_URL'], params, auth_token=auth_token)


def make_wikidata_edit(username, language, id, lang_label,
                       file_name,data, action, auth_object):

    revision_id = None
    edit_options = {
        'wbsetlabel': set_item_label,
        'wbsetdescription': set_item_description
    }


    csrf_token, api_auth_token = generate_csrf_token(config['API_URL'],
                                                 auth_object['consumer_key'],
                                                 auth_object['consumer_secret'],
                                                 auth_object['access_token'],
                                                 auth_object['access_secret'])
    edit_params = build_edit_params(username, language, id, lang_label, file_name,
                               data, action, auth_object, csrf_token)

    try:
        result = edit_options[action](edit_params, api_auth_token)
        revision_id = revision_id # rev_id can be used for another edit
    
        return {
            'id': id,
            'rev_id': revision_id
        }

    except Exception as e:
        return {'message': str(e)}
