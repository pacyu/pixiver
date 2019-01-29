from datetime import datetime
from pixiver.exceptions import DateError


def check_date(year, mouth, day):
    if year < 2008 or year > datetime.now().year:
        raise DateError(
            'No day {} in February {}'.format(day, year)
        )
    if mouth == 2:
        if year % 400 == 0:
            if day > 29 or day < 1:
                raise DateError(
                    'No day {} in February {}'.format(day, year)
                )
        else:
            if day > 28 or day < 1:
                raise DateError(
                    'No day {} in February {}'.format(day, year)
                )
    elif mouth == 1:
        if day > 31 or day < 1:
            raise DateError(
                'No day {} in January {}'.format(day, year)
            )
    elif mouth == 3:
        if day > 31 or day < 1:
            raise DateError(
                'No day {} in March {}'.format(day, year)
            )
    elif mouth == 4:
        if day > 30 or day < 1:
            raise DateError(
                'No day {} in April {}'.format(day, year)
            )
    elif mouth == 5:
        if day > 31 or day < 1:
            raise DateError(
                'No day {} in May {}'.format(day, year)
            )
    elif mouth == 6:
        if day > 30 or day < 1:
            raise DateError(
                'No day {} in June {}'.format(day, year)
            )
    elif mouth == 7:
        if day > 31 or day < 1:
            raise DateError(
                'No day {} in July {}'.format(day, year)
            )
    elif mouth == 8:
        if day > 31 or day < 1:
            raise DateError(
                'No day {} in August {}'.format(day, year)
            )
    elif mouth == 9:
        if day > 30 or day < 1:
            raise DateError(
                'No day {} in September {}'.format(day, year)
            )
    elif mouth == 10:
        if day > 31 or day < 1:
            raise DateError(
                'No day {} in October {}'.format(day, year)
            )
    elif mouth == 11:
        if day > 30 or day < 1:
            raise DateError(
                'No day {} in November {}'.format(day, year)
            )
    elif mouth == 12:
        if day > 31 or day < 1:
            raise DateError(
                'No day {} in December {}'.format(day, year)
            )
    else:
        raise DateError('Mouth error')
