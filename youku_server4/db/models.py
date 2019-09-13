# 模型表结构
from orm_pool.orm import Models,IntegerField,StringField


class User(Models):
    table_name = 'user'
    id = IntegerField(name='id',primary_key=True)
    name = StringField(name='name')
    password = StringField(name='password')
    is_vip = IntegerField(name='is_vip')
    is_locked = IntegerField(name='is_locked')
    user_type = StringField(name='user_type')
    register_time = StringField(name='register_time')


class Movie(Models):
    table_name = 'movie'
    id = IntegerField(name='id',primary_key=True)
    name = StringField(name='name')
    path = StringField(name='path')
    is_free = IntegerField(name='is_free')
    file_md5 = StringField(name='file_md5')
    user_id = IntegerField(name='user_id')
    is_delete = IntegerField(name='is_delete')
    upload_time = StringField(name='upload_time')


# 公告
class Notice(Models):
    table_name = 'notice'
    id = IntegerField(name='id', primary_key=True)
    title = StringField(name='title')
    content = StringField(name='content')
    user_id = IntegerField(name='user_id')
    create_time = StringField(name='create_time')


class DownloadRecord(Models):
    table_name = 'download_record'
    id = IntegerField(name='id', primary_key=True)
    # 哪个用户下载的 记录他的user_id
    user_id = IntegerField(name='user_id')
    # 下载电影的movie_id
    movie_id = IntegerField(name='movie_id')
    download_time = StringField(name='download_time')
