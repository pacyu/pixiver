from pixiver import pixiv, baseiv, imageiv
from pixiver.exceptions import AjaxRequestError


class User(pixiv.Pixiv, baseiv.PixivInitSay):
    person_json = {}
    profile_json = {}
    following_all = baseiv.BaseQueue()

    def __init__(self, user_id=None, username=None, password=None):
        super().__init__(username=username, password=password)

        if user_id:
            print(self.init_run)
            self.user_id = user_id

            person = 'https://www.pixiv.net/ajax/user/%s?' \
                     'full=1' % user_id
            profile = 'https://www.pixiv.net/ajax/user/%s/profile/' \
                      'all' % user_id

            self.sess.headers['Referer'] = \
                'https://www.pixiv.net/member.php?' \
                'id=%s' % user_id

            person_req = self.sess.get(
                person, headers=self.sess.headers, timeout=5
            )
            self.person_json.update(person_req.json())

            if self.person_json['error']:
                raise AjaxRequestError(
                    self.person_json['message']
                )

            self.username = self.person_json['body']['name']
            self.following_total = self.person_json['body']['following']
            self.social = self.person_json['body']['social']
            self.premium = self.person_json['body']['premium']

            profile_request = self.sess.get(
                profile, headers=self.sess.headers, timeout=5
            )
            self.profile_json.update(profile_request.json())

            if self.profile_json['error']:
                raise AjaxRequestError(
                    self.profile_json['message']
                )

            self.illusts = baseiv.BaseQueue(list(
                self.profile_json['body']['illusts'].keys()
            ))
            if 'manga' in self.profile_json['body']:
                self.mangas = baseiv.BaseQueue(list(
                    self.profile_json['body']['manga'].keys()
                ))

            self.sess.headers['Referer'] = \
                'https://www.pixiv.net/bookmark.php?' \
                'id=%s&type=user' % self.user_id

            offset = 0
            while offset < self.following_total:
                following = 'https://www.pixiv.net/ajax/user/%s/following?' \
                            'offset=%s&limit=20&rest=show' % (
                                self.user_id, offset)

                follow_request = self.sess.get(
                    following, headers=self.sess.headers, timeout=5
                )
                follow_json = follow_request.json()

                if follow_json['error']:
                    raise AjaxRequestError(
                        follow_json['message']
                    )

                for users_iter in follow_json['body']['users']:
                    self.following_all.que_tar.append(users_iter)
                offset += 20

            print(self.init_finished)

    def run(self, user_id=None):
        self.__init__(user_id)
