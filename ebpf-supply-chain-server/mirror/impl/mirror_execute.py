from abc import ABCMeta, abstractmethod

from modules.simple_common_service import SimpleCommonService


class MirrorExecute(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.mirror_execute = SimpleCommonService()

    @abstractmethod
    def do_business(self) -> None:
        return

    def execute(self) -> None:
        self.do_business()
