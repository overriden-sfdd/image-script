import requests
import json
import os


def get_token(data, api, headers, addition_url_string='/token'):
    '''
    data is the input `dict with login and password` len(data) = 2
    api is the `url where we get our token`
    headers is the default thing for post method with json
    addition_url_string is the `string containing special chars` to make url work
    '''
    response = requests.post(api + addition_url_string, \
                            json.dumps({'account': data}), \
                            headers=headers)
    return json.loads(response.text) # returning dict with response information in it


def detect_result(full_url, headers):
    '''
    full_url is the `api + addition_url_string`
    headers is the default thing for post method with json
    '''
    return json.loads(requests.get(full_url, headers).text)