import re
import requests
from requests import Session
from . import exceptions
import json


class BasicConfig(object):
    sess = Session()
    token = None
    user_id = None
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' \
                 ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                 ' Chrome/71.0.3578.98 Safari/537.36'
    kvpair = {
        'cookie': False,
        'proxy': '',
        'save_cookies': False,
        'timeout': 8
    }

    def __init__(self, headers=None, token=None, user_id=None):
        if headers:
            self.sess.headers.update(headers)
        else:
            self.sess.headers.update({
                'accept-encoding': 'gzip, deflate, br',
                'user-agent': self.user_agent,
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin'
            })

        if token:
            self.token = token

        if user_id:
            self.user_id = user_id


class Login(BasicConfig):
    init_url = 'https://www.pixiv.net/'
    login_api = 'https://accounts.pixiv.net/api/login'
    
    username = None
    password = None

    def __init__(self, username=None, password=None, **kwargs):
        super(Login, self).__init__()
        self.kvpair.update(kwargs)

        if self.kvpair['cookie']:
            cookie_json = json.load(open('../cookies'))
            self.sess.cookies = requests.utils.cookiejar_from_dict(cookie_json)
            self.token = self.get_postkey()

        elif username and password:
            self.username = username
            self.password = password

            self.token = self.get_postkey()

            data = {
                'pixiv_id': self.username,
                'captcha': '',
                'g_recaptcha_response': '',
                'password': self.password,
                'post_key': self.token,
                'source': 'pc',
                'ref': 'wwwtop_accounts_index',
                'return_to': self.init_url
            }

            login = self.sess.post(self.login_api, data=data, timeout=self.kvpair['timeout'])

            log_msg = login.json()

            if log_msg['error']:
                raise exceptions.PixivError(log_msg['message'])

            if 'validation_errors' not in log_msg['body']:
                print('Login successful!')
            elif 'pixiv_id' in log_msg['body']['validation_errors']:
                raise exceptions.PixivError(
                    log_msg['body']['validation_errors']['pixiv_id']
                )
            elif 'captcha' in log_msg['body']['validation_errors']:
                raise exceptions.PixivError(
                    log_msg['body']['validation_errors']['captcha']
                )

            if self.kvpair['save_cookies']:
                cookie_json = requests.utils.dict_from_cookiejar(self.sess.cookies)
                json.dump(cookie_json, open('../cookies', 'w+'),)

            cookie = "; ".join([str(x) + "=" + str(y) for x, y in self.sess.cookies.items()])
            headers = {
                'cookie': cookie,
            }
            self.sess.headers.update(headers)

    def login(self, username, password):
        self.username = username
        self.password = password
        self.__init__(username=username, password=password)

    def get_postkey(self):
        r = self.sess.get(self.init_url, timeout=5)
        reg = re.compile(r'.*pixiv.context.token = "([a-z0-9]{32})"?.*')
        return reg.findall(r.text)[0]


class LoadInfo:
    init_run = 'Pixiver Initializing...'
    init_finished = 'Initialized!'


class Queue(object):
    step_number = 0
    que_tar = []

    def __init__(self, argv=None):
        if argv:
            self.que_tar = argv

    def first(self):
        return self.que_tar[0]

    def curr(self):
        return self.que_tar[self.step_number]

    def prev(self):
        if self.step_number < 0:
            raise Exception('Lower limit.')
        self.step_number -= 1
        return self.que_tar[self.step_number]

    def next(self):
        if self.step_number > len(self.que_tar) - 1:
            raise Exception('Upper limit.')
        self.step_number += 1
        return self.que_tar[self.step_number]

    def last(self):
        return self.que_tar[len(self.que_tar) - 1]

    def size(self):
        return len(self.que_tar)

    def remove(self):
        self.que_tar.pop(self.step_number)
