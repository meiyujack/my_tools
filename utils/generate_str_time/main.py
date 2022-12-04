from . import time, datetime


def get_now_time(condition):
    """得到本地时间。分日期、时间和全格式三种"""
    if condition == 'date':
        return time.strftime("%Y-%m-%d")
    if condition == 'time':
        return time.strftime("%H:%M:%S")
    if condition == 'now':
        return time.strftime("%Y-%m-%d %H:%M:%S")


def transform_int_time(int_time):
    """把秒针形式的时间转换成标准日期格式"""
    return datetime.datetime.strptime(time.ctime(int_time), '%a %b  %d %H:%M:%S %Y').isoformat().replace('T', ' ')
