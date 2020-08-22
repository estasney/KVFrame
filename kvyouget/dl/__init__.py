from kvyouget.dl.utils import parse_youget, run_process

def get_url_itags(url):
    response = run_process("you-get", "-i", url)
    results = parse_youget(response)
    return results





