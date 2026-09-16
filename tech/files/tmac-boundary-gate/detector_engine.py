from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import re

# HF/torch import는 환경에 따라 실패할 수 있으므로 안전하게 처리
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    _HF_AVAILABLE = True
except Exception:
    _HF_AVAILABLE = False


@dataclass
class DetectorConfig:
    """
    model_name_or_path:
      - HF 모델 이름 또는 로컬 fine-tuned 모델 경로
    """
    model_name_or_path: str = "distilbert-base-uncased"
    max_length: int = 256
    device: Optional[str] = None

    # ✅ 옵션A: 학습 전에는 BERT score를 정책에 쓰지 않기 위해 rule만 사용
    # v0.3에서 fine-tuned 모델이 준비되면 False로 전환
    force_fallback_rules: bool = True

    # 모델 로딩 실패 시에도 안전하게 동작하도록 rule fallback 사용 여부
    enable_fallback_rules: bool = True


class ThreatSignalEngine:
    """
    v0.2 Threat Signal Engine
    - score(0~1)만 제공 (판정은 Policy)
    - DistilBERT 로딩 시도
    - 옵션A(force_fallback_rules=True)인 동안에는 항상 rule score 사용
    """

    RULE_PATTERNS = [
        r"ignore previous instructions",
        r"reveal the system prompt",
        r"system prompt",
        r"developer mode",
        r"show (me )?(your )?(internal|hidden) (rules|policy)",
        # KR hints
        r"이전 지침을 무시",
        r"시스템 프롬프트",
        r"내부 정책",
    ]

    def __init__(self, cfg: DetectorConfig | None = None):
        self.cfg = cfg or DetectorConfig()
        self._model_ready = False
        self._load_error = None

        # HF 라이브러리 자체가 없으면 모델 시도 불가
        if not _HF_AVAILABLE:
            self._model_ready = False
            self._load_error = "transformers/torch not available"
            return

        # device 선택
        if self.cfg.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = self.cfg.device

        # DistilBERT 로딩 시도 (성공해도 v0.3 전까지는 policy에 안 씀)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.cfg.model_name_or_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.cfg.model_name_or_path)
            self.model.to(self.device)
            self.model.eval()
            self._model_ready = True
        except Exception as e:
            self._model_ready = False
            self._load_error = repr(e)

    def is_model_ready(self) -> bool:
        return self._model_ready

    def evaluate(self, text: str, ctx: Dict[str, Any] | None = None) -> float:
        """
        score 반환.
        ✅ 옵션A(force_fallback_rules=True)이면 항상 rule score 반환.
        v0.3에서 fine-tuned 모델 준비 후 force_fallback_rules=False로 전환하면 BERT score 사용 가능.
        """
        if self.cfg.force_fallback_rules:
            return self._rule_score(text)

        if self._model_ready:
            return self._bert_score(text)

        if self.cfg.enable_fallback_rules:
            return self._rule_score(text)

        return 0.5

    def _bert_score(self, text: str) -> float:
        """
        DistilBERT 기반 score
        (binary classifier, label 1=attack 가정)
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=self.cfg.max_length,
            padding=True,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=-1)

        if probs.shape[-1] < 2:
            return 0.0
        return float(probs[0, 1].item())

    def _rule_score(self, text: str) -> float:
        """
        v0.1과 동일한 의미의 최소 rule score:
        - 매칭 있으면 0.5 (의심)
        - 없으면 0.1 (정상)
        """
        t = text.lower()
        for p in self.RULE_PATTERNS:
            if re.search(p, t, flags=re.IGNORECASE):
                return 0.5
        return 0.1
