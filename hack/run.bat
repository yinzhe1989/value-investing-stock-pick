@echo off
set CUR_DIR=%CD%
set HACK_DIR=%~dp0%
:echo get all stocks...
:python %HACK_DIR%/../crawl/get_all_stocks.py
echo crawl from sina stock...
cd %HACK_DIR%/../crawl/stock_crawler
scrapy crawl SinaStockCollector
cd %CUR_DIR%
echo calculate indicators...
python %HACK_DIR%/../calculate/calc_indicator.py
echo filte stocks...
python %HACK_DIR%/../filte/indicator_filter.py
echo done
