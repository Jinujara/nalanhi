import instagram_API
import create_object

IG= instagram_API.InstagramApi_Call()
text, image= create_object.create()

# 데이터 생성
import pandas as pd

# Create sample data
df = pd.DataFrame(columns=['upload_time', 'media_info', 'caption', 'Q_comment', 'A_reply'])
# info = [('https://www.humanesociety.org/sites/default/files/2019/03/rabbit-475261_0.jpg', 'IMAGE'),('https://res.heraldm.com/content/image/2022/10/12/20221012000744_0.jpg', 'IMAGE')]
# temp_str = '\n'*20

# # carousel (multi-data)
# data_multi = pd.DataFrame({
#     'upload_time': ['2024/07/13'],
#     'media_info': [info],
#     'caption' : ['multi media test'],
#     'Q_comment': ['문제를 맞춰봅시다 ^&^'],
#     'A_reply' : [f'정답을 알아봐요! {temp_str} O~X~']})

# single media
# single_info = [('https://octapi.lxzin.com/interior/vImgFileSeq/202210/11/8ede80a1-1d0c-4839-bcc3-97bd4f357ecd.jpg', 'IMAGE')]
# data_single = pd.DataFrame({
#     'upload_time': ['2024/07/20'],
#     'media_info': [single_info], # (url, media_type)
#     'caption' : ['single media test'],
#     'Q_comment': ['no_comments'],
#     'A_reply' : [None]})

single_info = [(image, 'IMAGE')]
data_single = pd.DataFrame({
    'upload_time': ['2024/07/20'],
    'media_info': [single_info], # (url, media_type)
    'caption' : [text],
    'Q_comment': ['이제 주제만 입력하면 한번에 업로드 됍니당 키키'],
    'A_reply' : ['이 글 누가 제일 먼저 발견하려나']})

# data_df = pd.concat([data_multi, data_single], axis=0, ignore_index=True)
# data_df.to_csv('data.csv', encoding='utf-8', index=False)
data_single.to_csv('data.csv', encoding='utf-8', index=False)

# 업로드
IG.post_media('data.csv')

# 모든 댓글에 대한 답글 달기
# IG.reply_for_comment()