# -*- coding: utf-8 -*-

# Scrapy settings for shijiegongchang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'shijiegongchang'

SPIDER_MODULES = ['shijiegongchang.spiders']
NEWSPIDER_MODULE = 'shijiegongchang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = "DEBUG"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    ":authority":"company.ch.gongchang.com",
    ":method":"GET",
    ":path":"/",
    ":scheme":"https",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"max-age=0",
    # "cookie":"LiveWSLRW77021783=e0b725cea87f469c94f9bec2a9def1e6; NLRW77021783fistvisitetime=1561219508135; NLRW77021783visitecounts=1; NLRW77021783lastvisitetime=1561219526517; NLRW77021783visitepages=2; _GCWGuid=D3BE5D26-0304-5F94-0107-0A8F0D58D891; Hm_lvt_87381154dcd52df3d7d1362797d6c4dc=1561219890; Hm_lvt_a39a1bb1395dcbf5a2fd98bbce30ec99=1561256825,1561257692,1562940727; Hm_lvt_1feded28e200c1f62aa6738cb40e9f68=1561219890,1561256825,1561257692,1562940727; Hm_lpvt_1feded28e200c1f62aa6738cb40e9f68=1562940865; Hm_lpvt_a39a1bb1395dcbf5a2fd98bbce30ec99=1562940865",
    "referer":"https://ch.gongchang.com/",
    "upgrade-insecure-requests":"1",
    # "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'shijiegongchang.middlewares.ShijiegongchangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'shijiegongchang.middlewares.ShijiegongchangDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'shijiegongchang.pipelines.MysqlTwistedPiplines': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_PORT = '3306'
MYSQL_DBNAME = 'spider_data_base'

# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # 确保所有爬虫共享相同的去重指纹
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # SCHEDULER_QUEUE_CLASS='scrapy_redis.queue.LifoQueue'
# DB_IP = 'localhost'
# dbNum = 1
# Redis_IP = 'localhost'
# REDIS_URL = 'redis://{0}:6379/{1}'.format(Redis_IP, dbNum)
# # Persist 允许暂停
# SCHEDULER_PERSIST = True
# SCHEDULER_FLUSH_ON_START = True
