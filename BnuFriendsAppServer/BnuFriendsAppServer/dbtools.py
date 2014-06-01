#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All mongodb operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import pymongo
import time


class DB:
    _server_address = "112.126.65.223"
    _port = 27017
    _db_name = "bnu_friends"

    def __init__(self, address=_server_address, port=_port):
        self.connection = pymongo.Connection(address, port)
        # self.setup_index()

    #==========================================================================
    # base operations
    #==========================================================================
    def get_db(self, name=_db_name):
        return self.connection[name]

    def get_collection(self, name):
        return self.get_db()[name]
    
    def setup_index(self):
        """
        ensure index according to data model
        should be called only once before any of the methods is invoked
        """
        pass
    
    #==========================================================================
    # user operations
    #
    #    _id
    #    email           || int       ||
    #    password        || string    ||
    #    name            || string    || 真实姓名
    #    is_admin        || int       || 默认0；0-普通用户；1-管理员
    #    dept            || string    || 学院
    #    year            || int       || 毕业年份
    #    degree          || string    || 学历
    #    province        || string    || 毕业后所在省
    #    city            || string    || 毕业后所在城市
    #    qq              || string    || qq or 微信
    #    company         || string    || 毕业后所在公司
    #    avatar_sub_url  || string    || 头像文件相对路径
    #    phone           || string    ||
    #    gender          || int       || 默认0；0-male；1-female
    #    signature       || string    || 个性签名
    #    reg_timestamp   || long      || 注册时间
    #
    #==========================================================================
    
    # TODO
    # store password encoded
    def add_user(self, email, password, name, is_admin = 0,
                 dept = r'', year = 2014, degree = r'', province = r'',
                 city = r'', qq = r'', company = r'', avatar_sub_url = r'',
                 phone = r'', gender = 0, signature = r''):
        user = {'email':email,
                'password':password,
                'name': name,
                'is_admin': is_admin,
                'dept': dept,
                'year': year,
                'degree': degree,
                'province': province,
                'city': city,
                'qq': qq,
                'company': company,
                'avatar_sub_url': avatar_sub_url, 
                'phone': phone,
                'gender': gender,
                'signature': signature,
                'reg_timestamp':  long(time.time()), }
        return self.get_collection('user').insert(user, safe=True)

    def check_user_exist_by_email(self, email):
        return self.get_collection('user')\
                 .find_one({'email': email}) is not None

    def login(self, email, password):
        return self.get_collection('user').find_one({'email': email, 
                                                     'password': password})
    
    def login_admin(self, email, password):
        pass
    
    def get_user_info_by_id(self, user_id):
        return self.get_collection('user').find_one({'_id': user_id})
    
    def update_user_profile(self, user_id, name, dept, year, degree,
                            province, city, qq, company, phone, 
                            gender, signature, avatar_sub_url, ):
        return self.get_collection('user')\
            .update({'_id': user_id},
                    {'$set': {'name': name,
                              'dept': dept,
                              'year': year,
                              'degree': degree,
                              'province': province,
                              'city': city,
                              'qq': qq,
                              'company': company,
                              'avatar_sub_url': avatar_sub_url, 
                              'phone': phone,
                              'gender': gender,
                              'signature': signature, }})
    
    def find_user_by_name_year_dept_city(self, name, year, dept, city, startk, limitk):
        # 1111
        if name is not None and year is not None and dept is not None and city is not None:
            return self.get_collection('user').find({'name': name, 'year': year, 'dept': dept, 'city': city, })\
                .skip(startk).limit(limitk)
        # 1110
        if name is not None and year is not None and dept is not None and city is None:
            return self.get_collection('user').find({'name': name, 'year': year, 'dept': dept, })\
                .skip(startk).limit(limitk)
        # 1101
        if name is not None and year is not None and dept is None and city is not None:
            return self.get_collection('user').find({'name': name, 'year': year, 'city': city,})\
                .skip(startk).limit(limitk)
        # 1100
        if name is not None and year is not None and dept is None and city is None:
            return self.get_collection('user').find({'name': name, 'year': year, })\
                .skip(startk).limit(limitk)
        # 1011
        if name is not None and year is None and dept is not None and city is not None:
            return self.get_collection('user').find({'name': name, 'dept': dept, 'city': city, })\
                .skip(startk).limit(limitk)        
        # 1010
        if name is not None and year is None and dept is not None and city is None:
            return self.get_collection('user').find({'name': name, 'dept': dept })\
                .skip(startk).limit(limitk)
        # 1001
        if name is not None and year is None and dept is None and city is not None:
            return self.get_collection('user').find({'name': name, 'dept': dept, })\
                .skip(startk).limit(limitk)
        # 1000
        if name is not None and year is None and dept is None and city is None:
            return self.get_collection('user').find({'name': name, })\
                .skip(startk).limit(limitk)
        # 0111
        if name is None and year is not None and dept is not None and city is not None:
            return self.get_collection('user').find({'year': year, 'dept': dept, 'city': city, })\
                .skip(startk).limit(limitk)
        # 0110
        if name is None and year is not None and dept is not None and city is None:
            return self.get_collection('user').find({'year': year, 'dept': dept, })\
                .skip(startk).limit(limitk)
        # 0101
        if name is None and year is not None and dept is None and city is not None:
            return self.get_collection('user').find({'year': year, 'city': city, })\
                .skip(startk).limit(limitk)
        # 0100
        if name is None and year is not None and dept is None and city is None:
            return self.get_collection('user').find({'year': year, })\
                .skip(startk).limit(limitk)
        # 0011
        if name is None and year is None and dept is not None and city is not None:
            return self.get_collection('user').find({'dept': dept, 'city': city, })\
                .skip(startk).limit(limitk)
        # 0010
        if name is None and year is None and dept is not None and city is None:
            return self.get_collection('user').find({'dept': dept, })\
                .skip(startk).limit(limitk)
        # 0001
        if name is None and year is None and dept is None and city is not None:
            return self.get_collection('user').find({'city': city, })\
                .skip(startk).limit(limitk)
    
    #==========================================================================
    # news operations
    #
    #    _id
    #    news_type                || int       || 0-article；1-video
    #    title                    || string    ||
    #    abstract                 || string    || 摘要 less than 20 words
    #    body                     || string    || 
    #    author                   || string    || 用于显示的作者
    #    module                   || int       || 版块id >0
    #    created_timestamp        || long      || 
    #    last_modify_timestamp    || long      ||
    #    pub_timestamp            || long      ||
    #    pub_status               || int       || 默认0；0-未发布； 1-发布
    #    inner_pic_sub_url        || string    || 文章配图的链接地址
    #    is_delete                || int       || 默认0；0-不删除； 1-删除
    #    video_target_url         || string    ||
    #
    #==========================================================================
    def add_news(self, news_type, title, abstract, body, author,
                 module, pub_status = 0, is_delete = 0,
                 inner_pic_sub_url = r'',
                 video_target_url = r''):   
        timestamp = long(time.time())
        raw_news = {'news_type': news_type,
                    'title': title,
                    'abstract': abstract,
                    'body': body,
                    'author': author,
                    'module': module,
                    'created_timestamp': timestamp,
                    'last_modify_timestamp': timestamp, 
                    'pub_timestamp': timestamp,
                    'pub_status': pub_status,
                    'is_delete': is_delete,
                    'inner_pic_sub_url': inner_pic_sub_url,
                    'video_target_url': video_target_url, }
        return self.get_collection('news').insert(raw_news)
    
    def update_pub_timestamp(self,):
        pass
    
    def update_pub_status(self, ):
        pass
    
    def update_is_delete_status(self,):
        pass
    
    def get_k_news_by_timestamp_pub_status_module(self, cur_timestamp,
                                                        module, 
                                                        pub_status = 1,
                                                        k = 5):
        return self.get_collection('news')\
                 .find({'pub_status': 1,
                        'module': module,
                        'pub_timestamp': {'$lte': cur_timestamp}})\
                 .sort('pub_timestamp', pymongo.DESCENDING)\
                 .limit(k)
    
    def get_k_news_by_timestamp_pub_status(self, cur_timestamp,
                                           pub_status = 1,
                                           k = 1):
        return self.get_collection('news')\
                 .find({'pub_status': 1,
                        'pub_timestamp': {'$lte': cur_timestamp}})\
                 .sort('pub_timestamp', pymongo.DESCENDING)\
                 .limit(k)
                 
    def get_news_count_by_timestamp_module(self, timestamp, module):
        return self.get_collection('news')\
                 .find({'pub_status': 1,
                        'module': module,
                        'pub_timestamp': {'$gte': timestamp}})\
                 .sort('pub_timestamp', pymongo.DESCENDING)\
                 .count()
                 
    def get_news_detail_by_id(self, news_id):
        return self.get_collection('news').find_one({'_id': news_id})

    #==========================================================================
    # comment operations
    #
    #    _id                
    #    user_id            || ObjectId      || 发布者id
    #    news_id            || ObjectId      || 关联的新闻id
    #    pub_timestamp      || long          || 发布时间
    #    msg                || string        ||
    #
    #==========================================================================
    def add_comment(self, news_id, user_id, msg):
        comment = {'user_id': user_id,
                   'news_id': news_id,
                   'pub_timestamp': long(time.time()),
                   'msg': msg, }
        return self.get_collection('comments').insert(comment)
    
    def get_k_comments_by_timestamp_news_id(self, begin_timestamp, news_id, k):
        return self.get_collection('comments')\
            .find({'news_id': news_id,
                   'pub_timestamp': {'$lte': begin_timestamp}})\
            .sort('pub_timestamp', pymongo.DESCENDING).limit(k)
    
    def get_comment_count_by_news_id(self, news_id):
        return self.get_collection('comments')\
                 .find({'news_id': news_id})\
                 .count()

    #==========================================================================
    # email operations
    #
    #    _id                
    #    sender_id          || ObjectId      || 发信者id
    #    receiver_id        || ObjectId      || 收信者id
    #    send_timestamp     || long          || 发信时间
    #    msg                || string        ||
    #
    #==========================================================================
    def add_email(self, sender_id, receiver_id, msg):
        email = {'sender_id': sender_id,
                 'receiver_id': receiver_id,
                 'send_timestamp': long(time.time()),
                 'msg': msg, }
        return self.get_collection('email').insert(email)
    
    def get_k_email_by_timestamp_user_id(self, begin_timestamp, user_id, k):
        return self.get_collection('email')\
            .find({'$or': [{'sender_id': user_id, },
                           {'receiver_id': user_id}, ],
                   'send_timestamp': {'$lte': begin_timestamp}}).limit(k)
            # .sort([('send_timestamp', pymongo.DESCENDING)]).limit(k)
    
    def get_email_count_by_timestamp_user_id(self, timestamp, user_id):
        return self.get_collection('email')\
            .find({'receiver_id': user_id,
                   'send_timestamp': {'$gte': timestamp}})\
            .count()
           
        
        
        
        
        
        
        
        
    