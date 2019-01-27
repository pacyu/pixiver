import pixiv


class User(pixiv.Pixiv):
    person_json = {}
    profile_json = {}
    following_json = {}

    def __init__(self, user_id, username=None, password=None):
        super().__init__(username=username, password=password)
        self.user_id = user_id
        person = 'https://www.pixiv.net/ajax/user/%s?' \
                 'full=1' % user_id
        profile = 'https://www.pixiv.net/ajax/user/%s/profile/' \
                  'all' % user_id
        following = 'https://www.pixiv.net/ajax/user/%s/following?' \
                    'offset=0&limit=20&rest=show' % user_id

        self.sess.headers['Referer'] = 'https://www.pixiv.net/member.php?' \
                                       'id=%s' % user_id
        person_req = self.sess.get(person, timeout=5)
        self.person_json = person_req.json()
        profile_request = self.sess.get(profile, timeout=5)
        self.profile_json = profile_request.json()
        self.sess.headers['Referer'] = 'https://www.pixiv.net/bookmark.php?' \
                                       'id=%s&type=user' % user_id
        follow_request = self.sess.get(following, timeout=5)
        self.following_json = follow_request.json()

    def get_name(self):
        if not self.person_json['error']:
            return self.person_json['body']['name']
        return self.person_json['message']

    def get_id(self):
        if not self.person_json['error']:
            return self.person_json['body']['userId']
        return self.person_json['message']

    def is_premium(self):
        if not self.person_json['error']:
            return self.person_json['body']['premium']
        return self.person_json['message']

    def get_social(self):
        if not self.person_json['error']:
            return self.person_json['body']['social']
        return self.person_json['message']

    def following_total(self):
        if not self.person_json['error']:
            return self.person_json['body']['following']
        return self.person_json['message']

    def get_works_all(self):
        if not self.profile_json['error']:
            return list(self.profile_json['body']['illusts'].keys()) \
                   + list(self.profile_json['body']['manga'])
        return self.profile_json['message']

    def get_following_total(self):
        if not self.following_json['error']:
            return self.following_json['body']['total']
        return self.following_json['message']

    def get_following(self):
        if not self.following_json['error']:
            return self.following_json['body']['users']
        return self.following_json['message']
