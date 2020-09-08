import json
from collections import namedtuple
from contextlib import redirect_stdout
from io import StringIO
from typing import Dict
import re

from you_get.common import any_download

ITag = namedtuple("ITag", "itag, container, quality, size, x, y")
Result = namedtuple("Result", "title, itags")

xy_re = re.compile(r"([\d]{3,4})(?:x)([\d]{3,4})")

def get_url_options(url: str) -> Result:
    s = StringIO()
    with redirect_stdout(s):
        any_download(url, info_only=True, json_output=True)
    url_options = json.loads(s.getvalue())
    title = url_options["title"]
    itags = []
    for itag, data in url_options['streams'].items():
        itags.append(_parse_itag(data))

    itags.sort(key=lambda i: i.x * i.y, reverse=True)

    return Result(title=title, itags=itags)


def _parse_itag(itag: Dict) -> ITag:
    itag_id = itag["itag"]
    itag_quality = itag["quality"]
    container = itag["container"]
    size = itag.get("size", 0)
    xy_size = xy_re.search(itag_quality)
    if not xy_size:
        x, y, = 0, 0
    else:
        x, y = [int(i) for i in xy_size.groups()]
    return ITag(itag=itag_id, container=container, quality=itag_quality, size=size, x=x, y=y)
