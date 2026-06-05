from typing import Dict, List  # typing helpers

import requests  # HTTP client for LLM APIs

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_CHAT_URL,
    GROQ_MODEL,
    LLM_PROVIDER,
    MAX_LLM_MESSAGE_CHARS,
    REQUEST_TIMEOUT_SECONDS,
)


class LLMService:
    """Shared LLM adapter for the manager and itinerary agents."""

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
        messages = self._fit_messages(messages)  # trim messages to LLM size limits
        if LLM_PROVIDER == "gemini":
            return self._generate_with_gemini(messages, temperature)
        return self._generate_with_groq(messages, temperature)

    def _fit_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:  # ensure payload fits char limits
        fitted = []
        remaining_chars = MAX_LLM_MESSAGE_CHARS
        for message in messages:
            content = message.get("content", "")
            if len(content) > remaining_chars:
                content = content[: max(remaining_chars, 0)] + "\n[Context truncated to fit LLM payload limits.]"
            fitted.append({**message, "content": content})
            remaining_chars -= len(content)
        return fitted

    def _generate_with_groq(self, messages: List[Dict[str, str]], temperature: float) -> str:
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_free_api_key_here":
            return "Groq API key not configured. Using deterministic local planning output."

        response = requests.post(
            GROQ_CHAT_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": GROQ_MODEL, "messages": messages, "temperature": temperature},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError:
            if response.status_code == 413:
                return "The travel context was too large for the LLM provider, so SmartTripAI used the structured local plan instead."
            try:
                detail = response.json().get("error", {}).get("message", response.text[:200])
            except (ValueError, AttributeError, KeyError):
                detail = response.text[:200] if response.text else "unknown error"
            return f"Groq request failed ({response.status_code}): {detail}"
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _generate_with_gemini(self, messages: List[Dict[str, str]], temperature: float) -> str:
        if not GEMINI_API_KEY:
            return "Gemini API key not configured. Using deterministic local planning output."

        prompt = "\n\n".join(f"{message['role'].upper()}: {message['content']}" for message in messages)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
        response = requests.post(
            url,
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature},
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError:
            if response.status_code == 413:
                return "The travel context was too large for the LLM provider, so SmartTripAI used the structured local plan instead."
            return f"Gemini request failed ({response.status_code}). Using deterministic local planning output."
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


class GeminiService(LLMService):
    """Backward-compatible name used by older imports."""


class GroqService(LLMService):
    """Backward-compatible name used by manager imports."""
