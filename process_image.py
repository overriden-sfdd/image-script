import requests
import base64
import glob
import json
import os
import time_tracker as tt


def collect_images(extensions, path='./'):
    '''
    Simple function which collects all images in all dirs and sub-dirs
    extensions `tuple|list of our image file extensions`
    path indicates the dir to start from looking for images
    returns the list of all images and their paths as list
    '''
    return [f for e in extensions for f in glob.glob(path + f"**/*.{e}", recursive=True)]

@tt.timeit  # simple time decorator
def send_image(path_to_img, detect_api, headers, addition_url_string):
    '''
    send_image function takes path_to_img = `our path_to_img` 
    each path is the element of list produced by collect_images function
    detect_api is the url of server where we will send our images
    headers is the default thing for post method with json
    addition_url_string is the `string containing special chars` to make url work
    '''
    with open(path_to_img, 'rb') as img_file:
        image_data = base64.b64encode(img_file.read())  # encoding image into string
    
    data = {'tradePointId': '1', 'images': [image_data.decode()]} # constant value 1 here
    response = requests.post(detect_api + addition_url_string, \
                        json.dumps(data), \
                        headers=headers)
    return json.loads(response.text)
