# -*- coding: utf-8 -*-
import cpca


class GetRightArea(object):
    def __init__(self, args):
        self.location_str_list = ["{}".format(args)]

    def get_area_name(self):
        df = cpca.transform(self.location_str_list, cut=False, lookahead=12, pos_sensitive=True)
        # print(df)
        province = df.iat[0, 0] if df.iat[0, 0] else ""
        city = df.iat[0, 1] if df.iat[0, 1] else ""
        area = df.iat[0, 2] if df.iat[0, 2] else ""
        low_address = df.iat[0, 3] if df.iat[0, 3] else ""
        if province == city:
            full_address = str(city + area + low_address)
        else:
            full_address = str(province + city + area + low_address)
        return area, full_address


# if __name__ == '__main__':
#     # gra = GetRightArea("河南省郑州市管城回族区锦荣商贸城东区一层六街8086号")
#     gra = GetRightArea("河南省郑州市管城回族区锦荣商贸城东区一层一街9号")
#     gra.get_area_name()
