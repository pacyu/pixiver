import re
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from pixiver import exceptions
from pixiver import baseiv
from pixiver.helperiv import check_date


class ImageTag(baseiv.ConfigHeaders):

    def __init__(self, tag):
        self.url = 'https://www.pixiv.net/ajax/tag/' \
                   '%s/info' % tag
        self.im_data = None

        self.headers = {'User-Agent': self.user_agent}
        r = requests.get(self.url, headers=self.headers,
                         timeout=5)
        self.info_json = r.json()
        self.im_tag_url = self.info_json['body']['thumbnail']
        self.im_name = self.im_tag_url.split('/')[-1]
        self.illust_id = self.im_name.split('.')[0]\
            .replace('_p0_master1200', '')\
            .replace('_p0', '')

    def get_info(self):
        if self.info_json['error']:
            raise exceptions.AjaxRequestError(
                self.info_json['message']
            )
        return self.info_json['body']

    def view_thumbnail_image(self):
        if not self.im_data:
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id,
                'User-Agent': self.user_agent
            }
            rg = requests.get(self.im_tag_url, headers=self.headers,
                              timeout=2)
            self.im_data = rg.content

        im = Image.open(BytesIO(self.im_data))
        im.show()

    def save_tag_image(self):
        if not self.im_data:
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id,
                'User-Agent': self.user_agent
            }
            rg = requests.get(self.im_tag_url, headers=self.headers,
                              timeout=2)
            self.im_data = rg.content

        with open(self.im_name, 'wb') as f:
            f.write(self.im_data)
        print('Saved!')


class ImageComment(baseiv.BaseQueue, baseiv.ConfigHeaders):

    def __init__(self, illust_id, comments_count):
        super().__init__()
        self.url = 'https://www.pixiv.net/ajax/illusts/comments/roots?' \
                   'illust_id=%s&offset=0&limit=%s' % (
                       illust_id,
                       comments_count
                   )
        self.headers = {'User-Agent': self.user_agent}
        r = requests.get(self.url, headers=self.headers,
                         timeout=5)
        self.info_json = r.json()

    def get_info(self):
        if self.info_json['error']:
            raise exceptions.AjaxRequestError(
                self.info_json['message']
            )
        self.que_tar = self.info_json['body']['comments']
        return self.que_tar


