# -*- coding: utf-8 -*-
from scrapy.downloadermiddlewares.retry import RetryMiddleware
# from scrapy import crawler
# crawler.engine.close_spider(spider, 'closespider_pagecount')
#
# sql_c = """SELECT company_id,company_name,lng,lat,company_address,row_id,area_name FROM map_address_f_pflsy_copy1 LIMIT 59386,100000"""

table_name = "c_zzy"
sql_c = """SELECT id,url FROM cbd_url"""


# sql_d = """SELECT * FROM map_address_f_pflsy_v1 f
# WHERE (f.lat,f.lng) IN (SELECT lat,lng FROM map_address_f_pflsy_v1 GROUP BY lat,lng HAVING count(*)>1) ORDER BY f.lat,f.lng;"""
