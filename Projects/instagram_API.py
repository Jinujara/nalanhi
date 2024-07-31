import requests
import openai
import json
import os
import ast
import pandas as pd
from pprint import pprint as pp
from dotenv import load_dotenv

class InstagramApi_Call:
    
    def __init__(self):
        # load .env
        load_dotenv()
        self.IG_ACCESS_TOKEN=os.environ.get("IG_ACCESS_TOKEN")
        self.IG_BUSINESS_ID=os.environ.get('IG_BUSINESS_ID')
        self.IG_USER_NAME=os.environ.get('IG_USER_NAME')
        self.creds = dict() 
        
        
        # get_creds
        """
        {'access_token': '',
        'graph_domain': 'https://graph.facebook.com/',
        'graph_version': 'v20.0',
        'instagram_account_id': '',
        'ig_username': '',
        'endpoint_base': 'https://graph.facebook.com/v20.0/'}

        """
        
        self.creds['access_token'] = self.IG_ACCESS_TOKEN   # access token for use with all api calls
        self.creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
        self.creds['graph_version'] = 'v20.0' # version of api we are hitting
        self.creds['instagram_account_id'] = self.IG_BUSINESS_ID # user business account id
        self.creds['ig_username'] = self.IG_USER_NAME
        # with domain and version
        self.creds['endpoint_base'] = self.creds['graph_domain'] + self.creds['graph_version'] + '/' # base endpoint
        
        self.params= self.creds
        


    def create_media(self, include_caption=True, include_children=False):
        """Create media container object

        API Endpoint:
        - For image
            https://graph.facebook.com/v20.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access_token}
        - For video
            https://graph.facebook.com/v20.0/{ig-user-id}/media?media_type=VIDEO&video_url={video-url}&caption={caption}&access_token={access_token}
        - For Carousel
            https://graph.facebook.com/v20.0/{ig-user-id}/media?media_type=CAROUSEL&children={children}&caption={caption}&access_token={access_token}

        Returns:
            json object: {id : media_container_object_id}
        """
        
        
        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/media'
        
        endpointParams = {
            'access_token': self.params['access_token']
        }

        ##### Media Type : IMAGE, VIDEO, CAROUSEL #####
        if self.params['media_type'] == 'IMAGE':
            endpointParams['image_url'] = self.params['media_url']
        
        elif self.params['media_type'] == 'VIDEO':
            endpointParams['video_url'] = self.params['media_url']
            endpointParams['media_type'] = self.params['media_type']
        
        # media_type == 'CAROUSEL'
        else:
            endpointParams['media_type'] = self.params['media_type']

        
        
        ##### Number of Media to Post : Single, Multi(=Carousel) #####
        
        # for single media post
        if include_caption:
            endpointParams['caption'] = self.params['caption']
            
        # for carousel.
        if include_children:
            endpointParams['children'] = self.params['children']
            response = requests.post(url, json=endpointParams)
            return response.json()

        response = requests.post(url, data=endpointParams)
        return response.json()

    def create_single_media(self):
        """Create `single media` container object"""
        return self.create_media(include_caption=True)

    def create_multi_media(self):
        """Create `multi media` container object"""
        return self.create_media(include_caption=False)

    def create_slide_media(self):
        """Create `slide media` container object"""
        return self.create_media(include_caption=True, include_children=True)

    def publish_media(self, media_object_id):
        """ Publish `media container` object
        
        API Endpoint:
            https://graph.facebook.com/
            v20.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access_token}

        Returns:
            json object: {id: media_id}
        """

        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/media_publish'

        endpointParams = dict()
        endpointParams['creation_id'] = media_object_id
        endpointParams['access_token'] = self.params['access_token']

        response = requests.post(url, data=endpointParams)
        
        print("\n---- MEDIA OBJECT PUBLISHED ---- \n")
        print("\tID:") # label
        print("\t" + response.json()['id']) # id of the object

        return response.json()

    def post_comment(self, media_id):
        """Post comment to media
        
        API Endpoint:
            https://graph.facebook.com/
            v20.0/{ig_media_id}/comments?message={message}&access_token={access_token}


        """
        url= self.params['endpoint_base'] + media_id + '/comments'
        endpointParams= dict()
        endpointParams['message']= self.params['message']
        endpointParams['access_token']= self.params['access_token']
        
        response= requests.post(url, data= endpointParams)
        
        return response.json()
    
    
    def post_reply_to_comment(self, comment_id):
        """ Post reply to a comment

        API Endpoint:
            https://graph.facebook.com/
            v20.0/{ig_comment_id}/replies?message={message}&access_token={access-token}

        Returns:
            Status Code <Response>
            - 200 : OK
            - 400 : Not supported input form
        """
        
        url = self.params['endpoint_base'] + comment_id + '/replies'
        
        endpointParams = dict()
        endpointParams['message'] = self.params['reply_message']
        endpointParams['access_token'] = self.params['access_token']
        response = requests.post(url, data=endpointParams)
        return response
    

    def get_media_id(self):
        """ Get User Media id
        
        API Endpoint:
            https://graph.facebook.com/
            v20.0/{ig-user-id}?fields=media&access_token={access_token}

        Returns:
            json object:
        
            {'media': {'data': [{'id': 'media_id_1'},
                                {'id': 'media_id_2'},
                                {'id': 'media_id_3'}],
                        'paging': {'cursors': {'before': '----',
                                                'after': '----'}
                                    }
                        },
            'id': 'ig_business_id'}
        """
        
        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '?fields=media'
        
        endpointParams = {
            'access_token': self.params['access_token']
        }
        response = requests.get(url, endpointParams)
        return response.json()

    def get_media_comments(self, media_id):
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
                        'id': {comment_id_2}}
                    ]
            }
        """

        url = self.params['endpoint_base'] + media_id + '/comments?'
        endpointParams = dict()
        endpointParams['access_token'] = self.params['access_token']

        response = requests.get(url, endpointParams)
        return response.json()

    def get_comment_replies(self, comment_id):
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

        url = self.params['endpoint_base'] + comment_id + '/replies'
        endpointParams = dict()
        endpointParams['access_token'] = self.params['access_token']
        endpointParams['fields'] = 'id, text, username'
        response = requests.get(url, endpointParams)
        return response.json()

    def create_reply_texts(self, comment):
        """
            comment를 입력으로 받아 이에 대한 답변을 LLM 모델로 생성
            여기서 무관한 comment시, 
            1) '모른다'라는 답변을 생성할 것인지,
            2) 아니면 reply하지 않을 것인지,
            3) 혹은 그냥 이모지 :) 생성할 것인지 (reply 확인용)
        """

        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": comment}
            ]
        )
        
        return completion.choices[0].message.content
    
    
    #### 메인 호출 함수 1 ####
    def reply_for_comment(self):
        """
        1. get all comments & all reply
        2. if I didn't reply, post reply

        """
        ##### get_media_id #####
        media_id_list= self.get_media_id()['media']['data']    
        
        ##### get_media_comments #####
        for media in media_id_list:
            comment_list_per_media= self.get_media_comments(media['id'])['data']
            
            ##### get_comment_replies #####
            for comment in comment_list_per_media:
                reply_list_per_comment= self.get_comment_replies(comment['id'])['data']
                
                ##### is_replied #####            
                ## reply exist
                if reply_list_per_comment:   
                    i_replied= [bool(reply['username']==self.params['ig_username']) for reply in reply_list_per_comment]
                    
                    # All False (내가 한 reply가 없음)
                    if not any(i_replied):   
                        self.params['reply_message']= self.create_reply_texts(comment['text'])
                        print(self.post_reply_to_comment(comment['id']).json())
                        
                
                ## reply no exist
                else:
                    self.params['reply_message']= self.create_reply_texts(comment['text'])
                    print(self.post_reply_to_comment(comment['id']).json())
    
                    
    #### 메인 호출 함수 2 ####
    def post_media(self, data_path):
        """ Run post process

        Sequence
            1. read_csv ('data.csv')
            2. post to instagram - with using 1st record
            3. return csv
                - len(data) >= 1 (pop first record and return remains)
                - len(data) == 0 (return blank data)
        
        Data Structure
        {
            'caption':  posting caption,
            'media_info': list of tuples (media url, media type)
            'Q_comment': question comment
            'A_reply' : answer reply
        }
        """

        # 데이터 로드 (media_info 열의 데이터는 문자열에서 리스트로 형변환)
        data= pd.read_csv(data_path, encoding='utf-8', converters={'media_info' : ast.literal_eval}) 

        # data의 데이터가 있으면 진행
        if len(data):
            
            ##### Import Data & Upload #####
            posting_data = data.iloc[0]

            self.params['caption'] = posting_data['caption']

            # single_media upload
            if (len(posting_data['media_info']) == 1):
                self.params['media_url'], self.params['media_type'] = posting_data['media_info'][0]
                media_container = self.create_single_media()

            # multi_media upload
            else:
                media_id_list = []

                # media container 생성 - 최대 10개까지만 업로드 가능
                for (media_url, media_type) in posting_data['media_info'][:10]:
                    self.params['media_type'] = media_type
                    self.params['media_url'] = media_url
                    temp_media_container = self.create_multi_media()
                    media_id_list.append(temp_media_container['id'])
                    
                # carousel로 넘기기
                self.params['media_type'] = 'CAROUSEL'
                self.params['children'] = media_id_list
                media_container = self.create_slide_media()
            
            # published 된 경우 object published 출력
            post_id = self.publish_media(media_container['id'])['id'] 
            
            
            
            ##### post comment (Question) #####
            # 글 생성과 동시에 Question 생성하는 경우
            if posting_data['Q_comment']:
                self.params['message'] = posting_data['Q_comment']
                comment_id = self.post_comment(post_id)['id']

                # post reply to comment (Answer)
                # 글 생성과 동시에 Q&A 까지 함께 진행하는 경우
                if posting_data['A_reply']:
                    self.params['reply_message'] = posting_data['A_reply']
                    reply_id = self.post_reply_to_comment(comment_id)

            
            ##### Save Remaining Data #####
            # 작업했던 데이터(첫번째 행) 제거 후, 나머지 data를 csv로 저장
            data = data.drop(index=0).reset_index(drop=True)  # 0번 인덱스 드랍
            data.to_csv(data_path, encoding='utf-8', index=False) # 값 저장.
            print(f'\tRemain records: {len(data)}')
            return 
        
        # data에 데이터가 없으면 바로 종료
        else:
            print("\n---- Sorry, Check the file plz ToT ---- \n")
            print(f'\tNothing to post in csv file')
            return