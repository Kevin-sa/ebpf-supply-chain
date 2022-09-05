import json

from rule.impl.rule_execute import RuleExecute
from database.mapper import hook_info_mapper
from database.mapper import evil_result_mapper
from modules.utils import get_md5


class ExecBlackRule(RuleExecute):
    """
    根据IP地址黑名单判责
    """

    def __init__(self):
        super().__init__()
        self.target_hook_info_type = "SYSEXEC"
        self.rule_name = "exec_black_rule"
        self.score = 60
        self.exec_black_list = [{"comm": "python3", "filename": "/bin/sh"}]

    def do_business(self, package_name: str) -> None:
        try:
            self.logger.info(f"{self.rule_name} packag:{package_name}")
            results = self.redis.get_key_value(
                key=f"{self.hook_info_record_key_prefix}{self.target_hook_info_type}:{package_name}")
            if results is None:
                return
            self.logger.info(f"{self.rule_name} packag:{package_name} result size:{len(results)}")
            for result in results:
                if self.__exec_black_list(result):
                    if evil_result_mapper.EvilResult().query_count_by_hash(get_md5(data=json.dumps(result))) > 0:
                        continue
                    result_id = hook_info_mapper.HookInfoSysExec().query_id_by_hook_info(result)
                    if result_id is None:                                                                    
                        result_id = hook_info_mapper.HookInfoSysExec().insert(result)
                    evil_result_mapper.EvilResult().insert(data=self.transform(data=result, result_id=result_id))
        except Exception as e:
            self.logger.error(f"do_business error:{e}")

    def __exec_black_list(self, result: dict) -> bool:
        for exec_black_word in self.exec_black_list:
            if result.get("comm", None) is None or result.get("filename", None) is None:
                continue
            if result.get("comm", "") == exec_black_word.get("comm", "") and result.get("filename", ) == exec_black_word.get("filename", ""):
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
