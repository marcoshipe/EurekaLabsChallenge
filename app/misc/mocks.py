from typing import Optional
from requests import JSONDecodeError


class MockRequestsResponse:
    def __init__(self, status_code: int, json_data: Optional[dict] = None, raise_json_exception: bool = False):
        self.status_code = status_code
        if json_data is None:
            self.json_data = {}
        else:
            self.json_data = json_data
        self.raise_json_exception = raise_json_exception

    def json(self):
        if self.raise_json_exception:
            raise JSONDecodeError('msg', 'doc', 1)
        return self.json_data
