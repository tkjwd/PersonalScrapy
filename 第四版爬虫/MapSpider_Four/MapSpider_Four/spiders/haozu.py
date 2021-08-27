# -*- coding: utf-8 -*-
import re
import scrapy
from time import sleep
from tools.Mysql_Help import MysqlHelp
from tools.Redis_Help import RedisHelp
from area_helper.get_right_area import GetRightArea
from tools.dbs_config import *
from tools.sql_statement import *
from scrapy_redis.spiders import RedisSpider
from tools.time_help import StopSpider
from MapSpider_Four.items import MapspiderFourItem, HzozucountItem
from scrapy.cmdline import execute


class HaozuSpider(RedisSpider):
    name = 'haozu'
    redis_key = "haozu:start_urls"
    HTTPERROR_ALLOWED_CODES = [503, 502]
    handle_httpstatus_list = [502]

    MH = MysqlHelp(db=mysql_db, host=mysql_host, port=mysql_port, user=mysql_user, pwd=mysql_pwd, is_dict=mysql_is_dict)

    StopSpider = StopSpider()

    def start_requests(self):
        data = self.get_url_data()
        for ct, url in data:
            # item = HzozucountItem()
            # print("------------id:%d-------------" % id)
            print("------------id:%d-------------" % ct)
            try:
                start_urls = url
                # start_urls = 'http://www.haozu.com/bj/'
                # start_urls = 'https://www.haozu.com/bj/zuxiezilou/'
                # start_urls = 'https://www.haozu.com/bj/zuxiezilou/o2/'
                # start_urls = 'https://www.haozu.com/bj_xzl_27/'
                # start_urls = 'http://www.haozu.com/cc_xzl_63919/'
                yield scrapy.Request(
                    url=start_urls,
                    # callback=self.parse,
                    callback=self.parse,
                    # dont_filter=True,
                    meta={"item": url}
                )
            except Exception as e:
                print(e)
                pass

    def parse(self, response):
        url = response.meta["item"]
        # item = response.meta["item"]
        # item = HzozucountItem()
        item = MapspiderFourItem()
        print("parse:", response.status)
        #     url_city_list = response.xpath('/html/body/div[2]/div[1]/div/div/ul//li//p/a/@href').extract()
        #     city_list = response.xpath('/html/body/div[2]/div[1]/div/div/ul//li//p/a/text()').extract()
        #     for i in range(len(url_city_list)):
        #         item['City'] = city_list[i]
        #         start_url = 'http:' + url_city_list[i] + 'zuxiezilou/'
        #         yield scrapy.Request(
        #             url=start_url,
        #             callback=self.parse_cbd,
        #             # dont_filter=True,
        #             meta={"item": item}
        #         )
        # for url_city in url_city_list[2:3]:
        #     # item = CbdItem()
        #     start_url = 'http:' + url_city + 'zuxiezilou/'
        #     yield scrapy.Request(
        #         url=start_url,
        #         callback=self.parse_cbd,
        #         # dont_filter=True,
        # meta={"item": item}
        #     )
        # item = CbdItem()
        xpath_string = '/html/body/div[2]/div[4]/div[1]/ul//li/span[contains(text(),"{}")]/../div/text()'
        xpath_string_detail = '/html/body/div[2]/div[4]/div[1]/ul//li/span[contains(text(),"{}")]/../div/ul//li/span/text() |/html/body/div[2]/div[4]/div[1]/ul//li/span[contains(text(),"{}")]/../div/ul//li/text()'
        if response.status == 200:
        # if len(response.xpath('/html/body/div[2]/div[4]/div[1]/ul/text()').extract()) > 1:
            try:
                # 楼宇名称
                item['CbdName'] = ''.join(
                    response.xpath('/html/body/div[2]/div[2]/div/div/div[1]/h1/span/text()').extract())
                # 所在城市
                item['City'] = ''.join(response.xpath('/html/body/div[1]/div/div[1]/span/text()').extract())
                # 所在区域
                item['District'] = ''.join(
                    response.xpath('/html/body/div[2]/div[2]/div/div/div[2]/span[1]//a/text()').extract()[0])
                # 所在商圈
                item['BusinessArea'] = ''.join(
                    response.xpath('/html/body/div[2]/div[2]/div/div/div[2]/span[1]//a/text()').extract()[1])
                # 地址
                item['Address'] = \
                response.xpath('/html/body/div[2]/div[2]/div/div/div[2]/span[1]/text()').extract()[1]
                # 总楼层
                item['Storey'] = ''.join(response.xpath(xpath_string.format('总楼层')).extract()).strip()
                item['Storey_detail'] = ';'.join(
                    ''.join(response.xpath(xpath_string_detail.format('总楼层', '总楼层')).extract()).strip().split())
                # 建筑面积
                item['Area'] = ''.join(response.xpath(xpath_string.format('建筑面积')).extract()).strip()
                # 得房率
                item['Ratio'] = ''.join(response.xpath(xpath_string.format('得房率')).extract()).strip()
                item['Ratio_detail'] = ';'.join(
                    ''.join(response.xpath(xpath_string_detail.format('得房率', '得房率')).extract()).strip().split())
                # 标准层高
                item['High'] = ''.join(response.xpath(xpath_string.format('标准层高')).extract()).strip()
                item['High_detail'] = ''.join(
                    response.xpath(xpath_string_detail.format('标准层高', '标准层高')).extract()).strip()
                # 客梯数
                item['ElevatorCount'] = ''.join(response.xpath(xpath_string.format('客梯数')).extract()).strip()
                item['ElevatorCount_detail'] = ''.join(
                    response.xpath(xpath_string_detail.format('客梯数', '客梯数')).extract()).strip()
                # 开发商
                item['Developers'] = ''.join(response.xpath(xpath_string.format('开发商')).extract()).strip()
                item['Developers_detail'] = ''.join(
                    response.xpath(xpath_string_detail.format('开发商', '开发商')).extract())
                # 物业公司
                item['Estate'] = ''.join(response.xpath(xpath_string.format('物业公司')).extract()).strip()
                item['Estate_detail'] = ''.join(
                    response.xpath(xpath_string_detail.format('物业公司', '物业公司')).extract())
                # 入驻企业
                item['SettledEnterprise'] = ''.join(
                    response.xpath(xpath_string.format('入驻企业')).extract()).strip()
                # 大厦简介
                item['Introduction'] = ''.join(response.xpath('//*[@id="switch-widget"]/text()').extract()).strip()
                item['SourceUrl'] = url
                yield item
            except Exception as e:
                print(response, e)

    def parse_cbd(self, response):
        item = response.meta["item"]
        # item = HzozucountItem()
        print("parse_cbd:", response.status)
        if response.status == 502:
            sleep(self.StopSpider.get_sleep_time())
        else:
            cbd_list = response.xpath(
                '/html/body/div[3]/div[1]/ul[@class="listCon propertyList"]//li//div[@class="list-content fl"]/h1/a/@href').extract()

            for cbd in cbd_list:
                if '//cowork.haozu.com/' in cbd:
                    continue
                start_url = 'http://www.haozu.com' + cbd
                # item['City'] = ''
                item['url'] = start_url
                yield item
                sleep(0.5)
                # yield scrapy.Request(
                #     url=start_url,
                #     callback=self.parse_cbd_detail,
                #     # dont_filter=True,
                #     # meta={"item": item}
                # )

            next_page = response.xpath('/html/body/div[3]/div[1]/div[2]/ul//li/a[@class = "next"]/@href').extract()
            if next_page:
                next_url = 'http://www.haozu.com' + next_page[0]
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_cbd,
                    # dont_filter=True,
                    meta={"item": item}
                )

    def parse_cbd_detail(self, response):
        # item = response.meta["item"]
        item = MapspiderFourItem()
        print("parse_cbd_detail:", response.status)
        if response.status == 502:
            sleep(self.StopSpider.get_sleep_time())
        else:
            xpath_string = '/html/body/div[2]/div[4]/div[1]/ul//li/span[contains(text(),"{}")]/../div/text()'
            xpath_string_detail = '/html/body/div[2]/div[4]/div[1]/ul//li/span[contains(text(),"{}")]/../div/ul//li/span/text() |/html/body/div[2]/div[4]/div[1]/ul//li/span[contains(text(),"{}")]/../div/ul//li/text()'
            if len(response.xpath('/html/body/div[2]/div[4]/div[1]/ul/text()').extract()) > 1:
                try:
                    # 楼宇名称
                    item['CbdName'] = ''.join(
                        response.xpath('/html/body/div[2]/div[2]/div/div/div[1]/h1/span/text()').extract())
                    # 所在城市
                    item['City'] = ''.join(response.xpath('/html/body/div[1]/div/div[1]/span/text()').extract())
                    # 所在区域
                    item['District'] = ''.join(
                        response.xpath('/html/body/div[2]/div[2]/div/div/div[2]/span[1]//a/text()').extract()[0])
                    # 所在商圈
                    item['BusinessArea'] = ''.join(
                        response.xpath('/html/body/div[2]/div[2]/div/div/div[2]/span[1]//a/text()').extract()[1])
                    # 地址
                    item['Address'] = \
                    response.xpath('/html/body/div[2]/div[2]/div/div/div[2]/span[1]/text()').extract()[1]
                    # 总楼层
                    item['Storey'] = ''.join(response.xpath(xpath_string.format('总楼层')).extract()).strip()
                    item['Storey_detail'] = ';'.join(
                        ''.join(response.xpath(xpath_string_detail.format('总楼层', '总楼层')).extract()).strip().split())
                    # 建筑面积
                    item['Area'] = ''.join(response.xpath(xpath_string.format('建筑面积')).extract()).strip()
                    # 得房率
                    item['Ratio'] = ''.join(response.xpath(xpath_string.format('得房率')).extract()).strip()
                    item['Ratio_detail'] = ';'.join(
                        ''.join(response.xpath(xpath_string_detail.format('得房率', '得房率')).extract()).strip().split())
                    # 标准层高
                    item['High'] = ''.join(response.xpath(xpath_string.format('标准层高')).extract()).strip()
                    item['High_detail'] = ''.join(
                        response.xpath(xpath_string_detail.format('标准层高', '标准层高')).extract()).strip()
                    # 客梯数
                    item['ElevatorCount'] = ''.join(response.xpath(xpath_string.format('客梯数')).extract()).strip()
                    item['ElevatorCount_detail'] = ''.join(
                        response.xpath(xpath_string_detail.format('客梯数', '客梯数')).extract()).strip()
                    # 开发商
                    item['Developers'] = ''.join(response.xpath(xpath_string.format('开发商')).extract()).strip()
                    item['Developers_detail'] = ''.join(
                        response.xpath(xpath_string_detail.format('开发商', '开发商')).extract())
                    # 物业公司
                    item['Estate'] = ''.join(response.xpath(xpath_string.format('物业公司')).extract()).strip()
                    item['Estate_detail'] = ''.join(
                        response.xpath(xpath_string_detail.format('物业公司', '物业公司')).extract())
                    # 入驻企业
                    item['SettledEnterprise'] = ''.join(
                        response.xpath(xpath_string.format('入驻企业')).extract()).strip()
                    # 大厦简介
                    item['Introduction'] = ''.join(response.xpath('//*[@id="switch-widget"]/text()').extract()).strip()
                    yield item
                except Exception as e:
                    print(response, e)

    def get_url_data(self):
        data = self.MH.exe_sql(sql_c)
        return data


if __name__ == '__main__':
    execute(["scrapy", "crawl", "haozu"])
    # execute(["scrapy", "crawl", "haozu", '-s', 'JOBDIR=crawls/haozu-1'])
