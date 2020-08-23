from collections import namedtuple
from typing import Dict

from you_get.common import any_download

ITag = namedtuple("ITag", "itag, container, quality, size")
Result = namedtuple("Result", "title, itags")


def get_url_options(url: str) -> Result:
    url_options = any_download(url, info_only=True, json_output=True)
    title = url_options["title"]
    itags = []
    for itag, data in url_options['streams'].items():
        itags.append(_parse_itag(data))

    return Result(title=title, itags=itags)


def _parse_itag(itag: Dict) -> ITag:
    itag_id = itag["itag"]
    itag_quality = itag["quality"]
    container = itag["container"]
    size = itag.get("size", 0)
    return ITag(itag=itag_id, container=container, quality=itag_quality, size=size)