class PixivImage(baseiv.ConfigHeaders):
    base_tags_que = None
    user_comments = None
    im_data = None
    im_name = None
    orig_im = None

    def __init__(self, illust_id):
        self.url = 'https://www.pixiv.net/ajax/illust/' \
                   '%s' % illust_id
        self.headers = {
            'User-Agent': self.user_agent
        }
        r = requests.get(self.url, headers=self.headers,
                         timeout=5)
        info = r.json()
        if info['error']:
            raise exceptions.AjaxRequestError(
                self.info['message']
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

    def tags(self):
        tags_que = self.info['tags']['tags']
        if self.base_tags_que is None:
            self.base_tags_que = baseiv.BaseQueue([{
                'tag_info': ImageTag(tag['tag']),
            } for tag in tags_que])
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

    def user_name(self):
        return self.info['userName']

    def view_count(self):
        return self.info['viewCount']

    def view_comments(self):
        if not self.user_comments:
            self.user_comments = ImageComment(
                self.illust_id(),
                self.comment_count()
            )
        return self.user_comments

    def view_mini_image(self):
        if not self.im_data:
            illust_url = self.mini_url()
            self.im_name = illust_url.split('/')[-1]
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
                'User-Agent': self.user_agent
            }
            rg = requests.get(illust_url, headers=self.headers,
                              timeout=2)
            self.im_data = rg.content

        im = Image.open(BytesIO(self.im_data))
        im.show()

    def view_thumb_image(self):
        if not self.im_data:
            illust_url = self.thumb_url()
            self.im_name = illust_url.split('/')[-1]
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
                'User-Agent': self.user_agent
            }
            rg = requests.get(illust_url, headers=self.headers,
                              timeout=2)
            self.im_data = rg.content

        im = Image.open(BytesIO(self.im_data))
        im.show()

    def view_small_image(self):
        if not self.im_data:
            illust_url = self.small_url()
            self.im_name = illust_url.split('/')[-1]
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
                'User-Agent': self.user_agent
            }
            rg = requests.get(illust_url, headers=self.headers,
                              timeout=2)
            self.im_data = rg.content

        im = Image.open(BytesIO(self.im_data))
        im.show()

    def view_regul_image(self):
        if not self.im_data:
            illust_url = self.regular_url()
            self.im_name = illust_url.split('/')[-1]
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
                'User-Agent': self.user_agent
            }
            rg = requests.get(illust_url, headers=self.headers,
                              timeout=2)
            self.im_data = rg.content

        im = Image.open(BytesIO(self.im_data))
        im.show()

    def view_orig_image(self):
        if not self.im_data:
            illust_url = self.original_url()
            self.im_name = illust_url.split('/')[-1]
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
                'User-Agent': self.user_agent
            }
            rg = requests.get(illust_url, headers=self.headers,
                              timeout=2)
            self.im_data = rg.content

        im = Image.open(BytesIO(self.im_data))
        im.show()

    def save(self):
        if not self.im_data:
            self.save_original()
        else:
            with open(self.im_name, 'wb') as f:
                f.write(self.im_data)
            print('Saved!')

    def save_original(self):
        if not self.orig_im:
            illust_url = self.original_url()
            self.im_name = illust_url.split('/')[-1]
            self.headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id(),
                'User-Agent': self.user_agent
            }
            rg = requests.get(self.original_url(), headers=self.headers,
                              timeout=2)
            self.orig_im = rg.content
            self.im_data = self.orig_im

        with open(self.im_name, 'wb') as f:
            f.write(self.orig_im)
        print('Saved!')


class DailyImages(baseiv.BaseQueue):

    def __init__(self, illust_attr, rank_date, rank):
        super().__init__()
        self.que_tar = [
            {
                'illust_attrs': zip_[0],
                'rank_date': zip_[1],
                'rank': zip_[2]
            } for zip_ in zip(illust_attr, rank_date, rank)
        ]


