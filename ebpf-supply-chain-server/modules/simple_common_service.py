import json

import requests
import time
from modules.logger import logger
from database.redis_db import Redis
from lxml import etree
from modules.get_package_version import get_package_version


class SimpleCommonService(object):
    def __init__(self):
        self.redis = Redis()
        self.logger = logger
        self.redis_key = "SIMPLE:PYPI:"
        self.redis_task_set_key = "SIMPLE:TASK:SET"
        self.redis_task_execute_history = "TASK:EXECUTE:HISTORY"

    def get_simple_list(self, simple_url: str) -> object:
        resp = requests.get(simple_url, timeout=5)
        if (resp.status_code != 200):
            self.logger.error(f"mirror:{simple_url} request error:{resp.status_code}")
            return None
        return resp.text

    def do_business(self, simple_html: object, simple_type: str, simple_url: str, is_reverse: bool):
        """
        1、判断是否存在key
        2、存在更新key value写入mirror
        3、不存在写入task队列
        :param simple_html:
        :param simple_type:
        :param simple_url:
        :return:
        """
        is_download = self.redis.get_key_value(key=self.redis_task_execute_history) is not None

        if simple_html is None:
            self.logger.error("simple_html is None")
            return
        root = etree.HTML(simple_html)
        node = root.xpath("//a")

        for i in node:
            logger.info(f"simple_type:{simple_type} package:{i.text}")
            value = self.redis.get_key_value(key=f"{self.redis_key}{i.text}")
            data = {"type": simple_type, "url": simple_url, "create_time": time.time()}
            if value is None:
                max_version = get_package_version(url=simple_url, package_name=i.text, is_download=is_download,
                                                  is_reverse=is_reverse)
                data["version"] = max_version
                self.redis.sadd_set(key=self.redis_task_set_key, value=i.text)
                value = {"data": [data], "type_list": [simple_type]}
            # else:
            #     if simple_type not in value["type_list"]:
            #         max_version = get_package_version(url=simple_url, package_name=i.text, is_download=False)
            #         data["version"] = max_version
            #         value["data"].append(data)
            #         value["type_list"].append(simple_type)
            self.redis.set_key_value(key=f"{self.redis_key}{i.text}", value=json.dumps(value), ex=60 * 60 * 24 * 2)
        self.redis.set_key_value(key=self.redis_task_execute_history, value=str(time.time()), ex=60 * 60 * 24)
