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
        # Try chat-completions first
        url_chat = f"{self.api_base}/chat/completions"
        payload_chat: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
        try:
            r = requests.post(url_chat, headers=self._headers(), json=payload_chat, timeout=self.timeout_s)
            if r.status_code == 200:
                data = r.json()
                # OpenAI-compatible: choices[0].message.content
                choices = data.get("choices", [])
                if choices and isinstance(choices[0], dict):
                    msg = choices[0].get("message", {})
                    if isinstance(msg, dict):
                        return (msg.get("content") or "").strip()
                # Some providers return "response"
                return (data.get("response") or "").strip() or "error"
        except Exception:
            # fall through to completions
            pass

        # Fallback: plain completions
        url_comp = f"{self.api_base}/completions"
        try:
            prompt = "\n".join(m.get("content", "") for m in messages)
            payload_comp: Dict[str, Any] = {
                "model": model,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            }
            r = requests.post(url_comp, headers=self._headers(), json=payload_comp, timeout=self.timeout_s)
            if r.status_code == 200:
                data = r.json()
                # OpenAI legacy: choices[0].text
                choices = data.get("choices", [])
                if choices and isinstance(choices[0], dict):
                    return (choices[0].get("text") or "").strip()
                return (data.get("response") or "").strip() or "error"
        except Exception:
            pass
        return "error"

    # -------------------------------
    # Internals
    # -------------------------------
    def _headers(self) -> Dict[str, str]:
        hdrs = {"Content-Type": "application/json"}
        if self.api_key:
            hdrs["Authorization"] = f"Bearer {self.api_key}"
        return hdrs


