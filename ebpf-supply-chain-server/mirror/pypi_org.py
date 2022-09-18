from mirror.impl.mirror_execute import MirrorExecute
from modules.simple_common_service import SimpleCommonService


class PypiOrg(MirrorExecute):
    def __init__(self):
        super().__init__()
        self.simple_url = "https://pypi.org/simple/"
        self.redis_key_prefix = "PYPI:"
        self.mirror_execute = SimpleCommonService()
        self.simple_diff = False
        self.is_reverse = False

    def do_business(self):
        simple_html = self.mirror_execute.get_simple_list(self.simple_url)
        self.mirror_execute.do_business(simple_html=simple_html, simple_type=self.redis_key_prefix,
                                        simple_url=self.simple_url, is_reverse=self.is_reverse)
        if self.simple_diff is False:
            return


if __name__ == "__main__":
    PypiOrg().execute()
