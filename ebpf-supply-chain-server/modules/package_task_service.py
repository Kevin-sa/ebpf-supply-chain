from database.redis_db import Redis
from urllib.parse import urlparse
from modules.logger import logger


class PackageTaskService(object):
    def __init__(self):
        self.redis = Redis()
        self.redis_key = "SIMPLE:PYPI:"
        self.redis_task_set_key = "SIMPLE:TASK:SET"
        self.logger = logger

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PackageTaskService, cls).__new__(cls)
        return cls.instance

    def get_pypi_package_task_info(self) -> dict:
        """
        从set中获取一个package包，暂时没有考虑version问题，version由端上ebpf获取
        :return:
        """
        message = {"package": "", "mirror": "", "host": "", "version": ""}
        try:
            package_name = self.redis.set_pop(key=self.redis_task_set_key)
            # package_name = "requests"
            self.logger.info(f"pop pypi task:{package_name}")
            message = {"package": package_name, "mirror": "", "version": ""}
            package_value = self.redis.get_key_value(key=f"{self.redis_key}{package_name}")
            if package_value is not None:
                data = package_value.get("data", [])
                mirror = data[0].get("url", "")
                message["mirror"] = mirror
                message["version"] = data[0].get("version", "")
                message["host"] = urlparse(mirror).hostname
                # message["version"] = get_package_version(mirror, package_name)
        except Exception as error:
            self.logger.error(f"get_pypi_package_task_info error:{error}")
        return {
            "result": 1,
            "error_msg": "success",
            "data": message
        }
