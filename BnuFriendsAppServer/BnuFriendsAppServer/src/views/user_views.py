#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All user operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import os
import json

from PIL import Image
from django.http import HttpResponse
from bson.objectid import ObjectId

from BnuFriendsAppServer import dbtools
from BnuFriendsAppServer import settings

db = dbtools.DB()


def register_action(request):
    email = request.POST['email']
    password = request.POST['password']
    name = request.POST['name']
    
    # username must be email
    # TODO
    res = {}
    if db.check_user_exist_by_email(email):
        res['code'] = 1
        res['msg'] = r'邮箱已被注册'
        return HttpResponse(json.dumps(res), )
    # end if
        
    user_id = db.add_user(email = email, password = password, name = name)
    
    if user_id is not None:
        res['code'] = 0
        res['msg'] = r'注册成功'
        res['userid'] = str(user_id)
        res['email'] = email
        res['name'] = name
    else:
        res['code'] = 1
        res['msg'] = r'注册失败'
        
    return HttpResponse(json.dumps(res), )

def login_action(request):
    email = request.POST['email']
    password = request.POST['password']
    
    user = db.login(email, password)
    
    res = {}
    if user is not None:
        res['code'] = 0
        res['msg'] = r'登陆成功'
        res['userid'] = str(user['_id'])
        res['email'] = user['email']
        res['name'] = user['name']
        res['dept'] = user['dept']
        res['year'] = user['year']
        res['degree'] = user['degree']
        res['province'] = user['province']
        res['city'] = user['city']
        res['qq'] = user['qq']
        res['company'] = user['company']     
        res['phone'] = user['phone']
        res['gender'] = user['gender']
        res['signature'] = user['signature']
        if user['avatar_sub_url'] != '':
            res['avatar_url'] = os.path.join(settings.IMAGES_URL_PREFIX, 
                                             r'user_avatar',
                                             user['avatar_sub_url'])
        else:
            res['avatar_url'] = ''        
    else:
        res['code'] = 1
        res['msg'] = r'登陆失败'
        
    return HttpResponse(json.dumps(res), )


def update_user_profile_action(request):
    user_id = ObjectId(request.POST['userid'])
    cur_user_info = db.get_user_info_by_id(user_id)
    
    # name
    if 'name' in request.POST and request.POST['name'] != '':
        name = request.POST['name']
    else:
        name = cur_user_info['name']

    # dept
    if 'dept' in request.POST and request.POST['dept'] != r'':
        dept = request.POST['dept']    
    else:
        dept = cur_user_info['dept']

    # year
    if 'year' in request.POST and request.POST['year'] is not None:
        year = int(request.POST['year'])    
    else:
        year = cur_user_info['year']
        
    # degree
    if 'degree' in request.POST and request.POST['degree'] != r'':
        degree = request.POST['degree']    
    else:
        degree = cur_user_info['degree']
        
    # province
    if 'province' in request.POST and request.POST['province'] != r'':
        province = request.POST['province']    
    else:
        province = cur_user_info['province']
        
    # city
    if 'city' in request.POST and request.POST['city'] != r'':
        city = request.POST['city']    
    else:
        city = cur_user_info['city']

    # qq
    if 'qq' in request.POST and request.POST['qq'] != r'':
        qq = request.POST['qq']    
    else:
        qq = cur_user_info['qq']
        
    # company
    if 'company' in request.POST and request.POST['company'] != r'':
        company = request.POST['company']    
    else:
        company = cur_user_info['company']
    
    # phone
    if 'phone' in request.POST and request.POST['phone'] != r'':
        phone = request.POST['phone']    
    else:
        phone = cur_user_info['phone']
        
    # gender
    if 'gender' in request.POST and request.POST['gender'] is not None:
        gender = request.POST['gender']    
    else:
        gender = cur_user_info['gender']
        
    # signature
    if 'signature' in request.POST and request.POST['signature'] != r'':
        signature = request.POST['signature']    
    else:
        signature = cur_user_info['signature']
    
    # avatar_sub_url
    if 'avatar_image' in request.FILES:
        reqfile = request.FILES['avatar_image']
        image = Image.open(reqfile)
        image.thumbnail((128,128),Image.ANTIALIAS)
        avatar_sub_url = '%s.jpeg' % str(user_id)
        avatar_path = os.path.join(settings.IMAGES_PATH, 
                                   r'user_avatar',
                                   avatar_sub_url)
        image.save(avatar_path,"jpeg")
    else:
        avatar_sub_url = cur_user_info['avatar_sub_url']
    
    db.update_user_profile(user_id = user_id, 
                           name = name, 
                           dept = dept, 
                           year = year, 
                           degree = degree,
                           province = province, 
                           city = city, 
                           qq = qq, 
                           company = company, 
                           phone = phone, 
                           gender = gender, 
                           signature = signature, 
                           avatar_sub_url = avatar_sub_url )
    res = {}
    res['code'] = 0
    res['msg'] = r'更新用户资料成功'
    res['userid'] = str(user_id)

    return HttpResponse(json.dumps(res), )


