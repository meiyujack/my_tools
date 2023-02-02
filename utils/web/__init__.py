from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class WebSecurity:

    def __init__(self, info: dict, secret_key, max_age):
        self.info = info
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.max_age = max_age

    def generate_token(self):
        token = self.serializer.dumps(self.info)
        return token

    def get_info_by_token(self, token):
        """
        加密内容字典长度为1直接返回其内容（value），否则返回元组((),()...)
        :param token: 待解析内容
        :return: str|tuple|None
        """
        try:
            info = self.serializer.loads(token, max_age=self.max_age)
        except BadSignature or SignatureExpired:
            return None
        return info["".join(self.info.keys())] if len(self.info) == 1 else tuple(self.info.items())

    def check_token(self, token):
        try:
            self.serializer.loads(token)
        except BadSignature or SignatureExpired:
            return False
        return True
