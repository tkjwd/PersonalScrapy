from scrapy.cmdline import execute
import os, datetime, time
from multiprocessing import Process


def run_work():
    while True:
        result = True
        while result:  # 操作cmd指定参数执行爬虫,并指定存入的数据表
            cmd = 'scrapy crawl haozu'
            # cmd = 'scrapy crawl haozu -s JOBDIR=crawls/haozu-1'
            os.system(cmd)

            # cmd_1 = 'scrapy crawl TarGet_Spider -a MYSQL_TABLENAME={0}' \
            #         ' -a data_expiration={1}' \
            #         ' -a status_list=status:3,status:4' \
            #         ' -s MYSQL_DBNAME=upwork'.format(table_l, data_expiration)
            # os.system(cmd_1)
            #
            # cmd_2 = 'scrapy crawl TarGet_Spider -a MYSQL_TABLENAME={0}' \
            #         ' -a data_expiration={1}' \
            #         ' -a status_list=status:1' \
            #         ' -s MYSQL_DBNAME=upwork'.format(table_l, data_expiration)
            # if 0<=now_hours<2:
            #     sleep_to_date(2)
            #     break
            # os.system(cmd_2)

            with open('working.txt', 'a') as f:  # 生成运行日志
                f.write('start data:%s\n' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    run_work()
