"""
Simple Cerebras Inference API client.

This client targets an OpenAI-compatible HTTP surface. If Cerebras changes
endpoints, configure with environment variables or CLI flags in callers.

Env vars:
  - CEREBRAS_API_KEY: API key for authorization
  - CEREBRAS_API_BASE: Base URL (default: https://api.cerebras.ai/v1)
"""

from typing import Any, Dict, List, Optional
import os
import requests
import time


def _safe_get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    try:
        return os.environ.get(name, default)
    except Exception:
        return default


class CerebrasClient:
    """
    Minimal client for Cerebras Inference APIs with conservative fallbacks.
    """

    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None, timeout_s: float = 12.0):
        self.api_key = api_key or _safe_get_env("CEREBRAS_API_KEY") or ""
        self.api_base = (api_base or _safe_get_env("CEREBRAS_API_BASE") or "https://api.cerebras.ai/v1").rstrip("/")
        self.timeout_s = timeout_s

    # -------------------------------
    # Public API
    # -------------------------------
    def list_models(self) -> List[str]:
        """
        Attempt to list available models. If endpoint unsupported, return empty list.
        """
        url = f"{self.api_base}/models"
        try:
            resp = requests.get(url, headers=self._headers(), timeout=self.timeout_s)
            if resp.status_code == 200:
                data = resp.json()
                # OpenAI-compatible format: {"data": [{"id": "model"}, ...]}
                if isinstance(data, dict) and isinstance(data.get("data"), list):
                    return [m.get("id", "") for m in data.get("data", []) if isinstance(m, dict)]
        except Exception:
            pass
        return []

    def chat_completion(self, model: str, messages: List[Dict[str, str]], max_tokens: int = 16, temperature: float = 0.1) -> str:
        """
        Call chat completions; falls back to plain completions if unavailable.
        Returns text or "error".
        """
        # Try chat-completions first with basic retries
        url_chat = f"{self.api_base}/chat/completions"
        payload_chat: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
        resp = self._post_with_retries(url_chat, payload_chat)
        if isinstance(resp, requests.Response):
            if resp.status_code == 200:
                try:
                    data = resp.json()
                except Exception as e:
                    return f"error: invalid_json {type(e).__name__}"
                choices = data.get("choices", [])
                if choices and isinstance(choices[0], dict):
                    msg = choices[0].get("message", {})
                    if isinstance(msg, dict):
                        return (msg.get("content") or "").strip()
                return (data.get("response") or "").strip() or "error: empty_response"
            return f"error: {resp.status_code} {resp.text[:200]}"
        elif isinstance(resp, Exception):
            return f"error: {type(resp).__name__}: {resp}"

        # Fallback: plain completions
        url_comp = f"{self.api_base}/completions"
        prompt = "\n".join(m.get("content", "") for m in messages)
        payload_comp: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
        resp = self._post_with_retries(url_comp, payload_comp)
        if isinstance(resp, requests.Response):
            if resp.status_code == 200:
                try:
                    data = resp.json()
                except Exception as e:
                    return f"error: invalid_json {type(e).__name__}"
                choices = data.get("choices", [])
                if choices and isinstance(choices[0], dict):
                    return (choices[0].get("text") or "").strip()
                return (data.get("response") or "").strip() or "error: empty_response"
            return f"error: {resp.status_code} {resp.text[:200]}"
        elif isinstance(resp, Exception):
            return f"error: {type(resp).__name__}: {resp}"
        return "error: unknown"

    # -------------------------------
    # HTTP helper with retries
    # -------------------------------
    def _post_with_retries(self, url: str, payload: Dict[str, Any], retries: int = 2):
        delay = 0.5
        for attempt in range(retries + 1):
            try:
                r = requests.post(url, headers=self._headers(), json=payload, timeout=self.timeout_s)
                # Retry on 429/5xx
                if r.status_code in (429, 500, 502, 503, 504):
                    if attempt < retries:
                        time.sleep(delay)
                        delay *= 2
                        continue
                return r
            except Exception as e:
                if attempt < retries:
                    time.sleep(delay)
                    delay *= 2
                    continue
                return e

    # -------------------------------
    # Internals
    # -------------------------------
    def _headers(self) -> Dict[str, str]:
        hdrs = {"Content-Type": "application/json"}
        if self.api_key:
            hdrs["Authorization"] = f"Bearer {self.api_key}"
        return hdrs