def get_user_profile_action(request):
    user_id = ObjectId(request.POST['userid'])
    user_info = db.get_user_info_by_id(user_id)
    res = {}
    
    if user_info is not None:
        res['code'] = 0
        res['msg'] = r'获得用户详情成功'
        res['userid'] = str(user_info['_id'])
        res['email'] = user_info['email']
        res['name'] = user_info['name']
        res['dept'] = user_info['dept']
        res['year'] = user_info['year']
        res['degree'] = user_info['degree']
        res['province'] = user_info['province']
        res['city'] = user_info['city']
        res['qq'] = user_info['qq']
        res['company'] = user_info['company']     
        res['phone'] = user_info['phone']
        res['gender'] = user_info['gender']
        res['signature'] = user_info['signature']
        if user_info['avatar_sub_url'] != '':
            res['avatar_url'] = os.path.join(settings.IMAGES_URL_PREFIX, 
                                             r'user_avatar',
                                             user_info['avatar_sub_url'])
        else:
            res['avatar_url'] = ''        
    else:
        res['code'] = 1
        res['msg'] = r'获得用户详情失败'
        
    return HttpResponse(json.dumps(res), )


def search_friends_action(request):
    user_id = ObjectId(request.POST['userid'])
    if 'name' in request.POST and request.POST['name'] != r'':
        name = request.POST['name']    
    else:
        name = None
    
    if 'year' in request.POST and request.POST['year'] != 0:
        year = int(request.POST['year'])    
    else:
        year = None
    
    if 'dept' in request.POST and request.POST['dept'] != r'':
        dept = request.POST['dept']    
    else:
        dept = None
        
    if 'city' in request.POST and request.POST['city'] != r'':
        city = request.POST['city']    
    else:
        city = None
    
    startk = int(request.POST['start'])
    limitk = int(request.POST['k'])
    
    raw_user_list = \
      db.find_user_by_name_year_dept_city(name, year, dept, city, startk, limitk)
    
    res = {}
    friends = []
    if raw_user_list is not None:
        for raw_user in raw_user_list:
            # 跳过搜索用户
            if raw_user['_id'] is user_id:
                continue
            
            if raw_user['avatar_sub_url'] != '':
                avatar_url = os.path.join(settings.IMAGES_URL_PREFIX, 
                                      r'user_avatar',
                                      raw_user['avatar_sub_url'])
            else:
                avatar_url = r''
            friends.append({'userid': str(raw_user['_id']),
                            'email': raw_user['email'],
                            'name': raw_user['name'],
                            'dept': raw_user['dept'],
                            'year': raw_user['year'],
                            'degree': raw_user['degree'],
                            'province': raw_user['province'],
                            'city': raw_user['city'],
                            'qq': raw_user['qq'],
                            'company': raw_user['company'],     
                            'phone': raw_user['phone'],
                            'gender': raw_user['gender'],
                            'avatar_url': avatar_url,
                            })
        # end for
        res['code'] = 0
        res['msg'] = r'搜索用户成功'
        res['count'] = raw_user_list.count()
        res['friends'] = friends
    else:
        res['code'] = 0
        res['msg'] = r'没有搜索到用户'
        res['count'] = 0
        res['friends'] = friends
    
    return HttpResponse(json.dumps(res), )
    

