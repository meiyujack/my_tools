# @Author  : meiyujack
# @Version : v0.04
# @Time    : 2021/8/9 23:33

import urllib3
import urllib

import requests
from requests.exceptions import Timeout, ConnectionError
from lxml import etree

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_answer(url, request_head=None, xpath_exp=None):
    """
    得到网页的元素、源代码或图片。

    :param url: 待访问的网址。
    :param xpath_exp: xpath匹配表达式，默认为None。
    :return: element、str或bytes
    """

    headers = {"pc-chrome": {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                           'Chrome/57.0.2987.133 Safari/537.36'},
               "uc": {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 '
                                    'UCBrowser/12.11.1.1197 Mobile Safari/537.36'
                      },

               "quark": {'User-Agent': 'Mozilla/5.0 (linux; u; android 9; zh-cn; v1816a build/pkq1.180819.001) '
                                       'applewebkit/537.36 (khtml, like gecko) version/4.0 chrome/57.......'
                         },

               "pc-edge": {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.100.0'
                           }}

    while True:
        try:
            if urllib.parse.urlparse(url)[0] in ('http','https'):
                if request_head:
                    response = requests.get(url, timeout=(21, 36), headers=headers[request_head], verify=False)
                else:
                    response = requests.get(url, timeout=(21, 36), verify=False)
                if xpath_exp:
                    html = etree.HTML(response.content)
                    element = html.xpath(xpath_exp)
                    return element
                elif url.split('.')[-1] in ('jpg', 'jpeg', 'png', 'gif', 'mp3','mp4'):
                    return response.content
                else:
                    if response.encoding != 'UTF-8':
                        response.encoding = 'UTF-8'
                    return response.text
            else:
                html=etree.parse(url,etree.HTMLParser())
                element=html.xpath(xpath_exp)
                return element
        except Timeout:
            print('请求超时......正在重试')
            continue
        except ConnectionError:
            print('网络错误......正在重试')
            continue
