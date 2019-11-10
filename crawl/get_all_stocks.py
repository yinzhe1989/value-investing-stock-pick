import tushare as ts
import os
from datetime import date, timedelta
import pandas

if __name__ == '__main__':
    token = os.getenv('TUSHARE_TOKEN')
    if not token:
        print('No env TUSHARE_TOKEN found!')
        exit(-1)
    ts.set_token(token)
    pro = ts.pro_api()

    # 获取交易日期
    trade_date = ''
    today = date.today()
    start_date = today-timedelta(days=10)
    start_date = start_date.strftime('%Y%m%d')
    end_date = today.strftime('%Y%m%d')
    print(f'start_date: {start_date}, end_date: {end_date}')
    df = pro.query('trade_cal', start_date=start_date, end_date=end_date)
    for i in reversed(df.index):
        if df.loc[i].values[2]:
            trade_date = df.loc[i].values[1]
            break
    assert trade_date
    print(f'trade_date: {trade_date}')

    # 获取市盈率、市值等数据
    df_daily_basic = pro.daily_basic(
        ts_code='', trade_date=trade_date, fields='ts_code,pe,pe_ttm,pb,total_mv,circ_mv')

    # 获取股票列表
    df_stock_basic = pro.stock_basic(
        exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    
    # 合并保存
    df = pandas.merge(df_stock_basic, df_daily_basic, how='left', on='ts_code')
    df.to_csv('../tmp/stocks.csv')