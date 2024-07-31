import instagram_API


IG= instagram_API.InstagramApi_Call()

# 데이터 생성


# 업로드
IG.post_media('path')

# 모든 댓글에 대한 답글 달기
# IG.reply_for_comment()