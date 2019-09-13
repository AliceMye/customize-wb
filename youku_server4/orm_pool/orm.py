from orm_pool.sql_conn import Mysql



class Field(object):
    def __init__(self, name, column_type,primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class IntegerField(Field):
    def __init__(self, name, column_type='int', primary_key=False, default=0):
        super().__init__(name, column_type, primary_key, default)


class StringField(Field):
    def __init__(self, name, column_type='varchar(255)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)

class MymetaClass(type):
    def __new__(cls,class_name, class_bases, class_attr):
        if class_name == 'Models':
            return type.__new__(cls, class_name, class_bases, class_attr)

        table_name = class_attr.get('table_name',class_name)

        mapping = {}
        primary_key = None
        for k,v in class_attr.items():
            if isinstance(v,Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        raise TypeError('一张表只有一个主键')
                    primary_key = v.name

        for k in mapping.keys():
            class_attr.pop(k)

        if not primary_key:
            raise TypeError('一张表必须有主键')

        class_attr['table_name'] = table_name
        class_attr['primary_key'] = primary_key
        class_attr['mapping'] = mapping
        return type.__new__(cls,class_name,class_bases, class_attr)

class Models(dict,metaclass=MymetaClass):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, item):
        return self.get(item,'没有该建')

    def __setattr__(self, key, value):
        self[key] = value


    # 查
    @classmethod
    def select(cls,**kwargs):
        ms = Mysql()
        if not kwargs:

            sql = "select * from %s"%cls.table_name
            res = ms.select(sql)

        else:
            # select *from user where id=1
            pk = list(kwargs.keys())[0]
            values = kwargs.get(pk)
            sql = 'select * from %s where %s=?'%(cls.table_name,pk)
            sql = sql.replace('?','%s')
            res = ms.select(sql,values)
        if res:
            return [cls(**kwargs) for kwargs in res]


    # 保存
    def save(self):
        ms = Mysql()
        field = []
        args=[]
        values = []
        # insert into user(name,pwd) values('cc','123)
        for k,v in self.mapping.items():
            if not v.primary_key:
                field.append(v.name)
                # print(v.name,'sq1222')
                args.append("?")
                values.append(getattr(self,v.name,v.default))
        sql = 'insert into %s(%s) values(%s)' %(self.table_name,','.join(field),','.join(args))

        sql = sql.replace('?','%s')
        ms.execute(sql,values)

    # 更新
    def update(self):
        ms = Mysql()
        # 主键和字段
        field = []
        args = []
        values = []
        pk = None
        # update user set name='' passwoed='' where id=1
        for k,v in self.mapping.items():
            if v.primary_key:
                pk = getattr(self,v.name,v.default)

            else:
                field.append(v.name+'=?')
                values.append(getattr(self,v.name,v.default))
                print(v.name,'sql33')

        sql = 'update %s set %s where %s=%s'%(self.table_name, ','.join(field),self.primary_key,pk)
        sql = sql.replace('?','%s')
        ms.execute(sql,values)


if __name__ == '__main__':
    # class User(Models):
    #     id = IntegerField(name='id',primary_key=True)
    #     name = StringField(name='name')
    #     password = StringField(name='password')
    # res = User.select(name='ddd')
    # user_obj = res[0]
    # print(user_obj)
    # print(res)
    # save()
    # user_obj.name='bbb'
    # user_obj.password='999'
    # user_obj.save()
    # 改 update
    # user_obj.name='ddd'
    # user_obj.password = '666'
    # user_obj.update()
    pass













