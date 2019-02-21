import re
import time
from requests import Session
from . import exceptions
from http.cookies import BaseCookie


class BasicConfig(object):
    sess = Session()
    token = None
    user_id = None
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' \
                 ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                 ' Chrome/71.0.3578.98 Safari/537.36'

    def __init__(self, headers=None, token=None, user_id=None):
        if headers:
            self.sess.headers.update(headers)
        else:
            self.sess.headers.update({
                'Accept-Encoding': 'gzip, deflate, br',
                'User-Agent': self.user_agent,
            })

        if token:
            self.token = token

        if user_id:
            self.user_id = user_id


class Login(BasicConfig):
    init_url = 'https://www.pixiv.net'
    login_api = 'https://accounts.pixiv.net/api/login'
    kvpair = {
        'return_to': init_url,
        'cookie': False
    }
    username = None
    password = None
    cookies = BaseCookie()

    def __init__(self, username=None, password=None, **kwargs):
        super(Login, self).__init__()
        self.kvpair.update(kwargs)

        if self.kvpair['cookie']:
            self.cookies.load(open(self.kvpair['path']).read())
            php_sess_id = str(self.cookies['PHPSESSID']).replace('Set-Cookie: ', '').replace('PHPSESSID=', '')
            self.user_id = php_sess_id.split('_')[0]

            self.sess.headers.update({
                'Cookie': str(self.cookies).replace('Set-Cookie: ', '').replace('\r\n', '; ')
            })

            self.pixiv = self.get_pixiv()
            self.token = self.pixiv['token']

        elif username and password:
            self.username = username
            self.password = password

            self.pixiv = self.get_pixiv()
            self.token = self.pixiv['token']
            cookie = self.pixiv['cookie']

            self.cookies['p_ab_d_id'] = cookie['p_ab_d_id']
            self.cookies['p_ab_id'] = cookie['p_ab_id']
            self.cookies['p_ab_id_2'] = cookie['p_ab_id_2']
            self.cookies['first_visit_datetime_pc'] = cookie['first_visit_datetime_pc']

            data = {
                'pixiv_id': self.username,
                'captcha': '',
                'g_recaptcha_response': '',
                'password': self.password,
                'post_key': self.token,
                'source': 'pc',
                'ref': 'wwwtop_accounts_index',
                'return_to': self.kvpair['return_to']
            }

            login = self.sess.post(self.login_api, data=data, timeout=2)
            cookie = login.cookies

            log_msg = login.json()

            if log_msg['error']:
                raise exceptions.PixivError(log_msg['message'])

            if 'validation_errors' not in log_msg['body']:
                print('Login successful!')
            else:
                raise exceptions.PixivError(
                    log_msg['body']['validation_errors']['pixiv_id']
                )

            utmc = '235335808'
            tt = time.time()
            ts = str(tt)
            tis = str(int(tt))

            self.user_id = cookie['PHPSESSID'].split('_')[0]

            self.cookies['PHPSESSID'] = cookie['PHPSESSID']
            self.cookies['device_token'] = cookie['device_token']
            self.cookies['privacy_policy_agreement'] = cookie['privacy_policy_agreement']
            self.cookies['__utmc'] = utmc
            self.cookies['__utmz'] = utmc + '.' + tis + '.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
            self.cookies['__utmv'] = utmc + '.|2=login%20ever=no=1^9=p_ab_id=2=1^10=p_ab_id_2=3=1^11=lang=zh=1'
            self.cookies['__utma'] = utmc + '.' + '864160484.' + tis + '.' + tis + '.' + ts[:12]
            self.cookies['__utmb'] = utmc + '.1.10.' + ts[:12]
            self.cookies['__utmt'] = '1'
            self.cookies['login_bc'] = '1'
            self.cookies['_ga'] = 'GA1.2.1285249302.' + ts[:12]
            self.cookies['_gid'] = 'GA1.2.1090652169.' + ts[:12]
            self.cookies['_gat'] = '1'

            r = self.sess.get(self.init_url, timeout=5)

            cookie = r.cookies

            reg = re.compile(r'.*pixiv.user.premium = ([a-zA-Z]{4,5})')
            is_pre = reg.findall(r.text)[0]
            if is_pre == 'true':
                plan = 'premium'
            else:
                plan = 'normal'

            self.cookies['a_type'] = cookie['a_type']
            self.cookies['b_type'] = cookie['b_type']
            self.cookies['c_type'] = cookie['c_type']
            self.cookies['module_orders_mypage'] = cookie['module_orders_mypage']
            self.cookies['is_sensei_service_user'] = cookie['is_sensei_service_user']
            self.cookies['yuid_b'] = cookie['yuid_b']
            self.cookies['login_ever'] = 'yes'
            self.cookies['__utmv'] = utmc + '.|2=login%20ever=yes=1^3=plan=' \
                                          + plan \
                                          + '=1^6=user_id=' \
                                          + self.user_id \
                                          + '=1^9=p_ab_id=9=1^10=p_ab_id_2=0=1^11=lang=zh=1'

            self.sess.headers.update({
                'Cookie': str(self.cookies).replace('Set-Cookie: ', '').replace('\r\n', '; ')
            })

    def login(self, username, password):
        self.username = username
        self.password = password
        self.__init__(username=username, password=password)

    def get_pixiv(self):
        r = self.sess.get(self.init_url, timeout=5)
        reg = re.compile(r'.*pixiv.context.token = "([a-z0-9]{32})"?.*')
        return {'token': reg.findall(r.text)[0], 'cookie': r.cookies}


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
