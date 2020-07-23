# -*- coding: utf8 -*-

__version__ = '1.0.0'
__all__ = [
    'DataAccessor',
    'RedisAccessor'
]

from dal.da import DataAccessor
from dal.redis_da import RedisAccessor
