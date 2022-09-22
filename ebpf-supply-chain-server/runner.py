import imp
import threading
import time
from database.cache.hook_info_cache import HookInfoCache
from modules.logger import logger
from rule.socket_black_address_rule import ScoketBlackAddressRule
from rule.socket_black_port_rule import ScoketBlackPortRule
from rule.socket_address_rare_rule import ScoketAddressRareRule
from rule.sys_open_file_black_rule import SysOpenFileBlackRule
from rule.exec_black_rule import ExecBlackRule
from rule.dns_black_rule import DnsBlackRule

def main():
    """
    延迟从zset中获取hook_info
    根据预定规则做是否恶意package判责
    todo: thread_pool 处理
    """
    # thread_pool = ThreadPoolExecutor(10)
    rule_service = [ScoketBlackAddressRule, ScoketBlackPortRule, ScoketAddressRareRule, ExecBlackRule, SysOpenFileBlackRule,
                    DnsBlackRule]

    hook_info_cache = HookInfoCache()

    while True:
        end_time = int(time.time())
        total = hook_info_cache.get_hook_info_count(end_time=end_time)
        if total == 0:
            logger.info("get_hook_info_count total is 0")
            time.sleep(5)
            continue
        logger.info(f"get_hook_info_count total is:{total}")

        results = hook_info_cache.get_hook_info(end_time=end_time)
        logger.info(f"get_hook_info result size:{len(results)}")

        for result in results:
            work_thread_list = []
            for service in rule_service:
                try:
                    thread = threading.Thread(target=service().execute, args=(result,))
                    thread.setDaemon(True)
                    work_thread_list.append(thread)
                except Exception:
                    continue
            for thread in work_thread_list:
                thread.start()

            for thread in work_thread_list:
                thread.join()
        hook_info_cache.empty_zset_by_score(end_time=end_time)


if __name__ == '__main__':
    main()
