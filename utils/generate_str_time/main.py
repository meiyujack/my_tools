from . import time, datetime


def get_now_time(condition):
    """得到本地时间。分日期、时间和全格式三种"""
    if condition == 'date':
        return time.strftime("%Y-%m-%d")
    if condition == 'time':
        return time.strftime("%H:%M:%S")
    if condition == 'now':
        return time.strftime("%Y-%m-%d %H:%M:%S")


def get_certain_time(days):
    return (datetime.datetime.now() +
            datetime.timedelta(days=days)).strftime('%Y-%m-%d')


def transform_int_time(int_time):
    """把秒针形式的时间转换成字符串（标准日期格式）"""
    return datetime.datetime.strptime(
        time.ctime(int_time),
        '%a %b  %d %H:%M:%S %Y').isoformat().replace('T', ' ')


def transform_str_time(str_time):
    """把字符串（标准日期格式）的时间转换成秒针形式"""
    return int(datetime.datetime.strptime(str_time, '%Y-%m-%d').timestamp())
