from selenium import webdriver
from contextlib import contextmanager
import pandas as pd

@contextmanager
def init_webdriver():
    """
    初始化 webdriver 对象
    Parameters
    --------
        None

    Return
    --------
        WebDriver，firefox的 WebDriver 实例
    """
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-proxxy-server')
    try:
        driver = webdriver.Firefox(firefox_options=firefox_options)
        yield driver
    finally:
        driver.close()

def get_sw2_info(driver):
    """
    申万二级行业信息
    Parameters
    --------
        driver:获取网页用的WebDriver对象
    
    Return
    --------
        DataFrame，sw2行业信息列表：
        sw2_code: sw2行业代码
        sw2_name: sw2行业名称
        sw1_name: 所属一级行业名称
    """
    return pd.DataFrame()

def get_sw2_classify(sw2_info):
    """
    股票申万二级行业分类
    Parameters
    --------
        sw2_info:  DataFrame，申万二级行业信息，来自get_sw2_info函数的返回结果：
            sw2_code: sw2行业代码
            sw2_name: sw2行业名称
            sw1_name: 所属一级行业名称
    
    Return
    --------
        DataFrame，股票sw2行业分类列表：
        code: 股票代码
        name: 股票名称
        sw2_code: sw2行业代码
        sw2_name: sw2行业名称
        sw1_name: 所属一级行业名称
    """
    return pd.DataFrame()

def save_sw2_info(sw2_info):
    """
    保存sw2行业信息到csv文件
    Parameters
    --------
        sw2_info: DataFrame，申万二级行业信息，来自get_sw2_info函数的返回结果：
            sw2_code: sw2行业代码
            sw2_name: sw2行业名称
            sw1_name: 所属一级行业名称
    """
    pass

def save_sw2_classify(sw2_classify):
    """
    保存股票sw2行业分类到csv文件
    Parameters
    --------
        sw2_classify: DataFrame，股票申万二级行业分类列表，来自get_sw2_classify函数的返回结果：
            code: 股票代码
            name: 股票名称
            sw2_code: sw2行业代码
            sw2_name: sw2行业名称
            sw1_name: 所属一级行业名称
    """
    pass

def main():
    with init_webdriver() as driver:
        sw2_info = get_sw2_info(driver)
    sw2_classify = get_sw2_classify(sw2_info)

    save_sw2_info(sw2_info)
    save_sw2_classify(sw2_classify)