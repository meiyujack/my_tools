# @Author  : meiyujack
# @Version : v0.31
# @Time    : 2021/8/26 16:12
import ctypes
import time
import os
import datetime
import ctypes
import hashlib
import random

from PIL import Image


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


def loop_function(function, time_args, duration=None, is_right_now=False, *arg):
    """
    定时循环函数
    :param function: 函数名
    :param arg: 函数参数
    :param time_args: 元组，传递三个int值，24小时制(开始时间,结束时间,间隔时间,分钟时间)
    :param duration: 持续时间，天为单位。即终止时间，达到后退出函数，缺省永远
    :param is_right_now: 是否即刻运行
    :return:
    """
    time_lists = ['0' + str(x) + ':' + time_args[3] + ':00' for x in range(time_args[0], time_args[1], time_args[2]) if
                  x < 10]
    time_lists.extend(
        [str(x) + ':' + time_args[3] + ':00' for x in range(time_args[0], time_args[1], time_args[2]) if x >= 10])
    # print(time_lists)
    if is_right_now:
        function(*arg)
    while True:
        if time.strftime("%H:%M:%S") in time_lists:
            function(*arg)
        if duration:
            if get_now_time("now") == (datetime.datetime.now() + datetime.timedelta(days=duration)).strftime(
                    "%Y-%m-%d %H:%M:%S"):
                break


def walk_file(path):
    """得到路径下所有文件访问地址
    :param path: 访问路径
    :return: 列表形式，包含所有文件的访问地址
    """
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            result.append(os.path.join(root, file))
    return result


def open_file_as_txt(path, encoding='utf-8'):
    """
    读取文本文件，不做任何操作
    :param path: 文本文件路径
    :param encoding:  默认万国码
    :return: 列表
    """
    with open(path, encoding=encoding) as f:
        result = f.read()
        return result


def save_image_as_png(image_name, image_content):
    """
    存图片文件，不做任何操作
    :param image_name: 文件名，可包括路径
    :param image_content: 文件内容 ，二进制
    """
    with open(image_name, 'wb') as f:
        f.write(image_content)


def get_available_space(driver_letter):
    """
    获取磁盘剩余空间
    :param driver_letter: 磁盘盘符
    :return: 剩余空间，单位G
    """
    target_driver = driver_letter + ":"
    if os.path.exists(target_driver):
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(target_driver), None, None,
                                                   ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024


def handle_verified_image(original_image):
    image = Image.open(original_image)
    image = image.convert('L')  # 灰度处理
    threshold = 127
    table = []
    for i in range(256):  # 二值化处理
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    return image


def get_md5(value):
    """
    得到字符串的md5
    """
    md5 = hashlib.md5(value.encode('utf-8'))
    return md5.hexdigest()


def get_random_number():
    """
    得到随机十个数字
    :return: 返回字符串
    """
    return str(random.random())[2:12]