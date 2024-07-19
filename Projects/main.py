import instagram_API as IG
import test

params = IG.get_creds()

params['media_type'] = 'IMAGE'
params['media_url'] = 'https://octapi.lxzin.com/interior/vImgFileSeq/202210/11/8ede80a1-1d0c-4839-bcc3-97bd4f357ecd.jpg'

multi_image_media_object_1 = IG.create_multi_media(params)
multi_image_media_object_2 = IG.create_multi_media(params)
media_object_list = [multi_image_media_object_1, multi_image_media_object_2]

media_id_list = [container['id'] for container in media_object_list]
params['caption'] = '자동화 테스트'
params['media_type'] = 'CAROUSEL'
params['children'] = media_id_list
carousel_container = IG.create_slide_object(params)

# publish
publish_response = IG.publish_media(carousel_container['id'], params)