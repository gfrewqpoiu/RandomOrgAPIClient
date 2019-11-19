import httpx
import os
import asyncio
import warnings
from typing import Dict, Any

base_url = "https://api.random.org/json-rpc/2/invoke"


def _filter(id: int, result: Dict[str, Any]) -> Dict[str, Any]:
    assert id == result['id']  # Check that the ID of the result is what we expect.
    if "error" in result.keys():
        raise AttributeError(result["error"]['message'])
    else:
        return result['result']


class RandomOrgClient:
    def __init__(self, apiKey: str):
        self.apiKey = apiKey
        self.id = 0
        self.AsyncClient = httpx.AsyncClient()
        try:
            self.status = self.getUsage()['status']
        except AttributeError:
            raise AttributeError("The provided API Key is not valid.")
        if self.status == "stopped":
            raise AttributeError("The provided API Key is stopped.")
        elif self.status != "running":
            warnings.warn("The provided API Key is in a unknown state.")

    def getUsage(self) -> dict:
        data = self._prepare_json('getUsage', {})
        resp = httpx.post(base_url, json=data)
        return _filter(self.id, resp.json())

    async def generateIntegers(self, amount: int, min: int, max: int, with_replacement: bool = True, base: int = 10):
        request_json = self._prepare_json("generateIntegers",
                                         {'n': amount, 'min': min, 'max': max,
                                          'replacement': with_replacement, 'base': base})
        resp = await self.AsyncClient.post(base_url, json=request_json)
        resp = _filter(self.id, resp.json())
        return resp['random']['data']

    def _prepare_json(self, method: str, params: dict) -> Dict[str, Any]:
        self.id += 1
        params.update({'apiKey': self.apiKey})
        return {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': self.id}


async def main():
    if 'RANDOM_ORG_API_KEY' not in os.environ:
        raise EnvironmentError("Plesse specify your Random.org API key in the environment var: RANDOM_ORG_API_KEY")
    client = RandomOrgClient(os.environ['RANDOM_ORG_API_KEY'])
    import pprint
    pprint.pprint(client.status)
    integers_res = await client.generateIntegers(10, 1, 6)
    pprint.pprint(integers_res)


if __name__ == '__main__':
    asyncio.run(main())
