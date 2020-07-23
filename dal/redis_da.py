from dal.da import DataAccessor
from config import REDIS_HOST, REDIS_PORT, REDIS_USE_CLUSTER
from rediscluster import RedisCluster
from redis import Redis
import logging
import re


class RedisAccessor(DataAccessor):
    def __init__(self, logger=None):
        if REDIS_USE_CLUSTER:
            startup_nodes = [{"host": REDIS_HOST, "port": REDIS_PORT}]
            self._rc = RedisCluster(
                startup_nodes=startup_nodes, decode_responses=True)
        else:
            self._rc = Redis(REDIS_HOST, REDIS_PORT, decode_responses=True)

        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger('RedisAccessor')
            nullHandler = logging.NullHandler()
            self._logger.addHandler(nullHandler)

    def close(self):
        pass

    def add_to_crawl_processed_set(self, stockid, typecode):
        processed_key = self._make_key(stockid, typecode)
        self._rc.sadd('crawlprocessed', processed_key)
    
    def exists_in_crawl_processed_set(self, stockid, typecode):
        processed_key = self._make_key(stockid, typecode)
        return self._rc.sismember('crawlprocessed', processed_key)

    def remove_from_crawl_processed_set(self, stockid, typecode):
        processed_key = self._make_key(stockid, typecode)
        self._rc.srem('crawlprocessed', processed_key)
    
    def flush_crawl_processed_set(self):
        self._rc.delete('crawlprocessed')

    def add_to_calc_processed_set(self, stockid, typecode):
        processed_key = self._make_key(stockid, typecode)
        self._rc.sadd('calcprocessed', processed_key)
    
    def exists_in_calc_processed_set(self, stockid, typecode):
        processed_key = self._make_key(stockid, typecode)
        return self._rc.sismember('calcprocessed', processed_key)

    def remove_from_calc_processed_set(self, stockid, typecode):
        processed_key = self._make_key(stockid, typecode)
        self._rc.srem('calcprocessed', processed_key)
    
    def flush_calc_processed_set(self):
        self._rc.delete('calcprocessed')

    def get_moneyincomeratio(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'moneyincomeratio')

    def mget_moneyincomeratio(self, stockid):
        return self.handle_mget(stockid, 'moneyincomeratio')

    def get_roe(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'roe')

    def mget_roe(self, stockid):
        return self.handle_mget(stockid, 'roe')

    def get_assetsturnratio(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'assetsturnratio')

    def mget_assetsturnratio(self, stockid):
        return self.handle_mget(stockid, 'assetsturnratio')

    def get_incomegrowthratio(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'incomegrowthratio')

    def mget_incomegrowthratio(self, stockid):
        return self.handle_mget(stockid, 'incomegrowthratio')

    def get_goodwillequityratio(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'goodwillequityratio')

    def mget_goodwillequityratio(self, stockid):
        return self.handle_mget(stockid, 'goodwillequityratio')

    def get_grossprofitmarginratio(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'grossprofitmarginratio')

    def mget_grossprofitmarginratio(self, stockid):
        return self.handle_mget(stockid, 'grossprofitmarginratio')

    def get_laborgetcash(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'laborgetcash')

    def mget_laborgetcash(self, stockid):
        return self.handle_mget(stockid, 'laborgetcash')

    def get_bizinco(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'bizinco')

    def mget_bizinco(self, stockid):
        return self.handle_mget(stockid, 'bizinco')

    def get_goodwill(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'goodwill')

    def mget_goodwill(self, stockid):
        return self.handle_mget(stockid, 'goodwill')

    def get_equity(self, stockid, quarter):
        return self.handle_get(stockid, quarter, 'equity')

    def mget_equity(self, stockid):
        return self.handle_mget(stockid, 'equity')

    def handle_get(self, stockid, quarter, typecode):
        quarter = quarter.replace('-', '')
        if re.match(r'(19|20)\d{2}(0331|0630|0930|1231)', quarter) is None:
            raise ValueError(f'quarter format error, expected: YYYYMMDD, got: {quarter}')
        key = self._make_key(stockid, typecode)
        value = self._rc.hget(key, quarter)
        if value:
            value = float(value)
        self._logger.debug(f'RedisAccessor.handle_get, key: {key},'
                           f' field: {quarter}, value: {value}')
        return value

    def handle_mget(self, stockid, typecode):
        key = self._make_key(stockid, typecode)
        quarter_value_dict = self._rc.hmget(key)
        if quarter_value_dict:
            quarter_value_dict = {
                k: float(v) if v else v for k,v in quarter_value_dict.iterItems()
            }
        self._logger.debug(f'RedisAccessor.handle_mget, key: {key},'
                           f' values: {quarter_value_dict}')
        return quarter_value_dict

    def _make_key(self, stockid, codetype):
        # add key hash tags to stockid, so a stock's
        # total date will be allocated in the same hash slot
        return f'{{{stockid}}}:{codetype}'

    def handle_set(self, stockid, quarter, value, typecode):
        quarter = quarter.replace('-', '')
        if re.match(r'(19|20)\d{2}(0331|0630|0930|1231)', quarter) is None:
            raise ValueError(f'quarter format error, expected: YYYYMMDD, got: {quarter}')
        key = self._make_key(stockid, typecode)
        rt = self._rc.hset(key, quarter, value)
        self._logger.debug(f'RedisAccessor.handle_set, key: {key},'
                           f' field: {quarter}, value: {value}, return: {rt}')
        return rt

    def handle_mset(self, stockid, quarter_value_dict, typecode):
        new_quarter_value_dict = {}
        for quarter, value in quarter_value_dict.items():
            quarter = quarter.replace('-', '')
            if re.match(r'(19|20)\d{2}(0331|0630|0930|1231)', quarter) is None:
                raise ValueError(f'quarter format error, expected: YYYYMMDD, got: {quarter}')
            new_quarter_value_dict[quarter] = value
        key = self._make_key(stockid, typecode)
        rt = self._rc.hmset(key, new_quarter_value_dict)
        self._logger.debug(f'RedisAccessor.handle_mset, key: {key},'
                           f' values: {new_quarter_value_dict}, return: {rt}')
        return rt

    def set_moneyincomeratio(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'moneyincomeratio')

    def mset_moneyincomeratio(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'moneyincomeratio')

    def set_roe(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'roe')

    def mset_roe(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'roe')

    def set_assetsturnratio(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'assetsturnratio')

    def mset_assetsturnratio(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'assetsturnratio')

    def set_incomegrowthratio(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'incomegrowthratio')

    def mset_incomegrowthratio(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'incomegrowthratio')

    def set_goodwillequityratio(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'goodwillequityratio')

    def mset_goodwillequityratio(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'goodwillequityratio')

    def set_grossprofitmarginratio(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'grossprofitmarginratio')

    def mset_grossprofitmarginratio(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'grossprofitmarginratio')

    def set_laborgetcash(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'laborgetcash')

    def mset_laborgetcash(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'laborgetcash')

    def set_bizinco(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'bizinco')

    def mset_bizinco(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'bizinco')

    def set_goodwill(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'goodwill')

    def mset_goodwill(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'goodwill')

    def set_equity(self, stockid, quarter, value):
        return self.handle_set(stockid, quarter, value, 'equity')

    def mset_equity(self, stockid, quarter_value_dict):
        return self.handle_mset(stockid, quarter_value_dict, 'equity')
