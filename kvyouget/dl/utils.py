import json
from collections import namedtuple
from contextlib import redirect_stdout
from io import StringIO
from typing import Dict, Optional
import re

from you_get.common import any_download

ITag = namedtuple("ITag", "itag, container, quality, size, size_mb, x, y")
Result = namedtuple("Result", "title, itags")

xy_re = re.compile(r"([\d]{3,4})(?:x)([\d]{3,4})")

def bytes_to_mb(n_bytes: int) -> str:
    return f"{n_bytes / (1024 ** 2) :.1f} MB"

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
    itags = [i for i in itags if i.x > 0 and i.y > 0]

    return Result(title=title, itags=itags)

def download_url(url: str, itag: int, output_dir: Optional[str], on_complete: callable):
    s = StringIO()
    with redirect_stdout(s):
        any_download(url, stream_id=itag, output_dir=output_dir, merge=True)
    on_complete()



def _parse_itag(itag: Dict) -> ITag:
    itag_id = itag["itag"]
    itag_quality = itag["quality"]
    container = itag["container"]
    size = itag.get("size", 0)
    size_mb = bytes_to_mb(size)
    xy_size = xy_re.search(itag_quality)
    if not xy_size:
        x, y, = 0, 0
    else:
        x, y = [int(i) for i in xy_size.groups()]
    return ITag(itag=itag_id, container=container, quality=itag_quality, size=size, size_mb=size_mb, x=x, y=y)
