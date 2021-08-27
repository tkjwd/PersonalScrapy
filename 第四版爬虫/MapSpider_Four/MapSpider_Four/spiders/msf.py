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
from MapSpider_Four.items import MapspiderFourItem
from scrapy.cmdline import execute


class MsfSpider(RedisSpider):
    name = 'msf'
    redis_key = "msf:start_urls"
    tb_name = table_name
    # key = "7TTBZ-QIGK5-UWNIQ-QHG7K-VEWEV-RUFID"
    key = "MEDBZ-IMD6W-AQIRZ-RYWCO-4HSRS-VAF72"
    # key = "GFUBZ-UZS3U-W7DVH-2OC46-JVOQJ-FGBK3"
    api = ['https://apis.map.qq.com/ws/geocoder/v1/?address={}&key={}']
    # api = ['https://apis.map.qq.com/ws/place/v1/search?boundary=region(全国)&keyword={}&key={}']
    MH = MysqlHelp(db=mysql_db, host=mysql_host, port=mysql_port, user=mysql_user, pwd=mysql_pwd, is_dict=mysql_is_dict)
    RH = RedisHelp(host=redis_host, port=redis_port, pwd=redis_pwd, db=redis_db, des=redis_is_des)
    StopSpider = StopSpider()

    def start_requests(self):
        ct = 1
        data = self.get_map_data()
        for d in data:
            item = MapspiderFourItem()
            # SELECT company_id,company_name,Business_address,id FROM a_nlmy LIMIT 2000000
            item["company_id"] = d[0]
            item["company_name"] = d[1]
            company_address = d[2]
            item["row_id"] = d[3]
            item["industriesid"] = d[4]
            Province = d[5] if d[5] else ""
            City = d[6] if d[6] else ""
            try:
                if Province == City:
                    company_address_f = str(Province + company_address)
                else:
                    company_address_f = str(Province + City + company_address)
                company_address_s = self.clean_address(company_address)
                company_address_new = self.clean_address(company_address_f)
                item["area_name"], item["company_address"] = GetRightArea(company_address_s).get_area_name()
                if item["company_address"]:
                    if Province != item["company_address"][0:len(Province)]:  # 0?1 or X?1
                        if City != item["company_address"][0:len(City)]:  # 001
                            item["company_address"] = company_address_new
                        else:  # 011
                            item["company_address"] = str(Province + company_address_s)
                    elif City != item["company_address"][len(Province):len(str(Province+City))]:  # 101
                        if Province == City:  # 11
                            item["company_address"] = str(Province + company_address_s[len(Province):])
                        else:  # 1X1
                            item["company_address"] = str(Province + City + company_address_s[company_address_s.index('市')+1:])
                    print(ct, item["area_name"], item["company_address"])
                    ct += 1
                    if item["company_address"] == "":
                        item["company_address"] = company_address_new
                    start_urls = self.api[0].format(item["company_address"], self.key)
                    # print(search_url)
                    yield scrapy.Request(
                        url=start_urls,
                        callback=self.parse,
                        # dont_filter=True,
                        meta={"item": item}
                    )
            except Exception as e:
                print(e)
                pass

    def parse(self, response):
        item = response.meta["item"]
        # 收集错误request.url
        if response.text:
            res = json.loads(response.body.decode("utf-8"))
            # 限制流量超标
            if res:
                try:
                    status = res.get("status")
                    message = res.get("message")
                    if status == 121 and "已达到上限" in message:
                        sleep(self.StopSpider.get_sleep_time())
                    else:
                        # location = res.get("data")[0].get("location")
                        location = res.get("result").get("location")
                        lng = location.get("lng")
                        lat = location.get("lat")
                        if lng and lat:
                            item["lng"] = lng
                            item["lat"] = lat
                            if "管城新区" in item["company_address"]:
                                item["area_name"] = "管城区"
                            else:
                                # item["area_name"] = res.get("data")[0].get("ad_info").get("district")
                                item["area_name"] = item["area_name"]
                            yield item
                except Exception as e:
                    print(e)

        else:
            self.RH.Rs_.sadd("{}_Failed_Request_Url".format(self.tb_name), response.url)
            print("{} 表存在失败请求链接".format(self.tb_name))

    def get_map_data(self):
        data = self.MH.exe_sql(sql_c)
        return data

    def clean_address(self, company_address):
        if company_address and company_address != "":
            if "http" in company_address:
                company_address = company_address.split("http")[0]
            elif company_address.startswith("("):
                try:
                    pattren_a = re.compile(r'(\([A-Za-z0-9]\)).*?', re.S)
                    company_add = re.findall(pattren_a, company_address)[0] \
                        if re.findall(pattren_a, company_address) else ""
                    company_address = company_address.replace(company_add, "")
                    # print(company_address)
                except Exception as e:
                    print(e)
                    pass
            elif company_address.startswith("（"):
                try:
                    pattren_b = re.compile(r'(\（[A-Za-z0-9]\）).*?', re.S)
                    company_add = re.findall(pattren_b, company_address)[0] \
                        if re.findall(pattren_b, company_address) else ""
                    company_address = company_address.replace(company_add, "")
                    # print(company_address)
                except Exception as e:
                    print(e)
                    pass
            if company_address.endswith(")"):
                try:
                    company_address = company_address.split("(")[0].strip()
                except Exception as e:
                    print(e)
                    pass
            elif company_address.endswith("）"):
                try:
                    company_address = company_address.split("（")[0].strip()
                except Exception as e:
                    print(e)
                    pass
            else:
                company_address = company_address.strip()
            return company_address


if __name__ == '__main__':
    execute(["scrapy", "crawl", "msf"])
