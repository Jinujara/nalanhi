import requests
import json
import os
from pprint import pprint as pp
from dotenv import load_dotenv

# load .env
load_dotenv()
IG_ACCESS_TOKEN=os.environ.get("IG_ACCESS_TOKEN")
# FB_APP_SECRET_CODE=os.environ.get('FB_APP_SECRET_CODE')
IG_BUSINESS_ID=os.environ.get('IG_BUSINESS_ID')
IG_USER_NAME=os.environ.get('IG_USER_NAME')

def get_creds():
    """
    {'access_token': '',
    'graph_domain': 'https://graph.facebook.com/',
    'graph_version': 'v20.0',
    'instagram_account_id': '',
    'ig_username': '',
    'endpoint_base': 'https://graph.facebook.com/v20.0/'}

    """
    creds = dict() 
    creds['access_token'] = IG_ACCESS_TOKEN   # access token for use with all api calls
    # creds['client_secret'] = FB_APP_SECRET_CODE  # client secret from facebook app
    creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
    creds['graph_version'] = 'v20.0' # version of api we are hitting
    creds['instagram_account_id'] = IG_BUSINESS_ID # user business account id
    creds['ig_username'] = IG_USER_NAME
    # with domain and version
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint
    
    return creds

def create_single_media(params):
    """Create media `Container` object
    
    API Endpoint:
    - For image
        https://graph.facebook.com/
        v20.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access_token}
    
    - For video
        https://graph.facebook.com/
        v20.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access_token}

    Returns:
        json object: {id : media_container_object_id}
    """

    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'

    endpointParams = dict()
    if params['media_type'] == 'IMAGE':
        endpointParams['image_url'] = params['media_url']
    elif params['media_type'] == 'VIDEO':
        endpointParams['video_url'] = params['media_url']
        endpointParams['media_type'] = params['media_type']
    
    endpointParams['caption'] = params['caption']
    endpointParams['access_token'] = params['access_token']
    
    response = requests.post(url, data=endpointParams)

    return response.json()



def create_multi_media(params):
    """Create media `Container` object
    
    API Endpoint:
    - For image
        https://graph.facebook.com/
        v20.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access_token}
    
    - For video
        https://graph.facebook.com/
        v20.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access_token}

    Returns:
        json object: {id : media_container_object_id}
    """

    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'

    endpointParams = dict()
    if params['media_type'] == 'IMAGE':
        endpointParams['image_url'] = params['media_url']
    elif params['media_type'] == 'VIDEO':
        endpointParams['video_url'] = params['media_url']
        endpointParams['media_type'] = params['media_type']
    
    # endpointParams['caption'] = params['caption']
    endpointParams['access_token'] = params['access_token']
    
    response = requests.post(url, data=endpointParams)

    return response.json()


def publish_media(media_object_id, params):
    """ Publish `media container` object
    
    API Endpoint:
        https://graph.facebook.com/
        v20.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access_token}

    Returns:
        json object: {id: media_id}
    """

    url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish'

    endpointParams = dict()
    endpointParams['creation_id'] = media_object_id
    endpointParams['access_token'] = params['access_token']

    response = requests.post(url, data=endpointParams)
    
    print("\n---- IMAGE MEDIA OBJECT PUBLISHED ---- \n")
    print("\tID:") # label
    print("\t" + response.json()['id']) # id of the object

    return response.json()

def create_slide_object(params):
    """Create media `Container` object
    
    API Endpoint:
    - For image
        https://graph.facebook.com/
        v20.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access_token}
    
    - For video
        https://graph.facebook.com/
        v20.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access_token}

    Returns:
        json object: {id : media_container_object_id}
    """

    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'

    endpointParams = dict()
    endpointParams['media_type'] = params['media_type']
    endpointParams['caption'] = params['caption']
    endpointParams['children'] = params['children']
    endpointParams['access_token'] = params['access_token']
    
    response = requests.post(url, json=endpointParams)

    return response.json()

def get_user_media(params):
    """ Get User Media id
    
    API Endpoint:
        https://graph.facebook.com/
        v20.0/{ig-user-id}?fields=media&access_token={access_token}

    Returns:
        json object:
    
        {'data' : [{id : {media_id_1},
                    id : {media_id_2},
                    id : {media_id_3},]}
    """
    
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'
    
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    endpointParams['fields'] = 'media'
    response = requests.get(url, endpointParams)
    return response.json()

def get_media_comments(media_id, params):
    """  Get media comments

    API Endpoint:
        https://graph.facebook.com/
        v20.0/{media_id}/comments?access_token={access_token}
    
    Returns:
        json object:

        {'data' : [{'timestamp': {created_time},
                    'text': {comment_text_1},
                    'id' : {comment_id_1}},

                    {'timestamp': {created_time},
                    'text': {comment_text_2},
                    'id': {comment_id_2}}]}
    """
    url = params['endpoint_base'] + media_id + '/comments?'
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']

    response = requests.get(url, endpointParams)
    return response.json()

def get_comment_replies(comment_id, params):
    """Create reply for comment
    
    API Endpoint:
        https://graph.facebook.com/
        v20.0/{ig_comment_id}/replies?fields={fields}&access_token={access-token}
    
    Returns:
        json object: the replies are `stacked-shaped`(LIFO)
        
        {'data': [{'id': {replied_id_2},
                'text': {replied_text_2}
                'username': {ig_username},

                {'id', {replied_id_1},
                'text': {replied_text_1},
                'username': {ig_username}
                ]}
    """

    url = params['endpoint_base'] + comment_id + '/replies'
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    endpointParams['fields'] = 'id, text, username'
    response = requests.get(url, endpointParams)
    return response.json()

def post_reply_to_comment(comment_id, params):
    """ Post reply to a comment

    API Endpoint:
        https://graph.facebook.com/
        v20.0/{ig_comment_id}/replies&access_token={access-token}

    Returns:
        Status Code <Response>
        - 200 : OK
        - 400 : Not supported input form
    """
    
    url = params['endpoint_base'] + comment_id + '/replies'

    endpointParams = dict()
    endpointParams['message'] = params['reply_message']
    endpointParams['access_token'] = params['access_token']
    response = requests.post(url, data=endpointParams)
    return response

def post_comment(media_id, params):
    """Post comment to media
    
    API Endpoint:
        https://graph.facebook.com/
        v20.0/{ig_comment_id}/comments?message={message}&access_token={access_token}


    """
    url= params['endpoint_base'] + media_id + '/comments'
    endpointParams= dict()
    endpointParams['message']= params['message']
    endpointParams['access_token']= params['access_token']
    
    response= requests.post(url, data= endpointParams)
    
    return response.json()