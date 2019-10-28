import scrapy

class SinaStockCollector(scrapy.Spider):
    name = 'SinaStockCollector'

    def __init__(self):
        self.url_base = 'http://money.finance.sina.com.cn'

    def start_requests(self):
        url = 'http://money.finance.sina.com.cn/corp/view/vFD_FinancialGuideLineHistory.php?stockid=300760&typecode=financialratios26'
        request = scrapy.Request(url, callback=self.parse_financialratios26)
        yield request

    def parse_financialratios26(self, response):
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
