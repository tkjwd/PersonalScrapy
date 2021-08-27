import pickle
import redis
# import traceback
# from pymongo import MongoClient


class RedisHelp(object):
    def __init__(self, host=None, port=None, pwd=None, db=None, des=None):
        self.pool = redis.ConnectionPool(host=host, port=port, password=pwd, db=db,
                                         decode_responses=des)
        self.Rs_ = redis.Redis(connection_pool=self.pool)
        # self.conn = MongoClient(host=DB_IP, port=27017)
        # self.error_db = self.conn['Redis_error_db']

    # def set_object(self, text, teble='Mt_discount:dict'):
    #     _text = pickle.dumps(text)
    #     try:
    #         self._Rs.rpush(teble, _text)
    #     except Exception as e:
    #         print(e)
    #         # self.error_db['error'].insert_one(traceback.format_exc())
    #         print(traceback.format_exc())
    #         pass
    #     return 'OK!'
    #
    # def get_object(self, list_name='Mt_discount:dict', is_block=False):
    #     if is_block:
    #         _text = self._Rs.brpop(list_name)[1]
    #     else:
    #         _text = self._Rs.rpop(list_name)
    #     if _text:
    #         pk_text = pickle.loads(_text)
    #         return pk_text

    def _close(self):
        self.pool.disconnect()
        # self.conn.close()

#
# if __name__ == '__main__':
#     pass
