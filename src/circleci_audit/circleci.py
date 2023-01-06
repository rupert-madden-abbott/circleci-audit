import http.client
import json
from http.client import HTTPResponse
from typing import TypeVar, List, Callable, Optional, Iterable, Dict, Any


class HttpError(Exception):
    def __init__(self, message: str, response: HTTPResponse):
        super().__init__(message)
        self.response = response


T = TypeVar('T')


class NumberedPageIterator:
    def __init__(self, page_fetcher: Callable[[int], List[T]]):
        self.page_fetcher = page_fetcher
        self.current_page: Optional[List[T]] = []
        self.current_page_number: int = 0
        self.current_item_index: int = 0
        self.fetched_first_page: bool = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.fetched_first_page or self.current_item_index >= len(self.current_page):
            page = self.page_fetcher(self.current_page_number)
            self.current_page = [] if page is None else page
            self.current_item_index = 0
            self.current_page_number += 1
            self.fetched_first_page = True

        if len(self.current_page) == 0:
            raise StopIteration

        item = self.current_page[self.current_item_index]
        self.current_item_index += 1
        return item


class UnnumberedPageIterator:
    def __init__(self, page_fetcher: Callable[[Optional[str]], Dict[str, Any]]):
        self.page_fetcher = page_fetcher
        self.current_page: Optional[List[T]] = []
        self.next_page_token: Optional[str] = None
        self.current_item_index: int = 0
        self.fetched_first_page: bool = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.fetched_first_page or (
                self.current_item_index >= len(self.current_page) and self.next_page_token is not None
        ):
            page = self.page_fetcher(self.next_page_token)
            self.current_item_index = 0
            self.fetched_first_page = True
            self.next_page_token = page.get("next_page_token")
            self.current_page = page.get("items")

        if self.current_item_index >= len(self.current_page):
            raise StopIteration

        item = self.current_page[self.current_item_index]
        self.current_item_index += 1
        return item


class CircleCiClient:
    def __init__(self, token: str):
        self.token = token

    def get(self, url: str, params: Dict[str, str] = None):

        if params is None:
            params = {}

        if len(params) > 0:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            url = f"{url}?{query_string}"

        conn = http.client.HTTPSConnection("circleci.com")
        conn.request(
            method="GET",
            url=url,
            headers={
                'Accept': "application/json",
                'Circle-Token': self.token
            }
        )

        response = conn.getresponse()

        self._raise_for_status(url, response)

        body = response.read().decode("utf-8")
        return json.loads(body)

    def iterate_numbered_pages(self, url: str, params: Dict[str, str] = None) -> Iterable[Dict[str, object]]:
        if params is None:
            params = {}

        def get_page(page_number: int) -> List[Dict[str, object]]:
            params["page"] = str(page_number)
            params["per-page"] = "100"
            return self.get(url, params)

        return NumberedPageIterator(get_page)

    def iterate_unnumbered_pages(self, url: str, params: Dict[str, str] = None) -> Iterable[Dict[str, object]]:
        if params is None:
            params = {}

        def get_page(page_token: Optional[str]) -> Dict[str, Any]:
            if page_token is not None:
                params["page-token"] = page_token
            return self.get(url, params)

        return UnnumberedPageIterator(get_page)

    @staticmethod
    def _raise_for_status(url: str, response: HTTPResponse):
        http_error_msg = ""
        reason = response.reason

        if 400 <= response.status < 600:
            http_error_msg = (
                f"{response.status} Error: {reason} for url: {url}"
            )

        if http_error_msg:
            raise HttpError(http_error_msg, response)
