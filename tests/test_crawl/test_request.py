import urllib.parse
import urllib.request
stockid='300760'
laborgetcash_components = (
    'http',
    'money.finance.sina.com.cn',
    'corp/view/vFD_FinanceSummaryHistory.php',
    f'stockid={stockid}&typecode=INSPREMCASH&cate=xjll3',
    None
)

laborgetcash_url = urllib.parse.urlunsplit(laborgetcash_components)
print(laborgetcash_url)
code = urllib.request.urlopen(laborgetcash_url).getcode()
print(code)
if 200 != code:
    laborgetcash_components = (
        'http',
        'vip.stock.finance.sina.com.cn',
        'corp/view/vFD_FinanceSummaryHistory.php',
        f'stockid={stockid}&typecode=LABORGETCASH&cate=xjll0',
        None
    )
    laborgetcash_url = urllib.parse.urlunsplit(laborgetcash_components)
    print(laborgetcash_url)