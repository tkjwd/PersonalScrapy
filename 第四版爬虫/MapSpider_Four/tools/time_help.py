# -*- coding: utf-8 -*-
import time
# from loguru import logger


class StopSpider(object):
    def __init__(self):
        # self.lg = logger
        self.Turn_Time = "24:00:00"

    def get_sleep_time(self):
        turn_time_s = int(self.Turn_Time.split(":")[0]) * 60 * 60 \
                      + int(self.Turn_Time.split(":")[1]) * 60 \
                      + int(self.Turn_Time.split(":")[2])
        # self.lg.info("[turn_time_s]: {}".format(turn_time_s))
        localtime = time.localtime(time.time())
        now_time_hms = time.strftime('%H:%M:%S', localtime)
        now_time_s = int(now_time_hms.split(":")[0]) * 60 * 60 \
                     + int(now_time_hms.split(":")[1]) * 60 \
                     + int(now_time_hms.split(":")[2])
        # self.lg.info("[now_time_s]: {}".format(now_time_s))
        # should_sleep_time = int(turn_time_s) - int(now_time_s) + 600
        should_sleep_time = 600
        # self.lg.info("[should_sleep_time]: {}".format(should_sleep_time))
        return should_sleep_time
