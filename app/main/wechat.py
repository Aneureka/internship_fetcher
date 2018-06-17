# -*- coding: utf-8 -*-

from . import main
import os
from flask import request
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply
from app.utils.log_util import get_logger
from app.wechat.wechat_sdk import wechat_client


@main.route('/wechat', methods=['GET', 'POST'])
def wechat_core():
    if request.method == 'GET':
        """verifying"""
        data = request.args.to_dict()
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        token = os.environ.get('TOKEN')
        logger = get_logger()
        try:
            check_signature(token, signature, timestamp, nonce)
            logger.info('check signature successfully')
            return token
        except InvalidSignatureException:
            logger.warning('invalid signature from wechat')
            return 'Invalid request from wechat!'
    else:
        msg = parse_message(request.data)
        reply = TextReply(content='对话还没做嘤嘤嘤QAQ', message=msg)
        return reply.render()


@main.route('/wechat/access_token', methods=['GET'])
def access_token():
    data = request.args.to_dict()
    key = data.get('key')
    if not key or key != os.environ.get('ACCESS_TOKEN_KEY'):
        return 'You are not authorized to view the access token!'
    return wechat_client.access_token


