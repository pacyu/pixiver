from requests import Session
from bs4 import BeautifulSoup


class Pixiv(object):
    init_url = 'https://www.pixiv.net'
    login_url = 'https://accounts.pixiv.net/login'
    login_api = 'https://accounts.pixiv.net/api/login'
    kvpair = {'return_to': init_url}

    def __init__(self, username=None, password=None, **kwargs):
        self.username = username
        self.password = password
        self.sess = Session()
        self.sess.headers.update({
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/63.0.3239.132 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive'})
        self.kvpair.update(kwargs)
        if username and password:
            self.login(username, password)

    def __login__(self):
        requ = self.sess.get(self.login_url, timeout=5)
        doc = requ.text
        soup = BeautifulSoup(doc, 'html.parser')
        csrf_ = soup.input['value']
        data = {
            'pixiv_id': self.username,
            'captcha': '',
            'g_recaptcha_response': '',
            'password': self.password,
            'post_key': csrf_,
            'source': 'pc',
            'ref': 'wwwtop_accounts_index',
            'return_to': self.kvpair['return_to']
        }
        login = self.sess.post(self.login_api, data=data, timeout=2)
        self.sess.headers.update(login.headers)
        log_msg = login.json()

        if not log_msg['error']:
            if 'validation_errors' not in log_msg['body']:
                print('login success')
            else:
                print(log_msg['body']['validation_errors']['pixiv_id'])
                exit(1)
        else:
            print(log_msg['message'])
            exit(1)

    def login(self, username, passwrod):
        self.username = username
        self.password = passwrod
        self.__login__()

    def run(self):
        pass
