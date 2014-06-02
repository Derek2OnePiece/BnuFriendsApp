#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All news operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'


import json
import time

from django.http import HttpResponse
from bson.objectid import ObjectId

from BnuFriendsAppServer import dbtools


db = dbtools.DB()


def send_email_action(request):
    sender_id = ObjectId(request.POST['sender_id'])
    receiver_id = ObjectId(request.POST['receiver_id'])
    mail_msg = request.POST['msg']
    
    res = {}
    if db.add_email(sender_id, receiver_id, mail_msg) is not None:
        res['code'] = 0
        res['msg'] = r'邮件发送成功'
    else:
        res['code'] = 1
        res['msg'] = r'邮件发送失败'    
    return HttpResponse(json.dumps(res), )


def get_email_action(request):
    user_id = ObjectId(request.POST['userid'])
    req_timestamp = long(request.POST['timestamp'])
    k = int(request.POST['k'])
    
    if req_timestamp == -1:
        begin_timestamp = time.time()
    else:
        begin_timestamp = req_timestamp
    
    raw_mail_list = db.get_k_email_by_timestamp_user_id(begin_timestamp, 
                                                        user_id, k)

    
    mail_list = []
    for raw_mail in raw_mail_list:
        sender_info = db.get_user_info_by_id(raw_mail['sender_id'])
        receiver_info = db.get_user_info_by_id(raw_mail['receiver_id'])
        mail_list.append({'sender_id': str(raw_mail['sender_id']),
                          'receiver_id': str(raw_mail['receiver_id']),
                          'sender_name': sender_info['name'],
                          'receiver_name': receiver_info['name'],
                          'send_timestamp': raw_mail['send_timestamp'],
                          'mail_msg': raw_mail['msg'],  })
    
    res = {}
    res['code'] = 0
    res['msg'] = r'邮件加载成功'
    res['count'] = raw_mail_list.count()
    res['mail_list'] = mail_list
    return HttpResponse(json.dumps(res), )


def get_email_count_action(request):
    user_id = ObjectId(request.POST['userid'])
    req_timestamp = long(request.POST['timestamp'])
    
    res = {}
    res['code'] = 0
    res['msg'] = r'获取新邮件计数成功'
    res['count'] = db.get_email_count_by_timestamp_user_id(req_timestamp, 
                                                           user_id)
    return HttpResponse(json.dumps(res), )

