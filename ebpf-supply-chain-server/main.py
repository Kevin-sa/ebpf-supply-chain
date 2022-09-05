import asyncio
import threading

from mirror.cloud_tencent_com import CloudTencent
from mirror.doubanio_com import DouBanio
from mirror.pypi_org import PypiOrg
from mirror.tuna_tsinghua_edu import TunaTsinghuaEdu


# def worker(func) -> None:
#     """
#     开始调度后台任务
#     :return: 无
#     """
#     asyncio.set_event_loop(asyncio.new_event_loop())
#     loop = asyncio.get_event_loop()
#     # IAST扫描任务消费者启动器
#     loop.run_until_complete(func())
#     loop.close()


def main():
    mirror_executor = [CloudTencent().execute, TunaTsinghuaEdu().execute, DouBanio().execute, PypiOrg().execute]
    # for execute in mirror_executor:
    #     execute()
    work_thread_list = []

    for func in mirror_executor:
        try:
            # thread = threading.Thread(target=worker(), args=(func(),))
            thread = threading.Thread(target=func, args=())
            thread.setDaemon(True)
            work_thread_list.append(thread)
        except Exception:
            continue

    for thread in work_thread_list:
        thread.start()

    for thread in work_thread_list:
        thread.join()

    # tasks = []
    # for executor in mirror_executor:
    #     tasks.append(asyncio.ensure_future(executor))
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()


if __name__ == '__main__':
    main()
