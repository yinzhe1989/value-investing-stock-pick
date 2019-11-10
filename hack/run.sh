#!/bin/bash
hackdir=$(cd $(dirname $0); pwd)
echo 'get all stocks...'
python $hackdir/../crawl/get_all_stocks.py
echo 'crawl from sina stock...'
cd $hackdir/../crawl/stock_crawler
scrapy crawl SinaStockCollector
echo 'calculate indicators...'
python $hackdir/../calculate/calc_indicator.py
echo 'filte stocks...'
python $hackdir/../filte/indicator_filter.py
