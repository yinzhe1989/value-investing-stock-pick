# -*- coding: utf-8 -*-
import logging
import os
import sys

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_PATH)

# dal uses Redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_USE_CLUSTER = False

# logging
LOG_LEVEL = logging.INFO
LOG_FILE = os.path.join(BASE_PATH, 'tmp', 'sina_stock_crawler.log')

# stocks
# 过滤选股时，指标值不存在时是否当作满足过滤条件处理
# True - 满足；False - 不满足
PASS_IF_NOT_EXISTS = True
# 满足条件的指标数大于等于此值即选取此股
PASS_INDICATOR_COUNT = 5
MONEYINCOMERATIO_CONDITION_GATE = 96 # 100
ROE_CONDITION_GATE = 15 # 15
ASSETSTURNRATIO_CONDITION_GATE = 40 # 100
INCOMEGROWTHRATIO_CONDITION_GATE = 14 # 15
GOODWILLEQUITYRATIO_CONDITION_GATE = 30
GROSSPROFITMARGINRATIO_CONDITION_GATE = 15
STOCK_LIST_FILE = os.path.join(BASE_PATH, 'tmp', 'stocks.csv')
QUARTERS = ['2013-12-31', '2014-12-31', '2015-12-31', '2016-12-31',
            '2017-03-31', '2017-06-30', '2017-09-30', '2017-12-31',
            '2018-03-31', '2018-06-30', '2018-09-30', '2018-12-31',
            '2019-03-31', '2019-06-30', '2019-09-30']