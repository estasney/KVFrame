import re
import subprocess
from collections import namedtuple
from functools import partial
from typing import Optional


def _take_ntnh(result, n):
    return result[n]

def _take_quality(result):
    if not result[-1]:
        return result[-2]
    return result[-1]


def _replace_paren(result):
    return result.replace("(", "").replace(")", "")


def _strip(result):
    return result.strip()


def _apply(result, funcs):
    for func in funcs:
        result = func(result)
    return result


_take0 = partial(_take_ntnh, n=0)
_take_last = partial(_take_ntnh, n=-1)
dash_re = re.compile(r"(?:DASH).+")
title_re = re.compile(r"(?:title: +)(.+)")
title_op = partial(_apply, funcs=[_take0, _strip])
title_method = title_re.findall
line_split = re.compile(r"\r?\n\r?\n")
itag_re = re.compile(r"(?<=- itag:) +(\d+)")
itag_op = partial(_apply, funcs=[_take0, _strip])
itag_method = itag_re.findall
container_re = re.compile(r"(?<=container:) +(\w+)")
container_op = partial(_apply, funcs=[_take0, _strip])
container_method = container_re.findall
quality_re = re.compile(r"(?:quality: +)(([\dx]+)|([\d\w]+))(?(2) (\([\dp]+\)|))")
quality_op = partial(_apply, funcs=[_take_quality, _strip, _replace_paren])
quality_method = lambda x: quality_re.search(x).groups()
size_re = re.compile(r"(?:size: +)([\d.]+ \w{2,4})")
size_op = partial(_apply, funcs=[_take0, _strip])
size_method = size_re.findall
ITag = namedtuple("ITag", "itag, container, quality, size")
Result = namedtuple("Result", "title, itags")


def _try_regex_op(s, pattern_method, op, default=None):
    try:
        result = pattern_method(s)
        result = op(result)
        return result
    except Exception as e:
        if default is False:
            raise e
        else:
            return default


def parse_youget(response: str) -> Optional[Result]:
    options = []
    try:
        meta, itags = dash_re.split(response)
    except ValueError:
        return None

    title = _try_regex_op(meta, title_method, title_op, default="Unknown Title")
    for chunk in line_split.split(itags):
        chunk_itag = _try_regex_op(chunk, itag_method, itag_op)
        if not chunk_itag:
            print(f"Error Getting itag")
            print(chunk)
            continue
        chunk_container = _try_regex_op(chunk, container_method, container_op)
        if not chunk_container:
            print(f"Error Getting Chunk Container")
            print(chunk)
        chunk_quality = _try_regex_op(chunk, quality_method, quality_op)
        if not chunk_quality:
            print(f"Error Getting Chunk Quality")
            print(chunk)
        chunk_size = _try_regex_op(chunk, size_method, size_op)
        if not chunk_size:
            print(f"Error Getting Chunk Size")
            print(chunk)

        options.append(ITag(itag=chunk_itag, container=chunk_container, quality=chunk_quality, size=chunk_size))
    return Result(title=title, itags=options)


def run_process(cmd: str, *args) -> str:
    """
    Convenience method for subprocess

    Parameters
    ----------
    cmd
        Command
    args
        Arguments

    Returns
    -------
    str
        The stdout captured
    """
    args = [cmd] + list(args)
    with subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True) as p:
        result, _ = p.communicate()
    return result.decode().strip()