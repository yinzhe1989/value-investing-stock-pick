# stock-financial-index-filter

本项目根据一系列财务指标进行股票过滤。

财务报表基础知识：

三张表：资产负债表、利润表（损益表）、现金流量表

合并报表(Consolidation of Accounting statement) :是指由母公司编制的包括所有控股子公司会计报表的有关数据的报表。该报表可向报表使用者提供公司集团的财务状况和经营成果。合并报表包括合并资产负债表、合并损益表、合并现金流量表等。

编制合并会计报表的合并理论一般有三种理论可供遵循，即母公司理论、实体理论和当代理论。实务中多采用经修正的当代理论。

第一，母公司理论。按照母公司理论，在企业集团内的股东只包括母公司的股东，将子公司少数股东排除在外，看作是公司集团主体的外界债权人，以这个会计主体编制的合并资产负债表中的股东权益和合并损益表中的净利润仅指母公司拥有和所得部分，把合并会计报表看作是母公司会计报表的延伸和扩展。

第二，实体理论。按照实体理论，在企业集团内把所有的股东同等看待，不论是多数股东还是少数股东均作为该集团内的股东，并不过分强调控股公司股东的权益。采用这种理论编制的合并会计报表，能满足企业集团内整个生产经营活动中管理的需求。

第三，当代理论实际上是母公司理论与实体理论的混合，美国公认会计原则采纳了当代理论，所以它在美国实务中被广泛运用。资产负债表中将少数股东权益列示于股东权益项目下，与母公司股东权益分开列示。利润表中将少数股东损益列示于净利润项目下，与归属于母公司所有者净利润分开列示。

总资产-负债=所有者权益（股东权益）
所有者权益=归属于母公司股东权益+少数股东权益
（母公司理论）净资产=归属于母公司股东权益
（实体理论）净资产=所有者权益=归属于母公司股东权益+少数股东权益
下文除了商誉净资产比中的净资产指归属于母公司股东权益，其它都是指所有者权益（比如净资产收益率=净利润/净资产，该净利润和净资产应该都包含归母股东部分和少数股东部分）。因为报表中的少数股东权益不包含商誉，即商誉应该是对应归属于母公司股东权益：如2亿元现金购买1亿元资产，形成1亿元商誉。此时净资产并没有变化。公司在合并报表时，合并报表会增加1亿元的商誉。少数股东权益仍然是子公司净资产对应的比例数。

## 财务指标

### 现金收入比

反映了公司的盈利质量

- 计算公式
现金收入比=销售商品提供劳务收到的现金/销售收入
- 数据来源
销售商品提供劳务收到的现金：现金流量表
销售收入：利润表
- 过滤条件
现金收入比大于等于 100%

### 净资产收益率

反映公司的盈利能力

- 计算公式
净资产收益率=净利润/净资产
- 数据来源
净资产收益率各大网站均可获取
- 过滤条件
净资产收益率过去 5 年在 15% 以上

### 总资产周转率

反映公司的运营能力

- 计算公式
总资产周转率=销售收入/总资产
- 数据来源
总资产周转率各大网站均可获取
- 过滤条件
总资产周转率超过 100%

### 季度收入增长率

反映公司的成长能力

- 计算公式
季度收入增长率=(本年本季度销售收入-去年同季度销售收入)/去年同季度销售收入
- 数据来源
销售收入（营业收入）：利润表
- 过滤条件
过去 8 个季度，每个季度的收入增长率都超过 15%

### 商誉净资产比

反映溢价的无形资产所占比重，越小越好

- 计算公式
商誉净资产比=商誉/净资产（归属于母公司股东权益）
- 数据来源
商誉、净资产：资产负债表
- 过滤条件
商誉净资产比低于 50%。如果更谨慎一点的话，商誉净资产比低于 30%

### 毛利率

反映了企业的核心竞争能力和核心盈利能力

- 计算公式
毛利率=(主营业务收入-主营业务成本)/主营业务收入=(销售收入-销售成本)/销售收入
- 数据来源
主营业务收入、主营业务成本：利润表
销售毛利率各大网站均可获取
- 过滤条件
    1. 选择毛利率高一点的公司进行投资
    2. 拉长时间，除非外部环境有重大变化，否则公司毛利率一般比较稳定，不太会有大幅波动
    3. 公司毛利率和行业内其他公司相比，相差的幅度不会变化很大

## 模块

### 数据采集

使用scrapy实现数据采集，数据源为[新浪财经](http://finance.sina.com.cn)

- 模块输入
    1. 股票列表文件
    2. 财务季度列表
- 模块输出
    输出为redis的hash数据类型的映射表，其中：
    key：股票代码:财务季度，例如：`300760:2019-3`
    field：销售商品提供劳务收到的现金（laborgetcash or inspremcash）、销售收入（bizinco）、净资产收益率（roe）、总资产周转率（assetsturnratio）、商誉（goodwill）、净资产（归属于母公司股东权益）（equity）、销售毛利率（grossprofitmarginratio）
    value：上述field的值
- 数据来源
    1. 销售商品提供劳务收到的现金
    `http://vip.stock.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid=300760&typecode=LABORGETCASH&cate=xjll0`
    `http://money.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid=601318&typecode=INSPREMCASH&cate=xjll3`
    2. 销售收入
    `http://money.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid=600900&type=BIZINCO&cate=liru0`
    3. 净资产收益率
    `http://money.finance.sina.com.cn/corp/view/vFD_FinancialGuideLineHistory.php?stockid=601318&typecode=financialratios59`
    4. 总资产周转率
    `http://money.finance.sina.com.cn/corp/view/vFD_FinancialGuideLineHistory.php?stockid=601318&typecode=financialratios21`
    5. 商誉
    `http://money.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid=601318&type=GOODWILL&cate=zcfz3`
    6. 归属于母公司股东权益
    `http://money.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid=601318&type=PARESHARRIGH&cate=zcfz3`
    7. 销售毛利率
    `http://money.finance.sina.com.cn/corp/view/vFD_FinancialGuideLineHistory.php?stockid=600900&typecode=financialratios36`

### 数据存储：redis

获取及计算到的股票财务和指标数据存储在redis中，存储为hash数据类型。以迈瑞医疗（300760）2019第2季度为例：

1. 现金收入比：
    key：300760:2019-2
    field：moneyincomeratio
    value：101.0
2. 净资产收益率
    key：300760:2019-2
    field：roe
    value：20.1
3. 总资产周转率
    key：300760:2019-2
    field：assetsturnratio
    value：36.85
4. 季度收入增长率
    key：300760:2019-2
    field：incomegrowthratio
    value：18.0
5. 商誉净资产比
    key：300760:2019-2
    field：goodwillequityratio
    value：30.0
6. 毛利率
    key：300760:2019-2
    field：grossprofitmarginratio
    value：65.2

### 指标计算

1. 现金收入比：
    moneyincomeratio=laborgetcash/bizinco*100
2. 净资产收益率
    roe
3. 总资产周转率
    assetsturnratio
4. 季度收入增长率
    incomegrowthratio=[bizinco(2019-3)-bizinco(2019-2)]/bizinco(2019-2)*100
5. 商誉净资产比
    goodwillequityratio=goodwill/equity*100
6. 毛利率
    grossprofitmarginratio

### 过滤选股
