import asyncio
import aiohttp
from modules.logger import logger
import requests
from lxml import etree
import os
import time
from aiohttp import TCPConnector


def get_package_version(url: str, package_name: str, is_download: bool, is_reverse: bool) -> str:
    """
    根据package及mirror获取对应版本
    :return:
    """
    try:
        resp = requests.get(url=f"{url}{package_name}/", timeout=5)
        version_list = []
        file_list = {}

        root = etree.HTML(resp.text)
        node = root.xpath("//a")

        if is_reverse:
            node = node[::-1]

        for i in node:
            version = i.text.split("-")[1].replace(".tar.gz", "")
            version_list.append(version)
            file_list[version] = {"text": i.text, "href": i.attrib.get("href", "")}

        if len(version_list) == 0:
            raise Exception(f"package:{package_name} version list is Null")

        max_version = max(version_list)

        if is_download:
            download_package_file(url=f"{url}{package_name}",
                                  file_url=file_list.get(max_version, {}).get("href", ""),
                                  filename=file_list.get(max_version, {}).get("text", ""))
        return max_version
    except Exception as error:
        logger.error(f"url:{url} package:{package_name} error:{error}")
        return ""


def download_package_file(url: str, file_url: str, filename: str) -> None:
    """
    根据最大版本下载文件
    """
    try:
        content = requests.get(url=f"{url}/{file_url}").content

        download_path = f"/home/kevinsa/go/src/github.com/kevinsa/tmp_package/{time.strftime('%Y-%m-%d', time.localtime())}"

        # content = await __get_content(url=f"{url}/{file_url}")
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        file_path = f"{download_path}/{filename}"
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as error:
        logger.error(f"download_package_file error:{error}")


async def __get_content(url: str) -> bytes:
    async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        response = await session.get(url)
    content = await response.read()
    return content


if __name__ == "__main__":
    ""
