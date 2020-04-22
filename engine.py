from utils.config import Config
from utils.logger import logger, log

import process_image as prcimg
import authorize as auth
import time as t

CONFIG = './config/config.py' # path to our config file where all global vars are stored

def main():

    cfg = Config.fromfile(CONFIG)

    logger.setup(cfg.log_output, name='information_log')
    log(f'Initial data storage: {CONFIG}')

    auth_data = cfg.authorization_data.params
    api = cfg.api_data.params
    add_url = cfg.ADDITION_URL.params
    headers = cfg.HEADERS.params

    token_response = auth.get_token(auth_data, \
                                    api['authorization'], 
                                    headers, \
                                    add_url['get_token'])

    if token_response['status'] == 'ok': 
        log('Successfully got token')
    else:
        msg = f'Bad response: response status is {token_response.text["status"]}'
        log(msg)
        raise Exception(msg)
    
    token = token_response['account']['token']['value']

    session_ids, get_responses, total_time = [], [], []

    image_files = prcimg.collect_images(cfg.EXTENSIONS)
    for idx, image_name in enumerate(image_files):
        detect_response = prcimg.send_image(image_name, \
                                            api['detect'], \
                                            headers, \
                                            add_url['send_image'] + token)

        if detect_response['status'] == 'ok':
            log('Image has been successfully sent')
            session_ids.append(detect_response['sessionId'])
        else: 
            msg = f'Bad response: response status is {token_response.text["status"]}'
            log(msg)
            raise Exception(msg)

    for idx in range(len(image_files)): 
        while True:     
            t.sleep(cfg.ASK_FOR_PROCESS) # waits according to our global variable
            get_response = auth.detect_result(api['detect'] + \
                                add_url['send_image'] + token     + \
                                add_url['get_response'] + session_ids[idx], \
                                headers)
            
            if get_response['session']['processed'] == 1:  # if image has been processed
                get_responses.append(get_response)         # --> go to the next image session
                total_time.append(get_response['session']['detectionTime'])    
                break
    
    log('All images have been successfully processed')
    log(f'Total number of images is {len(image_files)}')
    log(f'Total time of detection is {sum(total_time)}')
    log(f'Mean time of detection on each image is {sum(total_time)/len(image_files)}')


if __name__ == '__main__':
        
    try:
        main()
    except KeyboardInterrupt:
        print('Keyboard Interrupted')