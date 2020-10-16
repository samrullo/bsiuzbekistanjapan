import datetime


def to_yyyymmdd(adate: datetime.date):
    return datetime.date.strftime(adate, '%Y%m%d')
