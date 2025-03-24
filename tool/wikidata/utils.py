import requests
from flask import jsonify

def make_api_request(url, PARAMS):
    """ Makes request to an end point to get data

        Parameters:
            url (str): The Api url end point
            PARAMS (obj): The parameters to be used as arguments

        Returns:
            data (obj): Json object of the recieved data.
    """
    try:
        S = requests.Session()
        r = S.get(url=url, params=PARAMS)
        data = r.json()
        return data
    except Exception as e:
        return jsonify(str(e))


def build_search_result(search_result):
    search_result_data = []
    for data in search_result:
        search_entity = {}
        if "id" in data.keys():
            search_entity["wd_id"] = data["id"]
        else:
            search_entity["wd_id"] = None
        if "label" in data.keys():
            search_entity["label"] = data["label"]
        else:
            search_entity["label"] = None
        if "description" in data.keys():
            search_entity["description"] = data["description"]
        else:
            search_entity["description"] = None

        search_result_data.append(search_entity)

    return search_result_data
