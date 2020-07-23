import scrapy
import urllib.parse
import urllib.request
import xml.dom.minidom

"""
import os
import sys

base_path = os.path.abspath(os.path.dirname(__file__))
for i in range(4):
    base_path = os.path.dirname(base_path)
sys.path.append(base_path)
"""

from dal import RedisAccessor

class SinaStockCollector(scrapy.Spider):
    name = 'SinaStockCollector'

    da_class = RedisAccessor

    def __init__(self):
        self._da = self.da_class(self.logger)

    def start_requests(self):
        for stockid in self._stocks():
            for typecode_url in self._generate_typecode_urls(stockid):
                typecode = typecode_url[0]
                url = typecode_url[1]
                meta = {
                    'stockid': stockid,
                    'typecode': typecode
                }
                if self._da.exists_in_crawl_processed_set(stockid, typecode):
                    self.logger.info(f'\nstockid: {stockid}, typecode: {typecode} already processed, skip it.')
                    continue
                self.logger.info(
                    f'\nstart request: <stockid: {stockid}, typecode: {typecode}, url: {url}')
                request = scrapy.Request(url, callback=self._parse, meta=meta)
                yield request

    def _request_inspremcash(self, item):
        laborgetcash_components = (
            'http',
            'money.finance.sina.com.cn',
            'corp/view/vFD_FinanceSummaryHistory.php',
            f'stockid={item.get("stockid")}&typecode=INSPREMCASH&cate=xjll3',
            None
        )
        url = urllib.parse.urlunsplit(laborgetcash_components)
        self.logger.info(f'\nstart request: <stockid: {item.get("stockid")}, '
                         f'typecode: {item.get("typecode")}->inspremcash, url: {url}')
        request = scrapy.Request(url, callback=self._parse, meta=item)
        return request

    def _parse(self, response):
        item = response.meta
        item['values'] = {}
        self.logger.debug(
            f'\nbegin parse, stock: {item.get("stockid")}, typecode: {item.get("typecode")}')
        # self.logger.debug(response.body)
        xml_data = response.xpath(
            "//param[@name='FlashVars']/@value").extract_first()
        if xml_data is None:
            self.logger.error(f'\nNo xml data found, stock: {item.get("stockid")}, '
                              f'typecode: {item.get("typecode")}, url: {response.url}')
            if item.get('typecode') == 'laborgetcash' and 'inspremcash' not in item:
                item['inspremcash'] = True
                yield self._request_inspremcash(item)
        else:
            xml_data = xml_data[len('&dataXML='):]
            # self.logger.debug(f'\nxml_data:\n{xml_data}\n')

            dom = xml.dom.minidom.parseString(xml_data)
            root = dom.documentElement
            date_values = root.getElementsByTagName('set')
            for date_value in date_values:
                value = date_value.getAttribute('value')
                if not value: # value = ''
                    continue
                if item.get("typecode") == 'assetsturnratio':
                    value = float(value) * 100
                    value = f'{value:.2f}'
                date = date_value.getAttribute('hoverText')
                self.logger.debug(f'\ndate: {date}, value: {value}')
                if date in self.settings['QUARTERS']:
                    item['values'][date] = value
            # item = {
            #   'stockid': '000001',
            #   'typecode': 'laborgetcash',
            #   'values': {
            #       '20190630': 201222.02,
            #       '20190930': 301222.02
            #   }
            # }
            yield item

    def _stocks(self):
        stock_list_file = self.settings['STOCK_LIST_FILE']
        with open(stock_list_file, 'rt', encoding='utf-8') as f:
            _ = f.readline()
            for line in f:
                columns = line.split(',')
                stockid = columns[2]
                yield stockid

    def _generate_typecode_urls(self, stockid):
        typecode_urls = []
        # 销售商品提供劳务收到的现金
        laborgetcash_components = (
            'http',
            'vip.stock.finance.sina.com.cn',
            'corp/view/vFD_FinanceSummaryHistory.php',
            f'stockid={stockid}&typecode=LABORGETCASH&cate=xjll0',
            None
        )
        laborgetcash_url = urllib.parse.urlunsplit(laborgetcash_components)
        typecode_urls.append(('laborgetcash', laborgetcash_url))

        # 销售收入
        bizinco_components = (
            'http',
            'money.finance.sina.com.cn',
            'corp/view/vFD_FinanceSummaryHistory.php',
            f'stockid={stockid}&type=BIZINCO&cate=liru0',
            None
        )
        bizinco_url = urllib.parse.urlunsplit(bizinco_components)
        typecode_urls.append(('bizinco', bizinco_url))

        # 净资产收益率
        roe_components = (
            'http',
            'money.finance.sina.com.cn',
            'corp/view/vFD_FinancialGuideLineHistory.php',
            f'stockid={stockid}&typecode=financialratios62',
            None
        )
        roe_url = urllib.parse.urlunsplit(roe_components)
        typecode_urls.append(('roe', roe_url))

        # 总资产周转率
        assetsturnratio_components = (
            'http',
            'money.finance.sina.com.cn',
            'corp/view/vFD_FinancialGuideLineHistory.php',
            f'stockid={stockid}&typecode=financialratios21',
            None
        )
        assetsturnratio_url = urllib.parse.urlunsplit(
            assetsturnratio_components)
        typecode_urls.append(('assetsturnratio', assetsturnratio_url))

        # 商誉
        goodwill_components = (
            'http',
            'money.finance.sina.com.cn',
            'corp/view/vFD_FinanceSummaryHistory.php',
            f'stockid={stockid}&type=GOODWILL&cate=zcfz0',
            None
        )
        goodwill_url = urllib.parse.urlunsplit(goodwill_components)
        typecode_urls.append(('goodwill', goodwill_url))

        # 归属于母公司股东权益
        equity_components = (
            'http',
            'money.finance.sina.com.cn',
            'corp/view/vFD_FinanceSummaryHistory.php',
            f'stockid={stockid}&type=PARESHARRIGH&cate=zcfz0',
            None
        )
        equity_url = urllib.parse.urlunsplit(equity_components)
        typecode_urls.append(('equity', equity_url))

        # 销售毛利率
        grossprofitmarginratio_components = (
            'http',
            'money.finance.sina.com.cn',
            'corp/view/vFD_FinancialGuideLineHistory.php',
            f'stockid={stockid}&typecode=financialratios36',
            None
        )
        grossprofitmarginratio_url = urllib.parse.urlunsplit(
            grossprofitmarginratio_components)
        typecode_urls.append(
            ('grossprofitmarginratio', grossprofitmarginratio_url))

        return typecode_urls