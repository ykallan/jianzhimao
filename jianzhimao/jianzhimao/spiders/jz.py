import scrapy


class JzSpider(scrapy.Spider):
    name = 'jz'
    # allowed_domains = ['jz.com']
    start_urls = ['https://www.jianzhimao.com/ctrlcity/changeCity.html']

    def parse(self, response):
        links = response.xpath('//ul[@class="city_table"]/li/a/@href').getall()
        for one_link in links:
            yield scrapy.Request(url=one_link, callback=self.parse_citys)

    def parse_citys(self, response):
        jobs = response.xpath('//ul[@class="content_list_wrap"]/li/a/@href').getall()
        for one_job in jobs:
            yield response.follow(url=one_job, callback=self.parse_detail)
        pages = response.xpath('//ul[@class="content_page_wrap"]/li/a/@href').getall()
        if pages:
            for page in pages:
                yield response.follow(url=page, callback=self.parse_citys)

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="job_title"]/text()').get()
        company = response.xpath('//div[@class="job_header"]/p[@class="info"]/text()').get()

        # print(title, company)
        com_intro = response.xpath('//div[@class="company_info"]/p[1]/text()').get()
        # print(com_intro)
        com_loc = response.xpath('//div[@class="company_info"]/p[2]/text()').get()
        # print(com_loc)

        price = response.xpath('//div[@class="job_base"]/span[@class="job_price"]/text()').get().strip()
        # print(price)
        details = response.xpath('//div[@class="box"]/div[@class="detail"]/text()').getall()
        detail = '\n'.join(x.strip() for x in details)

        item = {}
        item['title'] = title
        item['company'] = company
        item['com_intro'] = com_intro
        item['com_loc'] = com_loc
        item['price'] = price
        item['detail'] = detail
        yield item
