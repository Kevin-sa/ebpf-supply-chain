import logging
import json
from redis import StrictRedis


def redis_wrapper(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.redis = self.redis_client
        return func(*args, **kwargs)

    return wrapper


class Redis(object):
    try:
        host = "127.0.0.1"
        port = "6379"
        db = 2
        redis_client: StrictRedis = StrictRedis(
            host=host,
            port=port,
            db=db,
            socket_timeout=5.0,
            socket_connect_timeout=8.0,
            max_connections=8192,
        )
    except Exception as e:
        logging.error(f"redis connect error:{e}")

    def __init__(self):
        super().__init__()
        self.redis = self.redis_client

    @redis_wrapper
    def get_key_value(self, key: str) -> dict:
        try:
            value = self.redis.get(name=key)
            if value is None:
                return None
            if isinstance(value, bytes):
                value = value.decode("UTF-8")
            return json.loads(value)
        except Exception as e:
            logging.error(f"get value error:{e}")

    @redis_wrapper
    def set_key_value(self, key: str, value: str, ex=None, px=None, nx=False, xx=False) -> bool:
        try:
            return self.redis.set(name=key, value=str(value), ex=ex, px=px, nx=nx, xx=xx)
        except Exception as e:
            logging.error(f"set key:{key} value error:{e}")
            return False

    @redis_wrapper
    def sdiffstore_set(self, dest: str, key1: str, key2: str) -> int:
        try:
            return self.redis.sdiffstore(dest=dest, keys=[key1, key2])
        except Exception as e:
            logging.error(f"sdiffstore error:{e}")
            return 0

    @redis_wrapper
    def sadd_set(self, key: str, value: str) -> int:
        try:
            return self.redis.sadd(key, value)
        except Exception as e:
            logging.error(f"sadd_set error:{e}")
            return 0

    @redis_wrapper
    def set_smembers(self, key: str) -> list:
        try:
            result_set = self.redis.smembers(name=key)
            result = []
            for i in result_set:
                result.append(i.decode("UTF-8"))
            return result
        except Exception as e:
            logging.error(f"set_smembers error:{e}")
            return []

    @redis_wrapper
    def set_sunionstore(self, dest: str, keys: list) -> int:
        try:
            return self.redis.sunionstore(dest=dest, keys=keys)
        except Exception as e:
            logging.error(f"set_sunionstore error:{e}")
            return 0

    @redis_wrapper
    def del_key(self, key: str) -> None:
        try:
            self.redis.delete(key)
        except Exception as e:
            logging.error(f"del_key error:{e}")

    @redis_wrapper
    def set_pop(self, key: str) -> str:
        try:
            result = self.redis.spop(name=key, count=1)
            if len(result) != 0:
                return result[0].decode("UTF-8")
            return ""
        except Exception as e:
            logging.error(f"set_pop error:{e}")

    @redis_wrapper
    def zset_add(self, key: str, score: int, value: str) -> None:
        try:
            self.redis.zadd(name=key, mapping={value: score})
        except Exception as e:
            logging.error(f"zset_add error:{e}")


    @redis_wrapper
    def zset_count(self, key: str, min_score: int, max_score: int) -> int:
        result = 0
        try:
            return self.redis.zcount(name=key, min=min_score, max=max_score)
        except Exception as e:
            logging.error(f"zset_count error:{e}")
        return 0

    @redis_wrapper
    def zset_range_by_source(self, key: str, min_score: int, max_score: int) -> list:
        result = []
        try:
            data = self.redis.zrangebyscore(name=key, min=min_score, max=max_score)
            for i in data:
                if isinstance(i, bytes):
                    result.append(i.decode("UTF-8"))
                else:
                    result.append(i)
        except Exception as e:
            logging.error(f"zset_range_by_source error:{e}")
        return result


    @redis_wrapper
    def z_rem_range_by_score(self, key: str, min_score: int, max_score: int) -> None:
        try:
            self.redis.zremrangebyscore(name=key, min=min_score, max=max_score)
        except Exception as e:
            logging.error(f"z_rem_range_by_lex error:{e}")

if __name__ == "__main__":
    print(Redis().get_key_value("SIMPLE:TASK:SET"))
