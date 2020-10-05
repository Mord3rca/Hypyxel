import requests
import json


class Api:

    def __init__(self, key, host="https://api.hypixel.net"):
        self._session = requests.Session()
        self._host = host
        self._key = key

    def get(self, path: str, params: dict = None) -> json:
        """
        Perform a GET request on the REST API

        :param path: REST endpoint to GET
        :param params: Parameters needed for the request
        :return: Json object obtain from the request response
        """
        if type(path) is not str:
            raise ValueError("get(): path should be a string")

        if params and type(params) is not dict:
            raise ValueError("get(): params should be a dictionary")

        if not params:
            params = {}
        params["key"] = self._key

        r = self._session.get(f"{self._host}{path}", params=params)
        if r.status_code != 200:
            raise Exception("get(): Response is not 200")

        return json.loads(r.text)
