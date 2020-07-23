#!/bin/bash
hackdir=$(cd $(dirname $0); pwd)
workdir=$(cd $(dirname "$hackdir"); pwd)
export PYTHONPATH="$workdir"

echo 'get all stocks...'
python "$workdir"/crawl/get_all_stocks.py
echo 'crawl from sina stock...'
cd "$workdir"/crawl/stock_crawler
scrapy crawl SinaStockCollector
echo 'calculate indicators...'
python "$workdir"/calculate/calc_indicator.py
echo 'filte stocks...'
python "$workdir"/filte/indicator_filter.py
