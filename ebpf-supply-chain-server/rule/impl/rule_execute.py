from abc import ABCMeta, abstractmethod
from modules.logger import logger
from database.redis_db import Redis

class RuleExecute(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.hook_info_record_key_prefix = "HOOK:INFO:RECORD:"
        self.redis = Redis()
        self.logger = logger

    @abstractmethod
    def do_business(self, package: str) -> None:
        return

    def execute(self, package: str) -> None:
        self.do_business(package)