import json

from rule.impl.rule_execute import RuleExecute
from database.mapper import hook_info_mapper
from database.mapper import evil_result_mapper
from modules.utils import get_md5
import re

class DnsBlackRule(RuleExecute):
    """
    根据IP地址黑名单判责
    """

    def __init__(self):
        super().__init__()
        self.target_hook_info_type = "DNS"
        self.rule_name = "dns_black_rule"
        self.score = 100
        self.dns_hook_black_pattern = re.compile(".lol.0day-security.com")

    def do_business(self, package_name: str) -> None:
        try:
            self.logger.info(f"{self.rule_name} packag:{package_name}")
            results = self.redis.get_key_value(
                key=f"{self.hook_info_record_key_prefix}{self.target_hook_info_type}:{package_name}")
            if results is None:
                return
            self.logger.info(f"{self.rule_name} packag:{package_name} result size:{len(results)}")
            for result in results:
                if self.__dns_host_black_list(result):
                    self.logger.info(f"{self.rule_name} packag:{package_name} hit rule")
                    if evil_result_mapper.EvilResult().query_count_by_hash(get_md5(data=json.dumps(result))) > 0:
                        continue
                    result_id = hook_info_mapper.HookInfoDns().query_id_by_hook_info(result)
                    if result_id is None:                                                                    
                        result_id = hook_info_mapper.HookInfoSysExec().insert(result)
                    evil_result_mapper.EvilResult().insert(data=self.transform(data=result, result_id=result_id))
        except Exception as e:
            self.logger.error(f"do_business error:{e}")

    def __dns_host_black_list(self, result: dict) -> bool:
        if result.get("comm", None) is None or result.get("host", None) is None:
                return False
        host = result.get("host", "")
        if self.dns_hook_black_pattern.search(result.get("host", "")):
            return True
        return False

    def transform(self, data: dict, result_id: int) -> dict:
        return {
            "hook_type": self.target_hook_info_type.lower(),
            "hook_id": result_id,
            "rule_name": self.rule_name,
            "package": data.get("package", ""),
            "version": data.get("version", ""),
            "score": self.score,
            "hash": get_md5(data=json.dumps(data))
        }
