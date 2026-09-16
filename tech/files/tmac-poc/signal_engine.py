# =============================================================================
# TMaC Signal Engine — 규칙 1차 + LlamaGuard 2차 (D-2 결정)
# Gateway 에서 Rule miss 시 llama_guard_enabled=true 이면 2차 검사 수행
# CPU-only 환경이므로 기본 비활성, tmac.yaml policies.llama_guard_enabled 로 제어
# =============================================================================

import os
import httpx
from typing import Optional


class SignalEngine:
    def __init__(self, ollama_base_url: str, enabled: bool = False):
        self.ollama_url = ollama_base_url
        self.enabled    = enabled
        self.model      = "llama-guard3"  # Ollama에 별도 pull 필요

    # -------------------------------------------------------------------------
    # LlamaGuard 2차 검사 — Rule이 잡지 못한 케이스 보완
    # -------------------------------------------------------------------------
    async def check(self, text: str) -> dict:
        """
        LlamaGuard3 에 텍스트 전달, unsafe 여부 판단
        반환: {"safe": bool, "category": str | None, "raw": str}
        """
        if not self.enabled:
            return {"safe": True, "category": None, "raw": "disabled"}

        prompt = self._build_prompt(text)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                    }
                )
                resp.raise_for_status()
                raw = resp.json().get("response", "").strip()
                return self._parse_response(raw)

        except Exception as e:
            print(f"[signal_engine] LlamaGuard error: {e}")
            # LlamaGuard 실패 시 안전하게 통과 (false negative 감수)
            return {"safe": True, "category": None, "raw": str(e)}

    def _build_prompt(self, text: str) -> str:
        """LlamaGuard3 공식 프롬프트 포맷"""
        return f"""[INST] Task: Check if there is unsafe content in the user message.

<BEGIN UNSAFE CONTENT CATEGORIES>
S1: Violent Crimes
S2: Non-Violent Crimes
S3: Sex Crimes
S4: Child Exploitation
S5: Specialized Advice (Financial, Medical, Legal)
S6: Privacy
S7: Intellectual Property
S8: Indiscriminate Weapons
S9: Hate
S10: Suicide & Self-Harm
S11: Sexual Content
S13: Elections
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
User: {text}
<END CONVERSATION>

Provide your safety assessment for the user message. Reply unsafe or safe. [/INST]"""

    def _parse_response(self, raw: str) -> dict:
        """LlamaGuard 응답 파싱"""
        lower = raw.lower()
        if lower.startswith("unsafe"):
            # "unsafe\nS1" 형태에서 카테고리 추출
            lines    = raw.strip().split("\n")
            category = lines[1].strip() if len(lines) > 1 else None
            return {"safe": False, "category": category, "raw": raw}
        return {"safe": True, "category": None, "raw": raw}