class Daily(baseiv.ConfigHeaders, baseiv.PixivInitSay):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=daily'
    curr_one = {}
    curr_batch = []
    rank_total = 0
    subscript = 0
    params = {
        'format': 'json'
    }
    current_page = 1

    def __init__(self, daily=None):

        if daily:
            reg = re.compile(
                r'[0-9]{4}[^a-zA-Z0-9]?[0-9]{2}[^a-zA-Z0-9]?[0-9]{2}'
            )
            s = reg.fullmatch(str(daily))
            date = s.string
            date = date.replace('/', '')\
                .replace('-', '')\
                .replace('.', '')

            year = int(date[:4])
            mouth = int(date[4:6])
            day = int(date[6:])

            check_date(year, mouth, day)

            self.params = {
                'date': date,
                'format': 'json',
            }
            self.current_date = date
            self.__run__(params=self.params)

    def __run__(self, params):
        print(self.init_run)
        self.init_run = 'Current date: {}, page: {},' \
                        ' batch_size: {}, rank total: {}\n' \
                        'Loading date: {}, page: {} ...' \
            .format(
                self.current_date, self.current_page,
                len(self.curr_batch), self.rank_total,
                params['date'], params['p']
            )
        headers = {'User-Agent': self.user_agent}
        r = requests.get(self.init_url, params=params,
                         headers=headers, timeout=5)
        self.daily_json = r.json()
        if self.rank_total == 0:
            self.rank_total = self.daily_json['rank_total']
        self.current_page = self.daily_json['page']
        self.current_date = self.daily_json['date']
        print(self.init_finished)
        self.init_finished = 'Load finished!'

    def run(self, daily=None):
        if daily:
            reg = re.compile(
                r'[0-9]{4}[^a-zA-Z0-9]?[0-9]{2}[^a-zA-Z0-9]?[0-9]{2}'
            )
            s = reg.fullmatch(str(daily))
            date = s.string
            date = date.replace('/', '')\
                .replace('-', '')\
                .replace('.', '')

            year = int(date[:4])
            mouth = int(date[4:6])
            day = int(date[6:])

            check_date(year, mouth, day)

            self.params = {
                'date': date,
                'format': 'json',
            }

            self.current_date = date

        self.__run__(self.params)
        return self

    def one(self):
        self.curr_one = {
            'illust_attrs': PixivImage(
                self.daily_json['contents'][self.subscript]['illust_id']
            ),
            'rank_date': self.daily_json['date'],
            'rank': self.daily_json['contents'][self.subscript]['rank']
        }
        self.curr_batch.append(self.curr_one)
        return self.curr_one

    def batch(self):
        list1, list2, list3 = [], [], []
        for take in self.daily_json['contents']:
            list1.append(PixivImage(take['illust_id']))
            list2.append(self.daily_json['date'])
            list3.append(take['rank'])

        curr_batch = DailyImages(
            illust_attr=list1,
            rank_date=list2,
            rank=list3
        )
        self.curr_batch = curr_batch.que_tar
        return curr_batch

    def first(self):
        return self.curr_batch[0]

    def last(self):
        return self.curr_batch[len(self.curr_batch) - 1]

    def curr(self):
        return self.curr_batch[self.subscript]

    def prev(self):
        if self.subscript > 0:
            self.subscript -= 1
            return self.curr_batch[self.subscript]
        else:
            print('first!')

    def next(self):
        if self.subscript < len(self.curr_batch) - 1:
            self.subscript += 1
            return self.curr_batch[self.subscript]
        else:
            print('last!')

    def curr_date(self):
        return self.daily_json['date']

    def prev_date(self):
        if self.daily_json['prev_date']:
            self.rank_total = 0
            self.curr_batch.clear()
            self.params = {
                'date': self.daily_json['prev_date'],
                'p': self.daily_json['page'],
                'format': 'json',
            }
            return self.run()

    def next_date(self):
        if self.daily_json['next_date']:
            self.rank_total = 0
            self.curr_batch.clear()
            self.params = {
                'date': self.daily_json['next_date'],
                'p': self.daily_json['page'],
                'format': 'json',
            }
            return self.run()

    def curr_page(self):
        return self.daily_json['page']

    def prev_page(self):
        if self.daily_json['prev']:
            self.params = {
                'date': self.daily_json['date'],
                'p': self.daily_json['prev'],
                'format': 'json',
            }
            return self.run()

    def next_page(self):
        if self.daily_json['next']:
            self.params = {
                'date': self.daily_json['date'],
                'p': self.daily_json['next'],
                'format': 'json',
            }
            return self.run()

    def get_token(self):
        url = 'https://www.pixiv.net/ranking.php?mode=daily'
        headers = {
            'Referer': 'https://www.pixiv.net/ranking.php?'
                       'mode=daily',
            'User-Agent': self.user_agent
        }
        r = requests.get(url, headers=headers, timeout=5)
        doc = r.text
        soup = BeautifulSoup(doc, 'html.parser')
        script = soup.find_all('script')
        reg = re.compile(r'.*token = "([a-z0-9]{32})"?.*')
        token = reg.findall(script[11].string)
        return token


class Weekly(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=weekly'


class Mouthly(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=monthly'


class Rookie(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=rookie'


class Original(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=original'


class Male(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=male'


class Female(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=female'


class DailyR(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=daily_r18'


class WeeklyR(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=weekly_r18'


class MaleR(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=male_r18'


class FemaleR(Daily):
    init_url = 'https://www.pixiv.net/ranking.php?' \
               'mode=female_r18'
