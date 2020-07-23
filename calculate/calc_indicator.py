import re
import os
import sys

base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.dirname(base_path)
sys.path.append(base_path)

import config
from dal import RedisAccessor
import logging

da_class = RedisAccessor

def init_logger():
    logger = logging.getLogger('CalcIndicator')
    try:
        log_level = config.LOG_LEVEL
    except:
        log_level = logging.DEBUG

    try:
        fh = logging.FileHandler(config.LOG_FILE, mode='a', encoding='utf-8', delay=False)
    except:
        fh = logging.StreamHandler(sys.stdout)

    fh.setLevel(log_level)
    fm = logging.Formatter('%(asctime)s %(filename)s %(lineno)d %(levelname)s:%(message)s')
    fh.setFormatter(fm)

    logger.addHandler(fh)
    logger.setLevel(log_level)
    return logger

logger = init_logger()

def make_quarter(quarter):
    quarter = quarter.replace('-', '')
    if re.match(r'(19|20)\d{2}(0331|0630|0930|1231)', quarter) is None:
        raise ValueError(f'quarter format error, expected: YYYYMMDD, got: {quarter}')
    return quarter

def make_last_quarter(quarter):
    quarter = make_quarter(quarter)
    year = quarter[:4]
    last_year = str(int(year) - 1)
    last_month_day = quarter[4:]
    return last_year + last_month_day

def calc_moneyincomeratio(da, stockid, quarters):
    logger.info(f'calculating moneyincomeratio, stockid: {stockid}, quarters: {quarters}')
    if da.exists_in_calc_processed_set(stockid, 'moneyincomeratio'):
        logger.debug(f'moneyincomeratio of stockid {stockid} already calculated, skip it.')
        return
    moneyincomeratio = {}
    for quarter in quarters:
        quarter = make_quarter(quarter)
        laborgetcash = da.get_laborgetcash(stockid, quarter)
        bizinco = da.get_bizinco(stockid, quarter)
        if laborgetcash is not None and bizinco:
             moneyincomeratio[quarter] = laborgetcash / bizinco * 100
        else:
            logger.warning(f'failed calculate, quarter: {quarter}, '
                           f'laborgetcash: {laborgetcash}, bizinco: {bizinco}')
    if moneyincomeratio:
        if da.mset_moneyincomeratio(stockid, moneyincomeratio):
            da.add_to_calc_processed_set(stockid, 'moneyincomeratio')

def calc_incomegrowthratio(da, stockid, quarters):
    logger.info(f'calculating incomegrowthratio, stockid: {stockid}, quarters: {quarters}')
    if da.exists_in_calc_processed_set(stockid, 'incomegrowthratio'):
        logger.debug(f'incomegrowthratio of stockid {stockid} already calculated, skip it.')
        return
    incomegrowthratio = {}
    for quarter in quarters:
        quarter = make_quarter(quarter)
        last_quarter = make_last_quarter(quarter)
        bizinco = da.get_bizinco(stockid, quarter)
        last_bizinco = da.get_bizinco(stockid, last_quarter)
        if bizinco is not None and last_bizinco:
             incomegrowthratio[quarter] = (bizinco - last_bizinco) / last_bizinco * 100
        else:
            logger.warning(f'failed calculate, quarter: {quarter}, '
                           f'bizinco: {bizinco}, last_quarter: {last_quarter}, '
                           f'last_bizinco: {last_bizinco}')
    if incomegrowthratio:
        if da.mset_incomegrowthratio(stockid, incomegrowthratio):
            da.add_to_calc_processed_set(stockid, 'incomegrowthratio')

def calc_goodwillequityratio(da, stockid, quarters):
    logger.info(f'calculating goodwillequityratio, stockid: {stockid}, quarters: {quarters}')
    if da.exists_in_calc_processed_set(stockid, 'goodwillequityratio'):
        logger.debug(f'goodwillequityratio of stockid {stockid} already calculated, skip it.')
        return
    goodwillequityratio = {}
    for quarter in quarters:
        quarter = make_quarter(quarter)
        goodwill = da.get_goodwill(stockid, quarter)
        equity = da.get_equity(stockid, quarter)
        # 增加商誉为0的处理，如贵州茅台没有并购，所以商誉为0
        if not goodwill:
            goodwill = 0 
        if goodwill is not None and equity:
             goodwillequityratio[quarter] = goodwill / equity * 100
        else:
            logger.warning(f'failed calculate, quarter: {quarter}, '
                           f'goodwill: {goodwill}, equity: {equity}')
    if goodwillequityratio:
        if da.mset_goodwillequityratio(stockid, goodwillequityratio):
            da.add_to_calc_processed_set(stockid, 'goodwillequityratio')

def calc_indicators(da, stockid, quarters):
    calc_moneyincomeratio(da, stockid, quarters)
    calc_incomegrowthratio(da, stockid, quarters)
    calc_goodwillequityratio(da, stockid, quarters)

if __name__ == '__main__':
    da = da_class(logger=logger)
    quarters = config.QUARTERS
    with open(config.STOCK_LIST_FILE, 'rt', encoding='utf-8') as f:
        f.readline()
        for line in f:
            columns = line.split(',')
            stockid = columns[2]
            calc_indicators(da, stockid, quarters)