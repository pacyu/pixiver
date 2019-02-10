import re
from bs4 import BeautifulSoup
from pixiver.exceptions import PixivError
from pixiver.baseiv import ConfigHeaders


class Pixiv(ConfigHeaders):
    init_url = 'https://www.pixiv.net'
    login_url = 'https://accounts.pixiv.net/login'
    login_api = 'https://accounts.pixiv.net/api/login'
    kvpair = {
        'return_to': init_url,
        'cookie': False
    }

    def __init__(self, username=None, password=None, **kwargs):
        super().__init__()
        self.username = username
        self.password = password
        self.kvpair.update(kwargs)

        if self.kvpair['cookie']:
            cookie = open('C:/cookie.txt').read()

            self.sess.headers.update({
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': cookie
            })

        self.token = self.get_token()

        if username and password:
            self.__login__()

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

        log_msg = login.json()

        if log_msg['error']:
            raise PixivError(log_msg['message'])

        if 'validation_errors' not in log_msg['body']:
            print('Login success!')
        else:
            raise PixivError(
                log_msg['body']['validation_errors']['pixiv_id']
            )

    def login(self, username, passwrod):
        self.username = username
        self.password = passwrod
        self.__init__(username=username, password=passwrod)

    def get_token(self):
        r = self.sess.get(
            'https://www.pixiv.net/ranking.php?mode=daily',
            timeout=5
        )
        reg = re.compile(r'.*pixiv.context.token = "([a-z0-9]{32})"?.*')
        token = reg.findall(r.text)[0]
        return token

    def run(self):
        pass
