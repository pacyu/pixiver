import re
from pixiver import baseiv
from pixiver import pixiv
from pixiver.helperiv import check_date
from pixiver.imageiv import PixivImage


class RankImages(baseiv.BaseQueue):

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


class Daily(pixiv.Pixiv, baseiv.PixivInitSay, baseiv.BaseQueue):
    name = 'daily'
    rank_url = 'https://www.pixiv.net/ranking.php'
    rank_total = 0
    one_count = 0
    current_page = None
    current_date = None

    def __init__(self, daily=None, filters='complex', **kwargs):
        """
        :param daily:
            Example:
            ~~~~~~~
                20190101
                '2019-01-01'
                '2019/01/01'
                '2019.01.01'
        :param filters:
            Optional:
            ~~~~~~~~
                - complex
                - illust
                - ugoira (note: Unsupported view dynamic picture.)
                - manga
            default complex
        """
        super().__init__(
            **kwargs
        )

        self.params = {
            'mode': self.name,
            'date': '',
            'p': 1,
            'format': 'json'
        }

        if filters != 'complex':
            self.params.update({
                'content': filters,
            })

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
            })
            self.current_date = date
            self.__run__(params=self.params)

    def __run__(self, params):
        print(self.init_run)

        r = self.sess.get(
            self.rank_url,
            params=params,
            timeout=5
        )

        self.rjson = r.json()

        if self.rank_total == 0:
            self.rank_total = self.rjson['rank_total']
        self.current_page = self.rjson['page']
        self.current_date = self.rjson['date']

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
            self.__init__(daily=daily)
        else:
            self.__run__(self.params)
        return self

    def one(self):
        if self.one_count < 50:
            curr_one = {
                'illust_attrs': PixivImage(
                    self.rjson['contents'][self.one_count]['illust_id']
                ),
                'rank_date': self.rjson['date'],
                'rank': self.rjson['contents'][self.one_count]['rank'],
                'yes_rank': self.rjson['contents'][self.one_count]['yes_rank']
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

                take = self.rjson['contents'][self.one_count]

                list1.append(PixivImage(take['illust_id']))
                list2.append(self.rjson['date'])
                list3.append(take['rank'])
                list4.append(take['yes_rank'])

                self.one_count += 1

            curr_batch = RankImages(
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
        if self.rjson['prev_date']:
            self.rank_total = 0
            self.step_number = 0
            self.one_count = 0
            self.que_tar.clear()
            self.params = {
                'date': self.rjson['prev_date']
            }
            return self.run()

    def next_date(self):
        if self.rjson['next_date']:
            self.rank_total = 0
            self.step_number = 0
            self.one_count = 0
            self.que_tar.clear()
            self.params.update({
                'date': self.rjson['next_date']
            })
            return self.run()

    def prev_page(self):
        if self.rjson['prev']:
            self.one_count = 0
            self.params.update({
                'p': self.rjson['prev']
            })
            return self.run()

    def next_page(self):
        if self.rjson['next']:
            self.one_count = 0
            self.params.update({
                'p': self.rjson['next']
            })
            return self.run()


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

    def __init__(self, username=None, password=None,
                 daily=None, filters='complex', cookie=True):
        super().__init__(
            daily=daily,
            filters=filters,
            username=username,
            password=password,
            return_to=self.rank_url + '?mode=' + self.name,
            cookie=cookie
        )


class WeeklyR(DailyR):
    name = 'weekly_r18'


class MaleR(DailyR):
    name = 'male_r18'


class FemaleR(DailyR):
    name = 'female_r18'
