import re
from . import basiciv
from .helper import check_date
from . import worksiv


class Batch(basiciv.Queue):

    def __init__(self, **kwargs):
        super().__init__()
        self.que_tar = [
            {
                'illust_attrs': zip_[0],
                'rank': zip_[1],
                'yes_rank': zip_[2]
            } for zip_ in zip(
                kwargs['illust_attrs'],
                kwargs['rank'],
                kwargs['yes_rank']
            )
        ]


class Daily(basiciv.BasicConfig, basiciv.LoadInfo, basiciv.Queue):
    name = 'daily'
    rank_url = 'https://www.pixiv.net/ranking.php'
    rank_total = 0
    one_count = 0
    current_page = None
    current_date = None

    def __init__(self, ymd=None, filters='complex', **kwargs):
        """
        :param ymd:
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
        super(Daily, self).__init__(
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

        if ymd:
            reg = re.compile(
                r'[0-9]{4}[^a-zA-Z0-9]?[0-9]{2}[^a-zA-Z0-9]?[0-9]{2}'
            )
            s = reg.fullmatch(str(ymd))
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
            timeout=self.kvpair['timeout']
        )

        print(r.text)

        self.interface = r.json()

        if self.rank_total == 0:
            self.rank_total = self.interface['rank_total']
        self.current_page = self.interface['page']
        self.current_date = self.interface['date']

        print(self.init_finished)

        self.init_run = 'Current batch_size: {}, rank total: {}\n' \
                        'Loading date: {}, page: {} ...' \
            .format(
                len(self.que_tar), self.rank_total,
                params['date'], params['p']
            )
        self.init_finished = 'Load finished!'

    def run(self, ymd=None):
        if ymd:
            self.__init__(ymd=ymd)
        return self

    def one(self):
        if self.one_count < 50:
            curr_one = {
                'illust_attrs': worksiv.Works(
                    self.interface['contents'][self.one_count]['illust_id']
                ),
                'rank': self.interface['contents'][self.one_count]['rank'],
                'yes_rank': self.interface['contents'][self.one_count]['yes_rank']
            }
            self.one_count += 1
            self.que_tar.append(curr_one)
            return self.last()
        else:
            return self.next_page().one()

    def batch(self, nums=-1):
        if self.one_count < 50:
            list1, list2, list3 = [], [], []
            if nums == -1:
                while self.one_count < 50:
                    take = self.interface['contents'][self.one_count]

                    list1.append(worksiv.Works(take['illust_id']))
                    list2.append(take['rank'])
                    list3.append(take['yes_rank'])

                    self.one_count += 1
            else:
                for _ in range(nums):
                    if self.one_count == 50:
                        break
                    take = self.interface['contents'][self.one_count]

                    list1.append(worksiv.Works(take['illust_id']))
                    list2.append(take['rank'])
                    list3.append(take['yes_rank'])

                    self.one_count += 1

            curr_batch = Batch(
                illust_attrs=list1,
                rank=list2,
                yes_rank=list3
            )
            self.que_tar += curr_batch.que_tar
            return self.curr()
        else:
            return self.next_page().batch(nums)

    def prev_date(self):
        if self.interface['prev_date']:
            self.rank_total = 0
            self.step_number = 0
            self.one_count = 0
            self.que_tar.clear()
            self.params = {
                'date': self.interface['prev_date']
            }
            return self.run()

    def next_date(self):
        if self.interface['next_date']:
            self.rank_total = 0
            self.step_number = 0
            self.one_count = 0
            self.que_tar.clear()
            self.params.update({
                'date': self.interface['next_date']
            })
            return self.run()

    def prev_page(self):
        if self.interface['prev']:
            self.one_count = 0
            self.params.update({
                'p': self.interface['prev']
            })
            return self.run()

    def next_page(self):
        if self.interface['next']:
            self.one_count = 0
            self.params.update({
                'p': self.interface['next']
            })
            return self.run()


class Weekly(Daily):
    name = 'weekly'


class Monthly(Daily):
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

    def __init__(self, ymd=None, filters='complex', **kwargs):
        super(DailyR, self).__init__(
            ymd=ymd,
            filters=filters,
            **kwargs
        )


class WeeklyR(DailyR):
    name = 'weekly_r18'


class MaleR(DailyR):
    name = 'male_r18'


class FemaleR(DailyR):
    name = 'female_r18'
