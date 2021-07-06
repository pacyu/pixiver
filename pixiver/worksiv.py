from requests.compat import quote_plus
from PIL import Image
from io import BytesIO
from . import basiciv
from . import tagiv
from . import useriv


class Discussion(basiciv.BasicConfig):

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
        self.interface = r.json()

        if self.interface['error']:
            raise basiciv.exceptions.AjaxRequestError(
                self.interface['message']
            )
        elif not self.interface['body']:
            self.interface['body'] = {'comments': None}

        self.que_tar = basiciv.Queue(self.interface['body']['comments'])


class Works(basiciv.BasicConfig):
    base_tags_que = None
    user_comments = None
    im_data = None

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
                timeout=self.kvpair['timeout']
            )
            interface = r.json()

            if interface['error']:
                raise basiciv.exceptions.AjaxRequestError(
                    interface['message']
                )

            self.interface = interface['body']

    def author(self):
        return useriv.User(self.author_id())

    def details(self):
        return self.interface

    def create_date(self):
        return self.interface['createDate']

    def upload_date(self):
        return self.interface['uploadDate']

    def pages(self):
        return self.interface['pageCount']

    def illust_id(self):
        return self.interface['id']

    def imsize(self):
        return (self.interface['height'],
                self.interface['width'])

    def illust_title(self):
        return self.interface['title']

    def comment_count(self):
        return self.interface['commentCount']

    def mark_count(self):
        return self.interface['bookmarkCount']

    def like_count(self):
        return self.interface['likeCount']

    def view_tags(self):
        if self.base_tags_que is None:
            tags_que = self.interface['tags']['tags']
            self.base_tags_que = basiciv.Queue([
                tagiv.WorksTag(quote_plus(tag['tag'])) for tag in tags_que])
        return self.base_tags_que

    def mini_url(self):
        count = self.pages()
        url = self.interface['urls']['mini']
        urls = ()
        for i in range(count):
            urls += (url.replace('_p0', '_p%s' % i),)
        return urls

    def thumb_url(self):
        count = self.pages()
        url = self.interface['urls']['thumb']
        urls = ()
        for i in range(count):
            urls += (url.replace('_p0', '_p%s' % i),)
        return urls

    def small_url(self):
        count = self.pages()
        url = self.interface['urls']['small']
        urls = ()
        for i in range(count):
            urls += (url.replace('_p0', '_p%s' % i),)
        return urls

    def regular_url(self):
        count = self.pages()
        url = self.interface['urls']['regular']
        urls = ()
        for i in range(count):
            urls += (url.replace('_p0', '_p%s' % i),)
        return urls

    def original_url(self):
        count = self.pages()
        url = self.interface['urls']['original']
        urls = ()
        for i in range(count):
            urls += (url.replace('_p0', '_p%s' % i),)
        return urls

    def author_name(self):
        return self.interface['userName']

    def author_id(self):
        return self.interface['userId']

    def view_count(self):
        return self.interface['viewCount']

    def view_comments(self):
        if not self.user_comments:
            self.user_comments = Discussion(
                self.illust_id(),
                self.comment_count()
            )
        return self.user_comments

    def view_mini_image(self):
        print('Press key "s" save, non-"s" key page turn, key "Enter" determine, key "q" quit.')
        for i, illust_url in enumerate(self.mini_url()):
            self.sess.headers['Referer'] = 'https://www.pixiv.net/member_illust.php?' \
                           'mode=medium&illust_id=' + self.illust_id()
            rg = self.sess.get(illust_url, timeout=self.kvpair['timeout'])
            self.sess.headers.pop('Referer')
            self.im_data = rg.content
            im = Image.open(BytesIO(rg.content))
            im.show()
            gc = str(input())
            if gc is 's' or gc is 'S':
                if self.save(kind='mini', page_num=i):
                    gc = str(input('Continue to view? [Y] Yes | [Q] Quit'))
                    if gc is 'y' or gc is 'Y':
                        continue
            if gc is 'q' or gc is 'Q':
                break

    def view_thumb_image(self):
        print('Press key "s" save, non-"s" key page turn, key "Enter" determine, key "q" quit.')
        for i, illust_url in enumerate(self.thumb_url()):
            self.sess.headers['Referer'] = 'https://www.pixiv.net/member_illust.php?' \
                           'mode=medium&illust_id=' + self.illust_id()
            rg = self.sess.get(illust_url, timeout=self.kvpair['timeout'])
            self.sess.headers.pop('Referer')
            self.im_data = rg.content
            im = Image.open(BytesIO(rg.content))
            im.show()
            gc = str(input())
            if gc is 's' or gc is 'S':
                if self.save(kind='thumb', page_num=i):
                    gc = str(input('Continue to view? [Y] Yes | [Q] Quit'))
                    if gc is 'y' or gc is 'Y':
                        continue
            if gc is 'q' or gc is 'Q':
                break

    def view_small_image(self):
        print('Press key "s" save, non-"s" key page turn, key "Enter" determine, key "q" quit.')
        for i, illust_url in enumerate(self.small_url()):
            self.sess.headers['Referer'] = 'https://www.pixiv.net/member_illust.php?' \
                           'mode=medium&illust_id=' + self.illust_id()
            rg = self.sess.get(illust_url, timeout=self.kvpair['timeout'])
            self.sess.headers.pop('Referer')
            self.im_data = rg.content
            im = Image.open(BytesIO(rg.content))
            im.show()
            gc = str(input())
            if gc is 's' or gc is 'S':
                if self.save(kind='small', page_num=i):
                    gc = str(input('Continue to view? [Y] Yes | [Q] Quit'))
                    if gc is 'y' or gc is 'Y':
                        continue
            if gc is 'q' or gc is 'Q':
                break

    def view_regul_image(self):
        print('Press key "s" save, non-"s" key page turn, key "Enter" determine, key "q" quit.')
        for i, illust_url in enumerate(self.regular_url()):
            self.sess.headers['Referer'] = 'https://www.pixiv.net/member_illust.php?' \
                           'mode=medium&illust_id=' + self.illust_id()
            rg = self.sess.get(illust_url, timeout=10)
            self.sess.headers.pop('Referer')
            self.im_data = rg.content
            im = Image.open(BytesIO(rg.content))
            im.show()
            gc = str(input(':'))
            if gc is 's' or gc is 'S':
                if self.save(kind='regular', page_num=i):
                    gc = str(input('Continue to view? [Y] Yes | [Q] Quit\n:'))
                    if gc is 'y' or gc is 'Y':
                        continue
            if gc is 'q' or gc is 'Q':
                break

    def view_orig_image(self):
        print('Press key "s" save, non-"s" key page turn, key "Enter" determine, key "q" quit.')
        for i, illust_url in enumerate(self.original_url()):
            self.sess.headers['Referer'] = 'https://www.pixiv.net/member_illust.php?' \
                           'mode=medium&illust_id=' + self.illust_id()
            rg = self.sess.get(illust_url, timeout=self.kvpair['timeout'])
            self.sess.headers.pop('Referer')
            self.im_data = rg.content
            im = Image.open(BytesIO(rg.content))
            im.show()
            gc = str(input())
            if gc is 's' or gc is 'S':
                if self.save(kind='original', page_num=i):
                    gc = str(input('Continue to view? [Y] Yes | [Q] Quit'))
                    if gc is 'y' or gc is 'Y':
                        continue
            if gc is 'q' or gc is 'Q':
                break

    def save(self, kind='original', page_num=1):
        """
        :param kind: [mini, thumb, small, regular, original]
        :param page_num: >=0 and < pages
        :return: returns True when param is valid and image is successfully downloaded, otherwise False.
        """
        if 0 <= page_num < self.pages():
            if kind == 'mini':
                illust_url = self.mini_url()[page_num]
            elif kind == 'thumb':
                illust_url = self.thumb_url()[page_num]
            elif kind == 'small':
                illust_url = self.small_url()[page_num]
            elif kind == 'regular':
                illust_url = self.regular_url()[page_num]
            else:
                illust_url = self.original_url()[page_num]

            im_name = illust_url.split('/')[-1]
            if not self.im_data:
                headers = {
                    'Referer': 'https://www.pixiv.net/member_illust.php?'
                               'mode=medium&illust_id=' + self.illust_id(),
                }
                rg = self.sess.get(
                    illust_url,
                    headers=headers,
                    timeout=self.kvpair['timeout']
                )
                self.im_data = rg.content
            try:
                with open(im_name, 'wb') as f:
                    f.write(self.im_data)
            except IOError:
                raise basiciv.exceptions.IOError('Save original image failed!')
            return True
        else:
            raise basiciv.exceptions.PixivError('Page code error!')

    def like(self):
        if 'cookies' not in self.sess.headers:
            raise basiciv.exceptions.PixivError('You must be logged in before using this feature!')

        self.sess.headers.update({
            'referer': 'https://www.pixiv.net/member_illust.php?'
                       'mode=medium&illust_id=' + self.author_id(),
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-csrf-token': self.token,
        })
        interface = self.sess.post(
            'https://www.pixiv.net/ajax/illusts/like',
            json={'illust_id': self.illust_id()}).json()
        self.sess.headers.pop('x-csrf-token')
        self.sess.headers.pop('referer')
        if not interface['error']:
            return True
        else:
            raise basiciv.exceptions.AutheVerifyError(interface['message'])

    def mark(self):
        if 'cookies' not in self.sess.headers:
            raise basiciv.exceptions.PixivError('You must be logged in before using this feature!')

        interface = self.sess.post(
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
        if not interface['error']:
            return True
        else:
            raise basiciv.exceptions.AutheVerifyError(interface['message'])

    def bookmark(self):
        if 'cookies' not in self.sess.headers:
            raise basiciv.exceptions.PixivError('You must be logged in before using this feature!')

        interface = self.sess.post(
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
        if not interface['error']:
            return True
        else:
            raise basiciv.exceptions.AutheVerifyError(interface['message'])
