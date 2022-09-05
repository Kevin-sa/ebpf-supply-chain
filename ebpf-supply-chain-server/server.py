from flask import request
from config.setting import app
from database.mapper import hook_info_mapper

from modules.package_task_service import PackageTaskService
from database.cache.hook_info_cache import HookInfoCache
import re

@app.route("/")
def health():
    return "ok!"


@app.route("/hook/socket", methods=['POST'])
def hook_info_record():
    """
    结果体
    {"type": "PYPI", "package": "requests", "version": 1.0, "describe": "", "score": "execute", "comm": "pypi", "daddr": "", "dport": 0}
    :return:
    """
    data = request.get_json()
    if data.get("daddr", "") != "127.0.0.1" and data.get("package", "") != "":
        hook_info_mapper.HookInfoSocket().insert(data)
        HookInfoCache().socket_hook_info_cache(data)
    return {
        "result": 1,
        "error_msg": "success"
    }


@app.route("/hook/sys/open", methods=['POST'])
def sys_open_hook_info_record():
    """
    结果体
    {"type": "PYPI", "package": "requests", "version": 1.0, "describe": "", "score": "execute", "comm": "pypi", "filename": ""}
    :return:
    """
    data = request.get_json()
    comm_black_list = ["redis-server", "node", "vmtoolsd", "ps", "sleep", "sed", "cpuUsage.sh"]
    comm = data.get("comm", "").replace("\u0000", "")
    if comm not in comm_black_list and data.get("package", "") != "":
        data["comm"] = comm
        hook_info_mapper.HookInfoSysOpen().insert(data)
        # HookInfoCache().sys_open_hook_info_cache(data)
    return {
        "result": 1,
        "error_msg": "success"
    }


@app.route("/hook/sys/write", methods=['POST'])
def sys_write_hook_info_record():
    """
    结果体
    {"type": "PYPI", "package": "requests", "version": 1.0, "describe": "", "score": "execute", "comm": "pypi", "filename": ""}
    :return:
    """
    data = request.get_json()
    comm_black_list = ["redis-server", "node", "sshd", "gmain", "connection", "containerd-shim", "dockerd", "docker",
                       "cpuUsage.sh", "containerd", "NetworkManager"]
    comm = data.get("comm", "").replace("\u0000", "")
    if comm not in comm_black_list and data.get("package", "") != "":
        data["comm"] = comm
        hook_info_mapper.HookInfoSysWrite().insert(data)
        # HookInfoCache().sys_write_hook_info_cache(data)
    return {
        "result": 1,
        "error_msg": "success"
    }

@app.route("/hook/sys/exec", methods=['POST'])
def sys_exec_hook_info_record():
    """
    结果体
    {"type": "PYPI", "package": "requests", "version": 1.0, "describe": "", "score": "execute", "comm": "pypi", "filename": ""}
    :return:
    """
    data = request.get_json()
    comm_black_list = ["node"]
    filename_pattern = "vscode-server"
    if not re.search(filename_pattern, data.get("filename", "")) and data.get("package", "") != "" and data.get("comm") not in comm_black_list:
        hook_info_mapper.HookInfoSysExec().insert(data)
        HookInfoCache().sys_exec_hook_info_cache(data)

    return {
        "result": 1,
        "error_msg": "success"
    }


@app.route("/task/pypi", methods=['GET'])
def get_pypi_task_info():
    handler = PackageTaskService()
    return handler.get_pypi_package_task_info()


@app.route("/task/npm", methods=['GET'])
def get_npm_task_info():
    return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
