import json

import sentry_sdk
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from lwjTest.settings import logger

import uuid
def gen_uuid():
    return str(uuid.uuid1()).replace('-', '')

def _get_request_headers(request):
    headers = {}
    for k, v in request.META.items():
        if k.startswith('HTTP_'):
            headers[k[5:].lower()] = v
    return headers


def _get_response_headers(response):
    headers = {}
    headers_tuple = response.items()
    for i in headers_tuple:
        headers[i[0]] = i[1]
    return headers


NOT_SUPPORT_PATH = '/admin'  # 排除 admin 站点，admin 站点不会进入CollectionMiddleware的process_response方法，会导致报错


class CollectionMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 增加判断，如果请求的 path 是以/admin/开头的，则直接放过，不做任何处理
        if request.path.startswith(NOT_SUPPORT_PATH):
            pass
        else:
            logger.info('进入CollectionMiddleware，收集请求数据')
            if str(request.body, encoding='utf-8')!="":
                request.META['REQUEST_BODY'] = json.loads(str(request.body, encoding='utf-8').replace(' ', '').replace('\n',
                                                                                                                       '').replace(
                    '\t',
                    ''))
            else:
                request.META['REQUEST_BODY']=""

            if 'HTTP_X_FORWARDED_FOR' in request.META:
                remote_address = request.META['HTTP_X_FORWARDED_FOR']
            else:
                remote_address = request.META['REMOTE_ADDR']
            request.META['IP'] = remote_address

            request.META['LOG_UUID'] = gen_uuid()

    def process_response(self, request, response):
        # 增加判断，如果请求的 path 是以/admin/开头的，则直接放过，不做任何处理
        if request.path.startswith(NOT_SUPPORT_PATH):
            pass
        else:

            logger.info('进入CollectionMiddleware，收集响应数据')

            # 获取请求的 uid，如果是未登录的则为 None
            if not isinstance(request.user, AnonymousUser):
                uid = request.user.uid
            else:
                uid = None
            request.META['USER_UID'] = uid

            # 获取响应内容
            if response['content-type'] == 'application/json':
                if getattr(response, 'streaming', False):
                    response_body = '<<<Streaming>>>'
                else:
                    response_body = json.loads(str(response.content, encoding='utf-8'))
            else:
                response_body = '<<<Not JSON>>>'
            request.META['RESP_BODY'] = response_body

            # 获取请求的 view 视图名称
            try:
                request.META['VIEW'] = request.resolver_match.view_name
            except AttributeError:
                request.META['VIEW'] = None

            request.META['STATUS_CODE'] = response.status_code

            # 设置 headers: X-Log-Id
            response.setdefault('X-Log-Id', request.META['LOG_UUID'])

        return response


class LoggerMiddleware(MiddlewareMixin):
    """
    中间件，记录日志
    """

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        # 增加判断，如果请求的 path 是以/admin/开头的，则直接放过，不做任何处理
        if request.path.startswith(NOT_SUPPORT_PATH):
            pass
        else:
            logger.info('进入LoggerMiddleware，写日志')
            log_data = {
                'request': {
                    'uid': request.META['USER_UID'],
                    "ip": request.META['IP'],
                    "method": request.method,
                    'path': request.get_full_path(),
                    'view': request.META['VIEW'],
                    'body': request.META['REQUEST_BODY'],
                    'headers': _get_request_headers(request),
                },
                'response': {
                    'status': request.META['STATUS_CODE'],
                    'body': request.META['RESP_BODY'],
                    'headers': _get_response_headers(response),
                },
                'log_uuid': request.META['LOG_UUID']
            }
            logger.info(json.dumps(log_data))
        return response


class SentryMiddleware(MiddlewareMixin):
    """
    上报 sentry
    """

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        # 增加判断，如果请求的 path 是以/admin/开头的，则直接放过，不做任何处理
        if request.path.startswith(NOT_SUPPORT_PATH):
            pass
        else:
            logger.info('进入SentryMiddleware，上报请求至Sentry')
            sentry_sdk.add_breadcrumb(
                category='path',
                message=request.path,
                level='info',
            )

            sentry_sdk.add_breadcrumb(
                category='body',
                message=request.META["REQUEST_BODY"],
                level='info',
            )

            sentry_sdk.add_breadcrumb(
                category='request_headers',
                message=_get_request_headers(request),
                level='info',
            )

            sentry_sdk.add_breadcrumb(
                category='response_headers',
                message=_get_response_headers(response),
                level='info',
            )

            sentry_sdk.add_breadcrumb(
                category='view',
                message=request.META['VIEW'],
                level='info',
            )
            sentry_sdk.set_user({"id": request.META['USER_UID']})
            sentry_sdk.set_tag("log-id", request.META["LOG_UUID"])
            sentry_sdk.capture_message(request.META["LOG_UUID"])
        return response