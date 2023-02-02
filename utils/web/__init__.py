from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class WebSecurity:

    def __init__(self, secret_key):
        self.serializer = URLSafeTimedSerializer(secret_key)

    def generate_token(self,info):
        token = self.serializer.dumps(info)
        return token

    def get_info_by_token(self, token):
        try:
            info = self.serializer.loads(token)
        except BadSignature or SignatureExpired:
            return None
        return info

    def check_token(self, token):
        try:
            self.serializer.loads(token)
        except BadSignature or SignatureExpired:
            return False
        return True
