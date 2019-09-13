import os

from db import models
from lib import common
# 用户购买Vip

@common.login_auth
def buy_vip(recv_dic, conn):
    user_list = models.User.select(id=recv_dic['user_id'])
    if user_list:
        user_obj = user_list[0]
        user_obj.is_vip = 1
        user_obj.update()
        send_dic = {'flag':True,'msg':'购买vip成功'}
    else:
        send_dic = {'flag':False,'msg':'无此用户'}

    common.send_msg(send_dic,conn)


@common.login_auth
def download_movie(recv_dic,conn):
    # 下载电影
    # print('-0--')
    # print(recv_dic)
    movie_list = models.Movie.select(id=recv_dic['movie_id'])
    movie_obj = movie_list[0]
    user_obj = models.User.select(id=recv_dic['user_id'])[0]
    # 文件路径 文件大小 文件名

    # print(movie_obj,'111')
    path = movie_obj.path
    file_size = os.path.getsize(path)
    # print(file_size,'222')
    wait_time = 0
    if recv_dic['movie_type'] == 'free':
        if not user_obj.is_vip:
            wait_time=5

    send_dic = {'flag':True,'msg':'可以下载','file_size':file_size, 'wait_time':wait_time}
    common.send_msg(send_dic,conn,path)
    # 记得发送文件

    # 添加下载记录
    record = models.DownloadRecord(user_id=user_obj.id,movie_id=movie_obj.id,download_time=common.get_time())
    record.save()


@common.login_auth
def check_download_record(recv_dic,conn):
    """
    # 用户id 可以获取用户下载过的所有电影
    # table_name = 'download_record'
    # # 字段
    # id = IntegerField(name='id', primary_key=True)
    # # 那个用户下载的电影 记录用户id
    #
    # user_id = IntegerField(name='user_id')
    # # 下了哪部电影
    # movie_id = IntegerField(name='movie_id')
    # download_time = StringField(name='download_time')
    """
    # 先去获取所有的公告
    record_list = models.DownloadRecord.select()
    back_record_list = []
    user_id = recv_dic['user_id']
    if record_list:
        for record_obj in record_list:
            if record_obj.user_id == user_id:
                # 获取改用户的电影对象
                movie_obj = models.Movie.select(id=record_obj.movie_id)[0]  # 连表查电影的id == 带你应记录的id
                back_record_list.append(movie_obj.name)
        if back_record_list:
            send_dic = {'flag':True,'record_list':back_record_list}
        else:
            send_dic = {'flag':False,'msg': '暂无观影记录'}
    else:
        send_dic = {'flag': False, 'msg': '暂无观影记录'}
    common.send_msg(send_dic,conn)


def check_notice(recv_dic,conn):
    # 分函数封装
    back_notcie_list = notice_by_count()
    if back_notcie_list:
        send_dic = {'flag':True,'notice_list':back_notcie_list}
    else:
        send_dic = {'flag':False,'msg':'暂无公告'}
    common.send_msg(send_dic,conn)

def notice_by_count(count=None):
    # 获取所有的公告
    notice_list= models.Notice.select()  # [{},{}] 列表套对象
    back_notcie_list = []
    if notice_list:
        if not count:
            for notice_obj in notice_list:
                back_notcie_list.append({'title':notice_obj.title,'content':notice_obj.content})

        else:
            # 最新一tiao
            notices_lists = sorted(notice_list,key=lambda notice:notice.create_time,reverse=True)
            # dui想
            # print(notices_list,type(notices_list))
            back_notcie_list.append({'title':notices_lists[0].title,'content':notices_lists[0].content})
        if back_notcie_list:
            return back_notcie_list
        else:
            return False
    else:
        return
