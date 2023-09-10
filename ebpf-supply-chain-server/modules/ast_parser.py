import ast

from modules.logger import logger


class AstParser(object):
    """
    ast pasre modules
    """
    def __init__(self):
        self.logger = logger
        self.os_check = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(AstParser, cls).__new__(cls)
        return cls.instance


    """
    open file and parse code
    bad case: sys.platform == 'darwin'
    """
    def os_check_parser(self, path) -> None:
        with open(path, "r") as f:
            python_code = f.read()
        f.close()
        parsed_ast = ast.parse(python_code)
        import_package = []
        self.print_node_info(parsed_ast, import_package, "")
        print(import_package)
        print(self.os_check)

    def print_node_info(self, code_node: ast.AST, import_package: list, package_name: str, indent=0):
        if indent == 0:
            package_name = ""
        for field, value in ast.iter_fields(code_node):
            if isinstance(value, ast.AST):
                self.print_node_info(value, import_package, package_name, indent + 2)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.print_node_info(item, import_package, package_name, indent + 2)
            else:
                if code_node.__class__.__name__ == "alias" and field == "name":
                    import_package.append(f"{package_name}.{value}" if package_name != "" else value)
                if code_node.__class__.__name__ == "ImportFrom" and field == "module":
                    package_name = value
                if code_node.__class__.__name__ == "Str" and field == "s" and value == "darwin":
                    self.os_check = True


if __name__ == "__main__":
    AstParser().os_check_parser("../test/evil/kwxiaodian_macos_ast_test.py")