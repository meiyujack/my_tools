# @Author  : meiyujack
# @Version : v0.01
# @Time    : 2021/8/5 9:48

import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import IeOptions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException


def start_chrome(headless=False):
    chrome_options = ChromeOptions()
    if headless is True:
        chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  # 去沙盒
    # chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-error")
    chrome_options.add_argument("--ignore-net-error")
    chrome_options.add_argument('--log-level=1')
    chrome = webdriver.Chrome(options=chrome_options)
    return chrome


def start_ie():
    ie_options = IeOptions()
    ie_options.ignore_zoom_level=True
    ie_options.ignore_protected_mode_settings=True
    ie=webdriver.Ie(options=ie_options)
    return ie
