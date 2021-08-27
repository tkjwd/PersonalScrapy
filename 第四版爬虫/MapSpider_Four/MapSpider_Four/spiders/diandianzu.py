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
from MapSpider_Four.items import DDZCbdItem
from scrapy.cmdline import execute


class DiandianzuSpider(RedisSpider):
    name = 'diandianzu'
    allowed_domains = ['diandianzu.com']
    StopSpider = StopSpider()

    def start_requests(self):
        try:
            start_urls = 'https://gz.diandianzu.com/'
            yield scrapy.Request(
                url=start_urls,
                # callback=self.parse,
                callback=self.parse,
                # dont_filter=True,
                # meta={"item": item}
            )
        except Exception as e:
            print(e)
            pass

    def parse(self, response):
        url_city_list = response.xpath('/html/body/div[1]/div[1]/div[3]/div[1]/div/div[2]//a/@href').extract()
        for url_city in url_city_list:
            if '//london.diandianzu.com/' in url_city:
                continue
            head_url = 'http:' + url_city
            start_url = head_url + 'listing'
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_cbd,
                # dont_filter=True,
                meta={"item": head_url}
            )
        # item = DDZCbdItem()
        # if len(response.xpath('/html/body//div[@class="desc-box building-box left-box clearfix"]/text()').extract()) > 1:
        #     try:
        #         detials = response.xpath(
        #             '/html/body//div[@class="desc-box building-box left-box clearfix"]//span[@class="f-con"]/text()').extract()
        #         # 楼宇名称
        #         item['CbdName'] = ''.join(response.xpath('/html/body//div[@class="top-buildingName fl"]/h1/text()').extract())
        #         # 所在城市
        #         item['City'] = ''.join(response.xpath('/html/body//p[@class="attr-location"]//a[1]/text()').extract())
        #         # 所在区域
        #         item['District'] = ''.join(response.xpath('/html/body//p[@class="attr-location"]//a[2]/text()').extract())
        #         # 竣工时间
        #         item['EndDate'] = detials[0]
        #         # 地理位置
        #         item['Address'] = ''.join(response.xpath('/html/body//div[@class="desc-box building-box left-box clearfix"]//a[@class="location-link"]/text()').extract())
        #         # 层高
        #         item['High'] = detials[1]
        #         # 层数
        #         item['Storey'] = detials[2]
        #         # 物业
        #         item['Estate'] = detials[3]
        #         # 物业费
        #         item['EstateFee'] = detials[4]
        #         # 车位
        #         item['Parking'] = detials[5]
        #         # 车位月租金
        #         item['ParkingFee'] = detials[6]
        #         # 空调
        #         item['AirConditioner'] = detials[7]
        #         # 空调费
        #         item['AirConditionerFee'] = detials[8]
        #         # 空调开放时长
        #         item['AirConditionerPeriod'] = detials[9]
        #         # 电梯
        #         item['ElevatorCount'] = detials[10]
        #         # 网络
        #         item['Network'] = detials[11]
        #         # 入驻企业
        #         item['SettledEnterprise'] = detials[12]
        #         # 大厦简介
        #         item['Introduction'] = ''.join(response.xpath('/html/body//div[@class="desc-box building-box left-box clearfix"]//div[@class="desc-full hide"]/text()').extract()).strip()
        #         # yield item
        #     except Exception as e:
        #         print(response, e)

    def parse_cbd(self, response):
        item = response.meta["item"]
        cbd_list = response.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]//div/div/@data-href').extract()
        for cbd in cbd_list:
            start_url = item + cbd.lstrip('/')
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_cbd_detail,
                # dont_filter=True,
                # meta={"item": item}
            )
        next_page = response.xpath(
            '/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div//a[@class = "next tj-pc-listingList-page-click"]/@href ').extract()
        if next_page:
            next_url = item + next_page[0].lstrip('/')
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_cbd,
                # dont_filter=True,
                meta={"item": item}
            )

    def parse_cbd_detail(self, response):
        # item = response.meta["item"]
        item = DDZCbdItem()
        if len(response.xpath(
                '/html/body//div[@class="desc-box building-box left-box clearfix"]/text()').extract()) > 1:
            try:
                detials = response.xpath(
                    '/html/body//div[@class="desc-box building-box left-box clearfix"]//span[@class="f-con"]/text()').extract()
                # 楼宇名称
                item['CbdName'] = ''.join(
                    response.xpath('/html/body//div[@class="top-buildingName fl"]/h1/text()').extract())
                # 所在城市
                item['City'] = ''.join(
                    response.xpath('/html/body//p[@class="attr-location"]//a[1]/text()').extract())
                # 所在区域
                item['District'] = ''.join(
                    response.xpath('/html/body//p[@class="attr-location"]//a[2]/text()').extract())
                # 竣工时间
                item['EndDate'] = detials[0]
                # 地理位置
                item['Address'] = ''.join(response.xpath(
                    '/html/body//div[@class="desc-box building-box left-box clearfix"]//a[@class="location-link"]/text()').extract())
                # 层高
                item['High'] = detials[1]
                # 层数
                item['Storey'] = detials[2]
                # 物业
                item['Estate'] = detials[3]
                # 物业费
                item['EstateFee'] = detials[4]
                # 车位
                item['Parking'] = detials[5]
                # 车位月租金
                item['ParkingFee'] = detials[6]
                # 空调
                item['AirConditioner'] = detials[7]
                # 空调费
                item['AirConditionerFee'] = detials[8]
                # 空调开放时长
                item['AirConditionerPeriod'] = detials[9]
                # 电梯
                item['ElevatorCount'] = detials[10]
                # 网络
                item['Network'] = detials[11]
                # 入驻企业
                item['SettledEnterprise'] = detials[12]
                # 大厦简介
                item['Introduction'] = ''.join(response.xpath(
                    '/html/body//div[@class="desc-box building-box left-box clearfix"]//div[@class="desc-full hide"]/text()').extract()).strip()
                yield item
            except Exception as e:
                print(response, e)


if __name__ == '__main__':
    execute(["scrapy", "crawl", "diandianzu"])
