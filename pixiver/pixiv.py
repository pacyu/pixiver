from . import basiciv
from . import useriv
from . import worksiv
from . import rankiv


class Pixiv(basiciv.Login):

    def works(self, illust_id):
        return worksiv.Works(illust_id, headers=self.sess.headers, token=self.token, user_id=self.user_id)

    def user(self, user_id):
        return useriv.User(user_id, headers=self.sess.headers, token=self.token, user_id=self.user_id)

    def rank(self, date, typed='daily', filters='complex'):
        if typed == 'weekly':
            return rankiv.Weekly(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'Monthly':
            return rankiv.Monthly(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'male':
            return rankiv.Male(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'female':
            return rankiv.Female(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'rookie':
            return rankiv.Rookie(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'original':
            return rankiv.Original(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'daily_r18':
            return rankiv.DailyR(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'weekly_r18':
            return rankiv.WeeklyR(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'male_r18':
            return rankiv.MaleR(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        elif typed == 'female_r18':
            return rankiv.FemaleR(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
        else:
            return rankiv.Daily(
                ymd=date,
                filters=filters,
                headers=self.sess.headers,
                token=self.token,
                user_id=self.user_id
            )
