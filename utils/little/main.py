import uuid,random

from . import hashlib, random, json
from . import Image

from ..generate_str_time.main import get_now_time, datetime, time


def loop_function(function,
                  time_args,
                  duration=None,
                  is_right_now=False,
                  *arg):
    """
    定时循环函数
    :param function: 函数名
    :param arg: 函数参数
    :param time_args: 元组，传递三个int值，24小时制(开始时间,结束时间,间隔时间,分钟时间)
    :param duration: 持续时间，天为单位。即终止时间，达到后退出函数，缺省永远
    :param is_right_now: 是否即刻运行
    :return:
    """
    time_lists = [
        '0' + str(x) + ':' + time_args[3] + ':00'
        for x in range(time_args[0], time_args[1], time_args[2]) if x < 10
    ]
    time_lists.extend([
        str(x) + ':' + time_args[3] + ':00'
        for x in range(time_args[0], time_args[1], time_args[2]) if x >= 10
    ])
    # print(time_lists)
    if is_right_now:
        function(*arg)
    while True:
        if time.strftime("%H:%M:%S") in time_lists:
            function(*arg)
        if duration:
            if get_now_time("now") == (datetime.datetime.now() +
                                       datetime.timedelta(days=duration)
                                       ).strftime("%Y-%m-%d %H:%M:%S"):
                break


def save_wb_as_file(file_name, file_content):
    """
    存二进制数据为文件，不做任何操作
    :param file_name: 文件名，可包括路径
    :param file_content: 文件内容 ，二进制
    """
    with open(file_name, 'wb') as f:
        f.write(file_content)


def handle_verified_image(original_image):
    """对图片做黑白处理"""
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


def open_file_as_txt(path, encoding='utf-8'):
    """
    读取文本文件，不做任何操作
    :param path: 文本文件路径
    :param encoding:  默认万国码
    :return: str
    """
    with open(path, encoding=encoding) as f:
        result = f.read()
        return result


def get_md5(value):
    """得到字符串的md5"""
    md5 = hashlib.md5(value.encode('utf-8'))
    return md5.hexdigest()


def get_random_number():
    """
    得到随机十个数字
    :return: 返回字符串
    """
    return str(random.random())[2:12]


def read_json_file(path):
    """直接读取json文件"""
    return json.loads(open_file_as_txt(path))


def slice_reverse(l, i):
    """
    对列表的子列表进行倒序排列
    :return: 列表，返回结果
    """

    t = l[i:]
    t.reverse()
    for n in range(len(l)):
        if n >= i:
            l[n] = t[n - i]
    return l

def generate_unique(num:int):
    answer=''
    uid=str(uuid.uuid4())
    while len(answer)!=num:
        r=random.choice(uid)
        if r.isdigit()==True and r!='0':
            answer+=r
    return answer
