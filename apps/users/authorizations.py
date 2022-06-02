# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2020/9/6 5:54 下午
import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthentication(BaseJSONWebTokenAuthentication):
    """
    jwt认证
    """
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')

        # 自定义校验规则：auth token jwt
        token = self.parse_jwt_token(jwt_token)

        if token is None:
            return None
        try:
            # token => payload
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed({"status":"0","msg":"token已过期"})
        except:
            raise AuthenticationFailed({"status":"1","msg":"非法用户"})
        # payload => user
        user = self.authenticate_credentials(payload)

        return (user, token)

    # 自定义校验规则：jwt token
    def parse_jwt_token(self, jwt_token):
        try:
            tokens = jwt_token.split()
            if len(tokens) != 2 or tokens[0].lower() != 'jwt':
                return None
            return tokens[1]
        except:
            return "token效验失败"

