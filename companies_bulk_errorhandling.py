#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json

BASE_URL = "https://api.dealroom.co/api/v1"
HEADERS = {"Content-Type": "application/json"}
api_key = ""  # Replace with the issued Dealroom API key
AUTH = HTTPBasicAuth(api_key, "")

# Set the parameters depending on the use case. See refs:
# https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
retry_strategy = Retry(
    backoff_factor=1,
    total=3,
    read=3,
    status_forcelist=[500, 502, 503, 504],
    method_whitelist=False, # This is important to force retry of POST requests
)
ADAPTER = HTTPAdapter(max_retries=retry_strategy)

def get_session() -> requests.Session:
    """Return a Session object initialized with correct parameters."""

    session = requests.Session()
    session.headers = HEADERS
    session.auth = AUTH
    session.mount(BASE_URL, ADAPTER)
    return session


def post_request(
        session: requests.Session,
        url: str,
        data: dict
    ) -> requests.models.Response:
    """Make a POST request using input Session object. If ConnectionError is
    raised, we refresh the session."""

    try:
        return session.post(url, json=data)

    except ConnectionError as exc:
        exc_str = f"{exc.__class__.__name__}: {exc}"
        print(f"POST request raised: {exc_str}. Refreshing session.")
        session = get_session()
        return session.post(url, json=data)


def get_response_body(response: requests.models.Response) -> dict:
    """Get response body. If JSONDecodeError is raised, returns an empty
    dictionary."""

    try:
        return response.json()

    except json.JSONDecodeError as exc:
        exc_str = f"{exc.__class__.__name__}: {exc}"
        print(f"Getting response body raised: {exc_str}. Returning empty dictionary.")
        return {}


if __name__ == "__main__":

    session = get_session()
    url = f"{BASE_URL}/companies/bulk"

    next_page_id = ""
    while True:
        data = {
            'form_data': {'must': {'hq_locations': ['Berlin']}},
            'fields': 'id,name,path,tagline,about,url,website_url',
            'next_page_id': next_page_id,
            'limit': 100,
        }

        r = post_request(session, url, data)
        res = get_response_body(r)
        print(res)

        next_page_id = res['next_page_id']
        if next_page_id is None:
            break
