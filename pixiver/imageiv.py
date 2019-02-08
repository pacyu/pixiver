import re
import requests
from requests.compat import (
    quote_plus, unquote_plus
)
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

        if self.info_json['error']:
            raise exceptions.AjaxRequestError(
                self.info_json['message']
            )

        if self.info_json['body']:
            self.im_tag_url = self.info_json['body']['thumbnail']
            self.im_name = self.im_tag_url.split('/')[-1]
            self.illust_id = self.im_name.split('.')[0]\
                .replace('_p0_master1200', '')\
                .replace('_p0', '')
        else:
            self.info_json['body'] = {
                'tag': unquote_plus(tag),
                'abstract': None,
                'thumbnail': None
            }

    def tag_info(self):
        return self.info_json['body']

    def view_tag(self):
        return self.info_json['body']['tag']
    
    def view_abstract(self):
        return self.info_json['body']['abstract']

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


class ImageDiscuss(baseiv.BaseQueue, baseiv.ConfigHeaders):

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

        if self.info_json['error']:
            raise exceptions.AjaxRequestError(
                self.info_json['message']
            )
        elif not self.info_json['body']:
            self.info_json['body'] = {'comments': None}

        self.que_tar = self.info_json['body']['comments']


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

    def view_tags(self):
        if self.base_tags_que is None:
            tags_que = self.info['tags']['tags']
            self.base_tags_que = baseiv.BaseQueue([
                ImageTag(quote_plus(tag['tag'])) for tag in tags_que])
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

    def user_id(self):
        return self.info['userId']

    def view_count(self):
        return self.info['viewCount']

    def view_comments(self):
        if not self.user_comments:
            self.user_comments = ImageDiscuss(
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

    def __init__(self, **kwargs):
        super().__init__()
        self.que_tar = [
            {
                'illust_attrs': zip_[0],
                'rank_date': zip_[1],
                'rank': zip_[2],
                'yes_rank': zip_[3]
            } for zip_ in zip(
                kwargs['illust_attr'],
                kwargs['rank_date'],
                kwargs['rank'],
                kwargs['yes_rank']
            )
        ]


class Daily(baseiv.ConfigHeaders, baseiv.PixivInitSay, baseiv.BaseQueue):
    name = 'daily'
    init_url = 'https://www.pixiv.net/ranking.php'
    rank_total = 0
    one_count = 0
    current_page = 1
    current_date = None

    def __init__(self, daily=None):
        super().__init__()
        self.params = {
            'mode': self.name,
            'date': '',
            'p': '',
            'format': 'json'
        }
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

            self.params.update({
                'date': date,
                'p': self.current_page
            })
            self.current_date = date
            self.__run__(params=self.params)

    def __run__(self, params):
        print(self.init_run)

        headers = {'User-Agent': self.user_agent}
        r = requests.get(self.init_url, params=params,
                         headers=headers, timeout=5)

        self.daily_json = r.json()

        if self.rank_total == 0:
            self.rank_total = self.daily_json['rank_total']
        self.current_page = self.daily_json['page']
        self.current_date = self.daily_json['date']

        print(self.init_finished)

        self.init_run = 'Current batch_size: {}, rank total: {}\n' \
                        'Loading date: {}, page: {} ...' \
            .format(
                len(self.que_tar), self.rank_total,
                params['date'], params['p']
            )
        self.init_finished = 'Load finished!'

    def run(self, daily=None):
        if daily:
            self.__init__(daily)
        else:
            self.__run__(self.params)
        return self

    def one(self):
        if self.one_count < 50:
            curr_one = {
                'illust_attrs': PixivImage(
                    self.daily_json['contents'][self.one_count]['illust_id']
                ),
                'rank_date': self.daily_json['date'],
                'rank': self.daily_json['contents'][self.one_count]['rank'],
                'yes_rank': self.daily_json['contents'][self.one_count]['yes_rank']
            }
            self.one_count += 1
            self.que_tar.append(curr_one)
            return self.last()
        else:
            return self.next_page().one()

    def batch(self):

        if self.one_count < 50:
            list1, list2, list3, list4 = [], [], [], []
            while self.one_count < 50:

                take = self.daily_json['contents'][self.one_count]

                list1.append(PixivImage(take['illust_id']))
                list2.append(self.daily_json['date'])
                list3.append(take['rank'])
                list4.append(take['yes_rank'])

                self.one_count += 1

            curr_batch = DailyImages(
                illust_attr=list1,
                rank_date=list2,
                rank=list3,
                yes_rank=list4
            )
            self.que_tar += curr_batch.que_tar
            return self.curr()
        else:
            return self.next_page().batch()

    def prev_date(self):
        if self.daily_json['prev_date']:
            self.rank_total = 0
            self.step_number = 0
            self.one_count = 0
            self.que_tar.clear()
            self.params = {
                'date': self.daily_json['prev_date']
            }
            return self.run()

    def next_date(self):
        if self.daily_json['next_date']:
            self.rank_total = 0
            self.step_number = 0
            self.one_count = 0
            self.que_tar.clear()
            self.params.update({
                'date': self.daily_json['next_date']
            })
            return self.run()

    def prev_page(self):
        if self.daily_json['prev']:
            self.one_count = 0
            self.params.update({
                'p': self.daily_json['prev']
            })
            return self.run()

    def next_page(self):
        if self.daily_json['next']:
            self.one_count = 0
            self.params.update({
                'p': self.daily_json['next']
            })
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
    name = 'weekly'


class Mouthly(Daily):
    name = 'monthly'


class Rookie(Daily):
    name = 'rookie'


class Original(Daily):
    name = 'original'


class Male(Daily):
    name = 'male'


class Female(Daily):
    name = 'female'


class DailyR(Daily):
    name = 'daily_r18'


class WeeklyR(Daily):
    name = 'weekly_r18'


class MaleR(Daily):
    name = 'male_r18'


class FemaleR(Daily):
    name = 'female_r18'
