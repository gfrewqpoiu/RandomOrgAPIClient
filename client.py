import httpx
import os
from typing import Tuple


baseurl = "https://api.random.org/json-rpc/2/invoke"
id = 0


def prepare_json(method: str, params: dict) -> Tuple[dict, int]:
    global id
    id += 1
    return {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': id}, id


def _filter(id: int, result: dict) -> dict:
    assert id == result['id']
    if "error" in result.keys():
        raise AttributeError(result["error"]['message'])
    else:
        return result['result']


def check_key(key: str) -> dict:
    data, id = prepare_json('getUsage', {'apiKey': key})
    resp = httpx.post(baseurl, json=data)
    return _filter(id, resp.json())


if __name__ == '__main__':
    if 'RANDOM_ORG_API_KEY' not in os.environ:
        raise EnvironmentError("Plesse specify your Random.org API key in the environment var: RANDOM_ORG_API_KEY")
    key = os.environ['RANDOM_ORG_API_KEY']
    result = check_key(key)
    import pprint
    pprint.pprint(result)