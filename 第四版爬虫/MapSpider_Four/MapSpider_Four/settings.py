# -*- coding: utf-8 -*-
import random

# Scrapy settings for MapSpider_Four project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'MapSpider_Four'

SPIDER_MODULES = ['MapSpider_Four.spiders']
NEWSPIDER_MODULE = 'MapSpider_Four.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = "DEBUG"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 15
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 4
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False


# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'MapSpider_Four.middlewares.MapspiderFourSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'MapSpider_Four.middlewares.MapspiderFourDownloaderMiddleware': 540,
   #  'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   #  'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'MapSpider_Four.middlewares.ProcessAllExceptionMiddleware': 543,
    # 'MapSpider_Four.middlewares.MyRetryMiddleware': 543,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

MYEXT_ENABLED = True      # 开启扩展
IDLE_NUMBER = 360           # 配置空闲持续时间单位为 360个 ，一个时间单位为5s

# 在 EXTENSIONS 配置，激活扩展
EXTENSIONS = {
    'MapSpider_Four.redis_extensions.RedisSpiderSmartIdleClosedExensions': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'MapSpider_Four.pipelines.MapspiderFourPipeline': 300,
   'MapSpider_Four.pipelines.MysqlTwistedPipelines': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# MYSQL_HOST = '192.168.31.15'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Aa123456NWM' # 你的密码
MYSQL_PORT = '3306'
MYSQL_DBNAME = 'map_data_one'
# MYSQL_DBNAME = 'map_data_all'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
# REDIS_URL = "redis://192.168.31.2:6379/3"
REDIS_URL = "redis://192.168.31.11:6379/6"