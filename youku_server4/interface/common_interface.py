from db import models
from lib import common
from db import user_date
from threading import Lock
mutex=Lock()
# 注册功能
from interface import user_interface

def register(recv_dic,conn):
    user_list = models.User.select(name=recv_dic['name'])

    if not user_list:
        # 注册
        user_obj = models.User(name=recv_dic['name'],
                    password=recv_dic['password'],
                    is_vip=0,
                    is_locked=0,
                    user_type=recv_dic['user_type'],
                    register_time=common.get_time())
        user_obj.save()
        send_dic = {'flag':True,'msg':'注册成功'}
    else:
        send_dic = {'flag':False,'msg':'用户名已存在'}
    common.send_msg(send_dic,conn)


def login(recvc_dic,conn):
    user_list = models.User.select(name=recvc_dic['name'])
    if user_list:
        user_obj = user_list[0]
        if user_obj.user_type == recvc_dic['user_type']:
            if user_obj.password == recvc_dic['password']:
                send_dic = {'flag':True,'msg':'登陆成功'}
                # session
                session = common.get_session()
                send_dic['session'] = session
                mutex.acquire()
                user_date.alive_dic[recvc_dic['addr']] = [session,user_obj.id]  # 保护数据
                mutex.release()
                # 后期加公告
                new_notice = user_interface.notice_by_count(1)[0]
                send_dic['new_notice'] = new_notice
                send_dic['is_vip'] = user_obj.is_vip
            else:
                send_dic = {'flag':False,'msg':'两次密码不一致'}
        else:
            send_dic= {'flag':False,'msg':'用户类型不一致'}
    else:
        send_dic = {'flag':False,'msg':'用户不存在'}
    common.send_msg(send_dic,conn)


def get_movie_list(recv_dic,conn):
    # 获取所有的点电影
    movie_list = models.Movie.select()
    back_movie_list = []
    if movie_list:
        for movie in movie_list:
            if not movie.is_delete:
                # 电影名 是否免费  id
                if recv_dic['movie_type'] == 'all':
                    back_movie_list.append([movie.name,'免费' if movie.is_free else '收费', movie.id])
                elif recv_dic['movie_type'] == 'free':
                    if movie.is_free:
                        back_movie_list.append([movie.name,'免费', movie.id])
                else:
                    if not movie.is_free:
                        back_movie_list.append([movie.name,'收费',movie.id])
        if back_movie_list:
            send_dic = {'flag':True,'movie_list':back_movie_list}
        else:
            send_dic = {'flag':False,'msg':'暂无电影'}
    else:
        send_dic = {'flag':False,'msg':'数据库暂无电影'}
    common.send_msg(send_dic,conn)


