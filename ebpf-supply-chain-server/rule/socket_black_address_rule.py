import json

from rule.impl.rule_execute import RuleExecute
from database.mapper import hook_info_mapper
from database.mapper import evil_result_mapper
from modules.utils import get_md5


class ScoketBlackAddressRule(RuleExecute):
    """
    根据IP地址黑名单判责
    """

    def __init__(self):
        super().__init__()
        self.target_hook_info_type = "SOCKET"
        self.rule_name = "socket_black_address"
        self.score = 100
        self.black_address_list = ["175.24.100.2", "101.32.99.28"]

    def do_business(self, package_name: str) -> None:
        try:
            self.logger.info(f"{self.rule_name} packag:{package_name}")
            results = self.redis.get_key_value(
                key=f"{self.hook_info_record_key_prefix}{self.target_hook_info_type}:{package_name}")
            if results is None:
                return
            self.logger.info(f"{self.rule_name} result size:{len(results)}")
            for result in results:
                self.logger.info(f"{self.rule_name} result port:{result.get('daddr', '')}")
                if result.get("daddr", "") in self.black_address_list:
                    if evil_result_mapper.EvilResult().query_count_by_hash(get_md5(data=json.dumps(result))) > 0:
                        continue
                    result_id = hook_info_mapper.HookInfoSocket().query_id_by_hook_info(package=package_name, version=result.get("version", ""),
                                                                                        d_addr=result.get("daddr", ""), d_port=result.get("dport", 0))
                    if result_id is None:                                                                    
                        result_id = hook_info_mapper.HookInfoSocket().insert(result)
                    evil_result_mapper.EvilResult().insert(data=self.transform(data=result, result_id=result_id))
        except Exception as e:
            self.logger.error(f"do_business error:{e}")

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
