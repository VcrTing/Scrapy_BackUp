from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider


class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'test_redis'
    redis_key = 'test:start_urls'

    rules = (
        # follow all links
        Rule(LinkExtractor(allow=r'nan_0_0_allvisit_\d{1,2}.html'), callback='parse_page', follow=True),
    )

    # ……
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_DELAY': 1,

        # 指定redis数据库的连接参数
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': 6379,

        # 指定 redis链接密码，和使用哪一个数据库
        'REDIS_PARAMS': {
            'password': 'ZT123zlt',
            'db': 2
        },
    }

    #动态获取allow_domains
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MyCrawler, self).__init__(*args, **kwargs)

    def parse_page(self, response):
        for each in response.xpath('//div[@class="item masonry-brick"]'):
            return {
                'title': each.xpath('./div[@class="title"]/h3/a/text()').extract_first(),
                'content': each.xpath('./div[@class="intro"]/text()').extract_first(),
                'url': response.url,
            }
