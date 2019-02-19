from requests.compat import quote_plus
from PIL import Image
from io import BytesIO
from pixiver import basiciv
from pixiver.tagiv import WorksTag
from pixiver.useriv import User


class Discussion(basiciv.BasicConfig, basiciv.Queue):

    def __init__(self, illust_id, comments_count, **kwargs):
        super(Discussion, self).__init__(**kwargs)
        self.url = 'https://www.pixiv.net/ajax/illusts/comments/roots?' \
                   'illust_id=%s&offset=0&limit=%s' % (
                       illust_id,
                       comments_count
                   )
        r = self.sess.get(
            self.url,
            timeout=5
        )
        self.info_json = r.json()

        if self.info_json['error']:
            raise basiciv.exceptions.AjaxRequestError(
                self.info_json['message']
            )
        elif not self.info_json['body']:
            self.info_json['body'] = {'comments': None}

        self.que_tar = self.info_json['body']['comments']


class Works(basiciv.BasicConfig):
    base_tags_que = None
    user_comments = None
    im_data = None
    im_mini = None
    im_small = None
    im_thumb = None
    im_regular = None
    im_original = None
    im_name = None

    def __init__(self, illust_id=None, **kwargs):
        super(Works, self).__init__(**kwargs)
        if illust_id:
            self.url = 'https://www.pixiv.net/ajax/illust/' \
                       '%s' % illust_id
            r = self.sess.get(
                self.url,
                headers={
                    'x-user-id': self.user_id
                },
                timeout=5
            )
            info = r.json()

            if info['error']:
                raise basiciv.exceptions.AjaxRequestError(
                    info['message']
                )

            self.info = info['body']

    def all(self):
        return self.info

    def create_date(self):
        return self.info['createDate']

    def upload_date(self):
        return self.info['uploadDate']

    def illust_id(self):
        return self.info['id']

    def imsize(self):
        return (self.info['height'],
                self.info['width'])

    def illust_title(self):
        return self.info['title']

    def comment_count(self):
        return self.info['commentCount']

    def mark_count(self):
        return self.info['bookmarkCount']

    def like_count(self):
        return self.info['likeCount']

    def view_tags(self):
        if self.base_tags_que is None:
            tags_que = self.info['tags']['tags']
            self.base_tags_que = basiciv.Queue([
                WorksTag(quote_plus(tag['tag'])) for tag in tags_que])
        return self.base_tags_que

    def mini_url(self):
        return self.info['urls']['mini']

    def thumb_url(self):
        return self.info['urls']['thumb']

    def small_url(self):
        return self.info['urls']['small']

    def original_url(self):
        return self.info['urls']['original']

    def regular_url(self):
        return self.info['urls']['regular']

    def author_name(self):
        return self.info['userName']

    def author_id(self):
        return self.info['userId']

    def view_count(self):
        return self.info['viewCount']

    def view_comments(self):
        if not self.user_comments:
            self.user_comments = Discussion(
                self.illust_id(),
                self.comment_count()
            )
        return self.user_comments

    def view_mini_image(self):
        if not self.im_mini:
            illust_url = self.mini_url()
            self.im_name = illust_url.split('/')[-1]
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
            }
            rg = self.sess.get(
                illust_url,
                headers=headers,
                timeout=2
            )
            self.im_mini = rg.content

        self.im_data = self.im_mini

        im = Image.open(BytesIO(self.im_mini))
        im.show()

    def view_thumb_image(self):
        if not self.im_thumb:
            illust_url = self.thumb_url()
            self.im_name = illust_url.split('/')[-1]
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
            }
            rg = self.sess.get(
                illust_url,
                headers=headers,
                timeout=2
            )
            self.im_thumb = rg.content

        self.im_data = self.im_thumb

        im = Image.open(BytesIO(self.im_thumb))
        im.show()

    def view_small_image(self):
        if not self.im_small:
            illust_url = self.small_url()
            self.im_name = illust_url.split('/')[-1]
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
            }
            rg = self.sess.get(
                illust_url,
                headers=headers,
                timeout=2
            )
            self.im_small = rg.content

        self.im_data = self.im_small

        im = Image.open(BytesIO(self.im_small))
        im.show()

    def view_regul_image(self):
        if not self.im_regular:
            illust_url = self.regular_url()
            self.im_name = illust_url.split('/')[-1]
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
            }
            rg = self.sess.get(
                illust_url,
                headers=headers,
                timeout=2
            )
            self.im_regular = rg.content

        self.im_data = self.im_regular

        im = Image.open(BytesIO(self.im_regular))
        im.show()

    def view_orig_image(self):
        if not self.im_original:
            illust_url = self.original_url()
            self.im_name = illust_url.split('/')[-1]
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
            }
            rg = self.sess.get(
                illust_url,
                headers=headers,
                timeout=2
            )
            self.im_original = rg.content

        self.im_data = self.im_original

        im = Image.open(BytesIO(self.im_original))
        im.show()

    def save(self):
        if self.im_data:
            with open(self.im_name, 'wb') as f:
                f.write(self.im_data)
            print('Saved!')

    def save_original(self):
        if not self.im_original:
            illust_url = self.original_url()
            self.im_name = illust_url.split('/')[-1]
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
            }
            rg = self.sess.get(
                self.original_url(),
                headers=headers,
                timeout=2
            )
            self.im_original = rg.content

        with open(self.im_name, 'wb') as f:
            f.write(self.im_original)
        print('Saved!')

    def like(self):
        if 'Cookie' not in self.sess.headers:
            raise basiciv.exceptions.PixivError('You must login before use functional!')

        sepst = self.sess.post(
            'https://www.pixiv.net/ajax/illusts/like',
            json={
                'illust_id': self.illust_id(),
            },
            headers={
                'x-csrf-token': self.token
            }
        ).json()
        if not sepst['error']:
            print('Liked!')
        else:
            raise basiciv.exceptions.AjaxRequestError(sepst['message'])

    def mark(self):
        if 'Cookie' not in self.sess.headers:
            raise basiciv.exceptions.PixivError('You must login before use functional!')

        sepst = self.sess.post(
            'https://www.pixiv.net/ajax/illusts/bookmarks/add',
            json={
                'comment': '',
                'illust_id': self.illust_id(),
                'restrict': 0,
                'tags': []
            },
            headers={
                'x-csrf-token': self.token
            }
        ).json()
        if not sepst['error']:
            print('Marked!')
        else:
            raise basiciv.exceptions.AjaxRequestError(sepst['message'])

    def bookmark(self):
        if 'Cookie' not in self.sess.headers:
            raise basiciv.exceptions.PixivError('You must login before use functional!')

        sepst = self.sess.post(
            'https://www.pixiv.net/bookmark_add.php',
            data={
                'mode': 'add',
                'type': 'user',
                'user_id': self.author_id(),
                'tags': '',
                'restrict': 0,
                'format': 'json',
            },
            headers={
                'x-csrf-token': self.token
            }
        ).json()
        if not sepst:
            print('Bookmarked!')
        else:
            # Maybe have a bug
            raise basiciv.exceptions.AjaxRequestError(sepst['message'])

    def author(self):
        return User(self.author_id())
