from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class WebSecurity:

    def __init__(self, secret_key, max_age):
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.max_age = max_age

    def generate_token(self, info):
        token = self.serializer.dumps(info)
        return token

    def get_info_by_token(self, token, key):
        """
       获取加密内容
       :param token: 待解析内容
       :param key: 待解析内容的key
       :return: Any|None
       """
        try:
            info = self.serializer.loads(token, max_age=self.max_age)
        except BadSignature or SignatureExpired as ex:
            return ex
        return info[key]

    def check_token(self, token):
        try:
            self.serializer.loads(token)
        except BadSignature or SignatureExpired:
            return False
        return True
