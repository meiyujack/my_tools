from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class WebSecurity:

    def __init__(self, secret_key, info):
        self.info = info
        self.serializer = URLSafeTimedSerializer(secret_key)

    def generate_token(self):
        token = self.serializer.dumps(self.info)
        return token

    def get_info_by_token(self, token):
        try:
            payload = self.serializer.loads(token)
        except BadSignature or SignatureExpired:
            return None
        return payload

    def check_token(self, token):
        try:
            self.serializer.loads(token)
        except BadSignature or SignatureExpired:
            return False
        return True
