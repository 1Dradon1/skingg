class AuthData:
    def __init__(self, token: str, phpsessid_cookie: str):
        self.token = token
        self.phpsessid_cookie = phpsessid_cookie
