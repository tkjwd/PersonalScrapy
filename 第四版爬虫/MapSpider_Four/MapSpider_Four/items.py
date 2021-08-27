# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MapspiderFourItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    CbdName = scrapy.Field()
    City = scrapy.Field()
    District = scrapy.Field()
    BusinessArea = scrapy.Field()
    Address = scrapy.Field()
    Storey = scrapy.Field()
    Storey_detail = scrapy.Field()
    Area = scrapy.Field()
    Ratio = scrapy.Field()
    Ratio_detail = scrapy.Field()
    High = scrapy.Field()
    High_detail = scrapy.Field()
    ElevatorCount = scrapy.Field()
    ElevatorCount_detail = scrapy.Field()
    Developers = scrapy.Field()
    Developers_detail = scrapy.Field()
    Estate = scrapy.Field()
    Estate_detail = scrapy.Field()
    SettledEnterprise = scrapy.Field()
    Introduction = scrapy.Field()
    SourceUrl = scrapy.Field()

    def insert_sql(self):
        sql = """
                    INSERT INTO cbd_detail(
                                CbdName,
                                City,
                                District,
                                BusinessArea,
                                Address,
                                Storey,
                                Storey_detail,
                                Area,
                                Ratio,
                                Ratio_detail,
                                High,
                                High_detail,
                                ElevatorCount,
                                ElevatorCount_detail,
                                Developers,
                                Developers_detail,
                                Estate,
                                Estate_detail,
                                SettledEnterprise,
                                Introduction,
                                SourceUrl
                                )
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                            """

        params = (
            self['CbdName'], self['City'], self['District'], self['BusinessArea'], self['Address'],
            self['Storey'], self['Storey_detail'], self['Area'], self['Ratio'], self['Ratio_detail'], self['High'],
            self['High_detail'], self['ElevatorCount'], self['ElevatorCount_detail'], self['Developers'], self['Developers_detail'],
            self['Estate'], self['Estate_detail'], self['SettledEnterprise'], self['Introduction'], self['SourceUrl']
        )

        return sql, params


class DDZCbdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    CbdName = scrapy.Field()
    City = scrapy.Field()
    District = scrapy.Field()
    EndDate = scrapy.Field()
    Address = scrapy.Field()
    High = scrapy.Field()
    Storey = scrapy.Field()
    Estate = scrapy.Field()
    EstateFee = scrapy.Field()
    Parking = scrapy.Field()
    ParkingFee = scrapy.Field()
    AirConditioner = scrapy.Field()
    AirConditionerFee = scrapy.Field()
    AirConditionerPeriod = scrapy.Field()
    ElevatorCount = scrapy.Field()
    Network = scrapy.Field()
    SettledEnterprise = scrapy.Field()
    Introduction = scrapy.Field()

    def insert_sql(self):
        sql = """
                    INSERT INTO ddz_cbd_detail(
                                CbdName,
                                City,
                                District,
                                EndDate,
                                Address,
                                High,
                                Storey,
                                Estate,
                                EstateFee,
                                Parking,
                                ParkingFee,
                                AirConditioner,
                                AirConditionerFee,
                                AirConditionerPeriod,
                                ElevatorCount,
                                Network,
                                SettledEnterprise,
                                Introduction
                                )
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                            """

        params = (
            self['CbdName'], self['City'], self['District'], self['EndDate'], self['Address'], self['High'],
            self['Storey'], self['Estate'], self['EstateFee'], self['Parking'], self['ParkingFee'],
            self['AirConditioner'], self['AirConditionerFee'], self['AirConditionerPeriod'], self['ElevatorCount'],
            self['Network'], self['SettledEnterprise'], self['Introduction']
        )

        return sql, params


class HzozucountItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    City = scrapy.Field()
    url = scrapy.Field()

    def insert_sql(self):
        sql = """
                    INSERT INTO cbd_url(
                                City,
                                url
                                )
                                VALUES (%s,%s)
                                            """

        params = (
            self['City'], self['url']
        )

        return sql, params
