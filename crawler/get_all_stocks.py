import tushare as ts
import os

if __name__ == '__main__':
    token = os.getenv('TUSHARE_TOKEN')
    if not token:
        print('No env TUSHARE_TOKEN found!')
        exit(-1)
    ts.set_token(token)
    pro = ts.pro_api()
    df = pro.stock_basic(exchange='', list_status='L', fields='symbol,name,exchange')
    df.to_csv('../tmp/stocks.csv')