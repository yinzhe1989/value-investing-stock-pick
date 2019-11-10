import os
import sys

base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.dirname(base_path)
sys.path.append(base_path)

import logging
from dal import RedisAccessor
import config
from datetime import date

class IndicatorFilter(object):
    da_class = RedisAccessor

    def __init__(self):
        self.pass_if_not_exists = config.PASS_IF_NOT_EXISTS
        self.logger = self.init_logger()
        self.da = self.da_class(logger=self.logger)
        self.last_eight_quarter = self.make_last_eight_quarter()
        self.last_five_year = self.make_last_five_year()
        self.logger.info(f'last eight quarters: {self.last_eight_quarter}')
        self.logger.info(f'last five years: {self.last_five_year}')
        # open file for save results
        try:
            self.satisfied_stocks_writer = open(
                '../tmp/satisfied_stocks.csv', 'wt', encoding='utf-8')
            self.satisfied_stocks_writer.write(',symbol,name\n')
        except:
            raise
        try:
            self.filte_result_writer = open(
                '../tmp/filte_result.csv', 'wt', encoding='utf-8')
            self.filte_result_writer.write(
                f'{"":<4},{"symbol":<8},{"name":\u3000<8},'
                f'{"moneyincomeratio":<22},'
                f'{"roe":<22},'
                f'{"assetsturnratio":<22},'
                f'{"incomegrowthratio":<22},'
                f'{"goodwillequityratio":<22},'
                f'{"grossprofitmarginratio":<22}'
                '\n')
        except:
            raise
        self.satisfied_stocks_count = 0
        self.filte_result_count = 0


    def init_logger(self):
        logger = logging.getLogger('IndicatorFilter')
        try:
            log_level = config.LOG_LEVEL
        except:
            log_level = logging.DEBUG

        try:
            fh = logging.FileHandler(
                config.LOG_FILE, mode='a', encoding='utf-8', delay=False)
        except:
            fh = logging.StreamHandler(sys.stdout)

        fh.setLevel(log_level)
        fm = logging.Formatter(
            '%(asctime)s %(filename)s %(lineno)d %(levelname)s:%(message)s')
        fh.setFormatter(fm)

        logger.addHandler(fh)
        logger.setLevel(log_level)
        return logger

    def make_previous_quarter(self, this_quarter):
        previous_quarter = ''
        if this_quarter[4:6] == '03':
            previous_quarter = f'{int(this_quarter[:4])-1}1231'
        elif this_quarter[4:6] == '06':
            previous_quarter = f'{int(this_quarter[:4])}0331'
        elif this_quarter[4:6] == '09':
            previous_quarter = f'{int(this_quarter[:4])}0630'
        elif this_quarter[4:6] == '12':
            previous_quarter = f'{int(this_quarter[:4])}0930'
        assert previous_quarter
        return previous_quarter

    def make_last_eight_quarter(self):
        today = date.today()
        # 季报一般在季度结束后一个月内披露，
        # 因此今日为上个季度结束的第二个月时才考虑上个季度
        last_eight_quarter = []
        if today.month < 2:
            last_eight_quarter.append(f'{today.year-1}0930')
        elif today.month < 5:
            last_eight_quarter.append(f'{today.year-1}1231')
        elif today.month < 8:
            last_eight_quarter.append(f'{today.year}0331')
        elif today.month < 11:
            last_eight_quarter.append(f'{today.year}0630')
        else:
            last_eight_quarter.append(f'{today.year}0930')
        for i in range(7):
            last_eight_quarter.append(
                self.make_previous_quarter(last_eight_quarter[i]))
        # return reversed(last_eight_quarter)
        last_eight_quarter.reverse()
        return last_eight_quarter

    def make_last_five_year(self):
        today = date.today()
        return [f'{today.year+i}1231' for i in range(-5, 0)]

    def filte_by_moneyincomeratio(self, stockid):
        self.logger.debug(f'begin to filte stock {stockid} by moneyincomeratio,'
                          f' pass condition: moneyincomeratio>={config.MONEYINCOMERATIO_CONDITION_GATE}...')
        all_satisfied = True
        total = 0
        for quarter in self.last_five_year:
            moneyincomeratio = self.da.get_moneyincomeratio(stockid, quarter)
            self.logger.debug(
                f'moneyincomeratio: {moneyincomeratio}, quarter: {quarter}')
            if moneyincomeratio is None:
                if self.pass_if_not_exists:
                    continue
                else:
                    all_satisfied = False
            else:
                total += moneyincomeratio
                if moneyincomeratio < config.MONEYINCOMERATIO_CONDITION_GATE:
                    all_satisfied = False
        
        return all_satisfied, total / len(self.last_five_year)

    def filte_by_roe(self, stockid):
        self.logger.debug(f'begin to filte stock {stockid} by roe,'
                          f' pass condition: roe>{config.ROE_CONDITION_GATE}...')
        all_satisfied = True
        total = 0
        for quarter in self.last_five_year:
            roe = self.da.get_roe(stockid, quarter)
            self.logger.debug(f'roe: {roe}, quarter: {quarter}')
            if roe is None:
                if self.pass_if_not_exists:
                    continue
                else:
                    all_satisfied = False
            else:
                total += roe
                if roe <= config.ROE_CONDITION_GATE:
                    all_satisfied = False
        return all_satisfied, total / len(self.last_five_year)

    def filte_by_assetsturnratio(self, stockid):
        self.logger.debug(f'begin to filte stock {stockid} by assetsturnratio,'
                          f' pass condition: assetsturnratio>={config.ASSETSTURNRATIO_CONDITION_GATE}...')
        all_satisfied = True
        total = 0
        for quarter in self.last_five_year:
            assetsturnratio = self.da.get_assetsturnratio(stockid, quarter)
            self.logger.debug(
                f'assetsturnratio: {assetsturnratio}, quarter: {quarter}')
            if assetsturnratio is None:
                if self.pass_if_not_exists:
                    continue
                else:
                    all_satisfied = False
            else:
                total += assetsturnratio
                if assetsturnratio < config.ASSETSTURNRATIO_CONDITION_GATE:
                    all_satisfied = False
        return all_satisfied, total / len(self.last_five_year)

    def filte_by_incomegrowthratio(self, stockid):
        self.logger.debug(f'begin to filte stock {stockid} by incomegrowthratio,'
                          f' pass condition: incomegrowthratio>{config.INCOMEGROWTHRATIO_CONDITION_GATE}...')
        all_satisfied = True
        total = 0
        for quarter in self.last_eight_quarter:
            incomegrowthratio = self.da.get_incomegrowthratio(stockid, quarter)
            self.logger.debug(f'incomegrowthratio: {incomegrowthratio}, quarter: {quarter}')
            if incomegrowthratio is None:
                if self.pass_if_not_exists:
                    continue
                else:
                    all_satisfied = False
            else:
                total += incomegrowthratio
                if incomegrowthratio <= config.INCOMEGROWTHRATIO_CONDITION_GATE:
                    all_satisfied = False
        return all_satisfied, total / len(self.last_five_year)

    def filte_by_goodwillequityratio(self, stockid):
        self.logger.debug(f'begin to filte stock {stockid} by goodwillequityratio,'
                          f' pass condition: goodwillequityratio<={config.GOODWILLEQUITYRATIO_CONDITION_GATE}...')
        all_satisfied = True
        total = 0
        for quarter in self.last_five_year:
            goodwillequityratio = self.da.get_goodwillequityratio(stockid, quarter)
            self.logger.debug(f'goodwillequityratio: {goodwillequityratio}, quarter: {quarter}')
            if goodwillequityratio is None:
                if self.pass_if_not_exists:
                    continue
                else:
                    all_satisfied = False
            else:
                total += goodwillequityratio
                if goodwillequityratio > config.GOODWILLEQUITYRATIO_CONDITION_GATE:
                    all_satisfied = False
        return all_satisfied, total / len(self.last_five_year)

    def filte_by_grossprofitmarginratio(self, stockid):
        self.logger.debug(f'begin to filte stock {stockid} by grossprofitmarginratio,'
                          f' pass condition: grossprofitmarginratio>{config.GROSSPROFITMARGINRATIO_CONDITION_GATE}...')
        all_satisfied = True
        total = 0
        for quarter in self.last_five_year:
            grossprofitmarginratio = self.da.get_grossprofitmarginratio(stockid, quarter)
            self.logger.debug(f'grossprofitmarginratio: {grossprofitmarginratio}, quarter: {quarter}')
            if grossprofitmarginratio is None:
                if self.pass_if_not_exists:
                    continue
                else:
                    all_satisfied = False
            else:
                total += grossprofitmarginratio
                if grossprofitmarginratio <= config.GROSSPROFITMARGINRATIO_CONDITION_GATE:
                    all_satisfied = False
        return all_satisfied, total / len(self.last_five_year)

    def filte(self, stockid):
        self.logger.info(f'begin to filte stock {stockid}...')
        # flite_result: {指标: (是否满足过滤条件, 指标均值)}
        filte_result = {}
        # (all_satisfied, mean) = self.filte_by_moneyincomeratio(stockid)
        filte_result['moneyincomeratio'] = self.filte_by_moneyincomeratio(stockid)
        # (all_satisfied, mean) = self.filte_by_roe(stockid)
        filte_result['roe'] = self.filte_by_roe(stockid)
        # (all_satisfied, mean) = self.filte_by_assetsturnratio(stockid)
        filte_result['assetsturnratio'] = self.filte_by_assetsturnratio(stockid)
        # (all_satisfied, mean) = self.filte_by_incomegrowthratio(stockid)
        filte_result['incomegrowthratio'] = self.filte_by_incomegrowthratio(stockid)
        # (all_satisfied, mean) = self.filte_by_goodwillequityratio(stockid)
        filte_result['goodwillequityratio'] = self.filte_by_goodwillequityratio(stockid)
        # (all_satisfied, mean) = self.filte_by_grossprofitmarginratio(stockid)
        filte_result['grossprofitmarginratio'] = self.filte_by_grossprofitmarginratio(stockid)
        
        # return: (所有指标是否满足过滤条件, {指标: (是否满足过滤条件, 指标均值)})
        indicator_result = [v[0] for k,v in filte_result.items()]
        return True if indicator_result.count(True) >= config.PASS_INDICATOR_COUNT else False, filte_result

    def save(self, stockid, line, flite_result):
        """
        Save satisfied stocks to file or database...
        `flite_result`: (所有指标是否满足过滤条件, {指标: (是否满足过滤条件, 指标均值)})
        """
        columns = line.split(',')
        stockname = columns[3]
        # 总市值大于2000000万， 流通市值大于1000000万
        if columns[10] and columns[11] \
            and float(columns[10]) > 2000000 \
            and float(columns[11]) > 1000000 \
                and flite_result[0]:
        #if flite_result[0]:
            self.satisfied_stocks_count += 1
            self.satisfied_stocks_writer.write(
                f'{self.satisfied_stocks_count},{line}\n')
        # ',symbol,name,'
        # 'moneyincomeratio_satisfied,moneyincomeratio_mean,'
        # 'roe_satisfied,roe_mean,'
        # 'assetsturnratio_satisfied,assetsturnratio_mean,'
        # 'incomegrowthratio_satisfied,incomegrowthratio_mean,'
        # 'goodwillequityratio_satisfied,goodwillequityratio_mean,'
        # 'grossprofitmarginratio_satisfied,grossprofitmarginratio_mean,'
        self.filte_result_count += 1
        self.filte_result_writer.write(
            f'{self.filte_result_count:<4},{stockid:<8},{stockname:\u3000<8},'
            f'{flite_result[1].get("moneyincomeratio")[0]:<5}{flite_result[1].get("moneyincomeratio")[1]:<17.2f},'
            f'{flite_result[1].get("roe")[0]:<5}{flite_result[1].get("roe")[1]:<17.2f},'
            f'{flite_result[1].get("assetsturnratio")[0]:<5}{flite_result[1].get("assetsturnratio")[1]:<17.2f},'
            f'{flite_result[1].get("incomegrowthratio")[0]:<5}{flite_result[1].get("incomegrowthratio")[1]:<17.2f},'
            f'{flite_result[1].get("goodwillequityratio")[0]:<5}{flite_result[1].get("goodwillequityratio")[1]:<17.2f},'
            f'{flite_result[1].get("grossprofitmarginratio")[0]:<5}{flite_result[1].get("grossprofitmarginratio")[1]:<17.2f}'
            '\n'
        )

    def close(self):
        self.filte_result_writer.close()
        self.satisfied_stocks_writer.close()


if __name__ == '__main__':
    indicator_filter = IndicatorFilter()
    with open(config.STOCK_LIST_FILE, 'rt', encoding='utf-8') as f:
        f.readline()
        for line in f:
            columns = line.split(',')
            stockid = columns[2]
            # flite_result: (所有指标是否满足过滤条件, {指标: (是否满足过滤条件, 指标均值)})
            flite_result = indicator_filter.filte(stockid)
            indicator_filter.save(stockid, line, flite_result)
            
    indicator_filter.close()
