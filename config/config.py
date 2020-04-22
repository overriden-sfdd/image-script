api_data = dict( 
    name='data',
    params={
    'authorization': 'Hide this',
    'detect': 'Hide this',
    },
)

authorization_data = dict(
    name='data', 
    params={
    'login': 'Hide this',
    'password': 'Hide this',
    },
)
 
images = 'images/test_images.zip'

HEADERS = dict(
    name='data',
    params={
    'Content-type': 'application/json', 
    'Accept': 'application/json',
    },
)

EXTENSIONS = ('jpg', 'png', 'gif')

ADDITION_URL = dict(
    name='data',
    params={
    'get_token': '/token', 
    'send_image': '/session?token=',
    'get_response': '&sessionId=',
    },
)

ASK_FOR_PROCESS = 60

log_output = './log/'