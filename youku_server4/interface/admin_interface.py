from db import models
from lib import common
import os
from conf import setttings
# 查看电影
@common.login_auth
def check_movie(recv_dic,conn):
    # 查看要上传的电影是否村咋i
    movie_list = models.Movie.select(file_md5=recv_dic['file_md5'])
    if not movie_list:
        send_dic = {'flag':True,'msg':'可以上传'}
    else:
        send_dic = {'flag':False,'msg':'电影已存在'}
    common.send_msg(send_dic,conn)


# 上传电影
@common.login_auth
def upload_movie(recv_dic,conn):
    # 电影是已经纯在的 直接上他
    file_name = common.get_session() + recv_dic['movie_name']
    file_size = recv_dic['file_size']

    path = os.path.join(setttings.UPLOAD_MOVIE_PATH,file_name)

    movie_obj = models.Movie(name=file_name,
                 path=path,
                 is_free=recv_dic['is_free'],
                 file_md5=recv_dic['file_md5'],
                 is_delete=0,
                 upload_time=common.get_time(),
                 user_id=recv_dic['user_id'])

    # 写文键
    recv_size= 0
    with open(path,'wb')as f:
        while recv_size<file_size:
            data = conn.recv(1024)
            f.write(data)
            recv_size += len(data)
        print('下载成功')


    send_dic = {"flag":True,'msg':'上传成功'}

    movie_obj.save()
    common.send_msg(send_dic,conn)


@common.login_auth
def delete_movie(recv_dic,conn):
    # 获取用户的id
    movie_list = models.Movie.select(id=recv_dic['movie_id'])
    if movie_list:

        movie_obj = movie_list[0]
        movie_obj.is_delete = 1

        movie_obj.update()
        send_dic = {'flag': True, 'msg': '用户删除电影成功'}
    else:
        send_dic = {'flag':False,'msg':'暂时无电影可以删除'}

    common.send_msg(send_dic,conn)


@common.login_auth
def release_notice(recv_dic,conn):
    # 直接发布公告
    # 哪个管理员发的记录user_id

    notice_obj = models.Notice(title=recv_dic['title'],
                               content=recv_dic['content'],
                               user_id=recv_dic['user_id'],
                               create_time=common.get_time()

    )
    notice_obj.save()
    send_dic = {'flag': True, 'msg': '发布公告成功'}
    common.send_msg(send_dic, conn)




