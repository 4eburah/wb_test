'''Script scraps all posts from http://forum.mfd.ru/forum/subforum/?id=649
Usage: scrapy crawl topics
see details at https://docs.scrapy.org/en/latest/intro/overview.html
'''

from urllib import parse

import scrapy

class TopicSpider(scrapy.Spider):
    '''Main class for scraping. You run it as: scrapy crawl topics'''

    name = "topics"
    #handle_httpstatus_list = [403]

    start_urls = ['http://forum.mfd.ru/forum/subforum/?id=649', 'http://forum.mfd.ru/forum/subforum/?id=649&page=1', ]

    def parse(self, response):
        '''Parses start_urls'''

        for href in response.xpath('//td[has-class("mfd-item-subject")]/a/@href'):
            yield response.follow(href, callback=self.parse_topic)

    def parse_topic(self, response):
        '''Parses topics at subforum'''

        print(response.url)

        # get topic id

        topic_id = parse.parse_qs(parse.urlparse(response.url).query)['id'][0]

        # get topic name

        topic_name = response.xpath('//div[has-class("mfd-header")]/h1/text()').get()

        for post in response.xpath('//div[has-class("mfd-post")]'):
            parsed_post = self.parse_post(post)

            parsed_post['topic_id'] = int(topic_id)
            parsed_post['topic_name'] = topic_name

            yield parsed_post

        previous_page = response.xpath('//a[has-class("mfd-paginator-selected")]/preceding-sibling::a[1]/@href').get()

        if previous_page is not None:
            yield response.follow(previous_page, callback=self.parse_topic)

    def parse_post(self, post_selector):
        '''Parses topics posts

        arguments:
        post_selector -- Scrapy selector object
        '''

        post_dict = {}

        # get post id

        post_id = post_selector.xpath('./div[has-class("mfd-post-top")]/div[@id]/@id').get()

        post_dict['id'] = int(post_id)

        # post url and date

        url = post_selector.xpath('.//a[has-class("mfd-post-link")]/@href').get()
        post_date = post_selector.xpath('.//a[has-class("mfd-post-link")]/text()').get()

        post_dict['url'] = url
        post_dict['post_date'] = post_date

        # author and author id

        author_name = post_selector.xpath('.//a[has-class("mfd-poster-link")]/text()').get()
        author_title = post_selector.xpath('.//a[has-class("mfd-poster-link")]/@title').get()

        author_id = None
        if author_title is not None:
            author_id = int(author_title.lstrip('ID: '))

        post_dict['author'] = author_name
        post_dict['author_id'] = author_id

        post_rating = post_selector.xpath('.//span[has-class("u")]/text()').get()

        post_dict['post_rating'] = post_rating

        # post text

        text_list = post_selector.xpath('.//div[has-class("mfd-post-text")]/div[has-class("mfd-quote-text")]/text()').getall()

        text_str = ''.join(text_list)

        post_dict['text'] = text_str

        # post relpies to

        reply_url = post_selector.xpath('.//div[has-class("mfd-post-text")]/blockquote/div[has-class("mfd-quote-info")]/a/@href').get()

        replies_to = None
        if reply_url is not None:
            replies_to = int(reply_url.split('=',1)[1])

        post_dict['replies_to'] = replies_to

        return post_dict
