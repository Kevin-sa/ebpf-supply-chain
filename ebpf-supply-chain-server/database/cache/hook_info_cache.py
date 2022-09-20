from modules.logger import logger
from database.redis_db import Redis
import time
import json


class HookInfoCache(object):
    def __init__(self):
        self.redis = Redis()
        self.logger = logger
        self.hook_info_zset_key_prefix = "HOOK:INFO:ZSET"
        self.hook_info_record_key_prefix = "HOOK:INFO:RECORD:"
        self.hook_info_recode_expire = 3600
        self.hook_info_recode_delay = 300
        self.sys_write_comm_black_list = ["gnome-terminal-", "redis-cli", "redis-server", "node", "sshd", "gmain",
                                          "connection", "containerd-shim", "dockerd", "docker", "cpuUsage.sh",
                                          "containerd", "NetworkManager", "supervisord"]
        self.sys_open_comm_black_list = ["redis-server", "node", "vmtoolsd", "ps", "sleep", "sed", "cpuUsage.sh"]

    def empty_zset_by_score(self, end_time: int) -> None:
        return self.redis.z_rem_range_by_score(key=self.hook_info_zset_key_prefix,
                                         min_score=0,
                                         max_score=end_time - self.hook_info_recode_delay)

    def get_hook_info_count(self, end_time: int) -> int:
        return self.redis.zset_count(key=self.hook_info_zset_key_prefix,
                                         min_score=0,
                                         max_score=end_time - self.hook_info_recode_delay)

    def get_hook_info(self, end_time: int) -> list:
        result = []
        result = self.redis.zset_range_by_source(key=self.hook_info_zset_key_prefix,
                                                min_score=0,
                                                max_score=end_time - self.hook_info_recode_delay)
        return result

    def socket_hook_info_cache(self, data: dict) -> None:
        try:
            package_name = data.get("package", "")

            if package_name == "" and data.get("daddr", "") == "127.0.0.1":
                return
            self.comm_hook_info_cache(data=data, type="SOCKET", package_name=package_name)
        except Exception as e:
            self.logger.error(f"socket_hook_info_cache error:{e}")

    def sys_open_hook_info_cache(self, data: dict) -> None:
        try:
            package_name = data.get("package", "")
            if package_name == "" and data.get("comm", "") in self.sys_open_comm_black_list:
                return
            self.comm_hook_info_cache(data=data, type="SYSOPEN", package_name=package_name)
        except Exception as e:
            self.logger.error(f"sys_open_hook_info_cache error:{e}")

    def sys_write_hook_info_cache(self, data: dict) -> None:
        try:
            package_name = data.get("package", "")
            if package_name == "" and data.get("comm", "") in self.sys_write_comm_black_list:
                return
            self.comm_hook_info_cache(data=data, type="SYSWRITE", package_name=package_name)
        except Exception as e:
            self.logger.error(f"sys_write_hook_info_cache error:{e}")

    def sys_exec_hook_info_cache(self, data: dict) -> None:
        try:
            package_name = data.get("package", "")
            self.comm_hook_info_cache(data=data, type="SYSEXEC", package_name=package_name)
        except Exception as e:
            self.logger.error(f"sys_write_hook_info_cache error:{e}")


    def dns_hook_info_cache(self, data: dict) -> None:
        try:
            package_name = data.get("package", "")
            self.comm_hook_info_cache(data=data, type="DNS", package_name=package_name)
        except Exception as e:
            self.logger.error(f"sys_write_hook_info_cache error:{e}")

    def comm_hook_info_cache(self, data: dict, type: str, package_name: str) -> None:
        try:
            self.redis.zset_add(key=self.hook_info_zset_key_prefix,
                                score=int(time.time()),
                                value=package_name)
            redis_key = f"{self.hook_info_record_key_prefix}{type}:{package_name}"

            self.logger.info(f"type:{type} redis key:{redis_key}")

            hook_info_recode = self.redis.get_key_value(key=redis_key)

            if hook_info_recode is None:
                self.redis.set_key_value(key=redis_key, value=json.dumps([data]),
                                         ex=self.hook_info_recode_expire)
            else:
                hook_info_recode.append(data)
                self.redis.set_key_value(key=redis_key, value=json.dumps(hook_info_recode),
                                         ex=self.hook_info_recode_expire)
        except Exception as e:
            self.logger.error(f"comm_hook_info_cache error:{e}")