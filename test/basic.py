from pixiver import basiciv
import json

account = json.load(open('../pixiv_user.json'),)
login = basiciv.Login(username=account['username'], password=account['password'], save_cookies=True)
print(login.sess.cookies, '\n', login.sess.headers)
