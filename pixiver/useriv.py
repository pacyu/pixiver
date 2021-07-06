from . import basiciv
from . import worksiv


class User(basiciv.BasicConfig):

    def __init__(self, author_id=None, **kwargs):
        super(User, self).__init__(**kwargs)
        self.author_id = author_id
        self.following_all = basiciv.Queue()

        if author_id:
            person = 'https://www.pixiv.net/ajax/user/%s?' \
                     'full=1' % author_id
            profile = 'https://www.pixiv.net/ajax/user/%s/profile/' \
                      'all' % author_id

            self.sess.headers['Referer'] = \
                'https://www.pixiv.net/member.php?' \
                'id=%s' % author_id

            person_req = self.sess.get(
                person, headers=self.sess.headers, timeout=self.kvpair['timeout']
            )
            self.person_interface = person_req.json()

            if self.person_interface['error']:
                raise basiciv.exceptions.AjaxRequestError(
                    self.person_interface['message']
                )

            self.author_name = self.person_interface['body']['name']
            self.following_total = self.person_interface['body']['following']
            self.social = self.person_interface['body']['social']
            self.premium = self.person_interface['body']['premium']

            profile_request = self.sess.get(
                profile, headers=self.sess.headers, timeout=self.kvpair['timeout']
            )
            self.profile_interface = profile_request.json()

            if self.profile_interface['error']:
                raise basiciv.exceptions.AjaxRequestError(
                    self.profile_interface['message']
                )

            if 'illusts' in self.profile_interface['body']:
                self.illusts = basiciv.Queue([
                    worksiv.Works(illust_id=illust_id) for illust_id in list(
                        self.profile_interface['body']['illusts'].keys()
                    )])

            if 'manga' in self.profile_interface['body']:
                self.mangas = basiciv.Queue([
                    worksiv.Works(illust_id=illust_id) for illust_id in list(
                        self.profile_interface['body']['manga'].keys()
                    )])

            self.sess.headers['Referer'] = \
                'https://www.pixiv.net/bookmark.php?' \
                'id=%s&type=user' % self.author_id

            offset = 0
            while offset < self.following_total:
                following = 'https://www.pixiv.net/ajax/user/%s/following?' \
                            'offset=%s&limit=20&rest=show' % (
                                self.author_id, offset)

                follow_request = self.sess.get(
                    following, headers=self.sess.headers, timeout=self.kvpair['timeout']
                )
                follow_interface = follow_request.json()

                if follow_interface['error']:
                    raise basiciv.exceptions.AjaxRequestError(
                        follow_interface['message']
                    )

                for users_iter in follow_interface['body']['users']:
                    self.following_all.que_tar.append(users_iter)
                offset += 20

    def details(self):
        return self.person_interface['body']

    def run(self, author_id=None):
        self.__init__(author_id)

    def bookmark(self):
        if 'Cookie' not in self.sess.headers:
            raise basiciv.exceptions.PixivError('You must be logged in before using this feature!')

        interface = self.sess.post(
            'https://www.pixiv.net/bookmark_add.php',
            data={
                'mode': 'add',
                'type': 'user',
                'user_id': self.author_id,
                'tags': '',
                'restrict': 0,
                'format': 'json',
            },
            headers={
                'x-csrf-token': self.token
            }
        ).json()
        if not interface['error']:
            return True
        else:
            raise basiciv.exceptions.AutheVerifyError(interface['message'])
