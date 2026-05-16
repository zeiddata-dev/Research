"""
zeid_data_island_client.py

A small, defensive Island API client.
- API key auth (Authorization Bearer <key> by default, configurable)
- basic retry/backoff for 429/5xx
- best-effort pagination (because APIs love making this *fun*)

You will likely need to adjust endpoint paths in your config to match your tenant's OpenAPI.
"""

from __future__ import annotations

import time
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union
from urllib.parse import urljoin

import requests


Json = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


@dataclass
class AuthConfig:
    header: str = "Authorization"
    prefix: str = "Bearer"  # set "" for x-api-key style
    api_key: str = ""


@dataclass
class HttpConfig:
    timeout_seconds: int = 30
    verify_ssl: bool = True
    max_retries: int = 6
    backoff_seconds: float = 1.0


class IslandClient:
    def __init__(self, base_url: str, auth: AuthConfig, http: HttpConfig):
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.auth = auth
        self.http = http
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        key = (self.auth.api_key or "").strip()
        if not key:
            raise RuntimeError("Missing API key (auth.api_key). Set it via environment and config.")
        if self.auth.prefix:
            value = f"{self.auth.prefix} {key}".strip()
        else:
            value = key
        return {
            "Accept": "application/json",
            self.auth.header: value,
            "User-Agent": "zeid-data-evidence-bundle-kit/0.1.0",
        }

    def _request(self, method: str, path_or_url: str, *, params=None, json_body=None) -> requests.Response:
        # path_or_url can be a relative path (e.g. "users") or a full URL (pagination "next" links).
        url = path_or_url if path_or_url.startswith("http") else urljoin(self.base_url, path_or_url.lstrip("/"))

        last_err = None
        for attempt in range(self.http.max_retries + 1):
            try:
                resp = self.session.request(
                    method,
                    url,
                    headers=self._headers(),
                    params=params,
                    json=json_body,
                    timeout=self.http.timeout_seconds,
                    verify=self.http.verify_ssl,
                )

                # Rate limiting
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    if retry_after:
                        sleep_s = float(retry_after)
                    else:
                        sleep_s = self.http.backoff_seconds * (2 ** attempt)
                    time.sleep(min(60.0, sleep_s))
                    continue

                # Retry server errors
                if 500 <= resp.status_code < 600:
                    time.sleep(min(60.0, self.http.backoff_seconds * (2 ** attempt)))
                    continue

                resp.raise_for_status()
                return resp

            except requests.RequestException as e:
                last_err = e
                time.sleep(min(60.0, self.http.backoff_seconds * (2 ** attempt)))

        raise RuntimeError(f"Island API request failed after retries: {last_err}")

    def get_json(self, path_or_url: str, *, params=None) -> Json:
        resp = self._request("GET", path_or_url, params=params)
        if not resp.text:
            return None
        return resp.json()

    def post_json(self, path_or_url: str, *, json_body=None, params=None) -> Json:
        resp = self._request("POST", path_or_url, params=params, json_body=json_body)
        if not resp.text:
            return None
        return resp.json()

    def iter_items(self, path: str, *, params: Optional[Dict[str, Any]] = None, item_path: Optional[str] = None) -> Iterator[Json]:
        """
        Iterate items from list-like endpoints with best-effort pagination.

        Supports common response patterns:
        - list response: [ ... ]
        - dict response with list under key: {"data":[...]} or {"items":[...]} (use item_path)
        - next URL: {"next":"https://..."} or {"links":{"next":"..."}} (best effort)
        - token pagination: {"next_page_token":"..."} (best effort)
        """
        params = dict(params or {})
        url_or_path = path

        while True:
            payload = self.get_json(url_or_path, params=params)

            items, next_url, next_token = self._extract_items_and_next(payload, item_path=item_path)

            for it in items:
                yield it

            if next_url:
                url_or_path = next_url
                params = {}  # next_url usually includes its own query
                continue

            if next_token:
                # Common pattern: pass token as page_token / next_page_token
                # If your API uses a different param name, set it in config by including it in params.
                params["page_token"] = next_token
                url_or_path = path
                continue

            break

    @staticmethod
    def _extract_items_and_next(payload: Json, *, item_path: Optional[str]) -> Tuple[List[Json], Optional[str], Optional[str]]:
        items: List[Json] = []
        next_url: Optional[str] = None
        next_token: Optional[str] = None

        if isinstance(payload, list):
            items = payload
            return items, None, None

        if isinstance(payload, dict):
            # Try to find items
            if item_path:
                # very small "pointer": only supports single key, e.g. "data" or "items"
                if item_path in payload and isinstance(payload[item_path], list):
                    items = payload[item_path]
            else:
                for k in ("data", "items", "results"):
                    if k in payload and isinstance(payload[k], list):
                        items = payload[k]
                        break

            # Try to find next URL
            if isinstance(payload.get("next"), str):
                next_url = payload["next"]
            elif isinstance(payload.get("links"), dict) and isinstance(payload["links"].get("next"), str):
                next_url = payload["links"]["next"]

            # Try to find token
            for tk in ("next_page_token", "nextPageToken", "next_token"):
                if isinstance(payload.get(tk), str) and payload.get(tk):
                    next_token = payload[tk]
                    break

        return items, next_url, next_token
