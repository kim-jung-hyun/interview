# =============================================================================
# TMaC Policy Gateway — tmac.yaml 파싱 및 위협 판정
# 모든 입력은 이 클래스를 통해 평가됨
# Chain Accumulator (T-04b) 도 여기서 관리
# =============================================================================

import re
import time
import yaml
from collections import deque
from typing import Optional


class PolicyGateway:
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        self._load()
        # 세션별 Tool 호출 이력 {session_id: deque[(tool_name, timestamp)]}
        self._chain_history: dict[str, deque] = {}

    # -------------------------------------------------------------------------
    # YAML 로드 / 리로드
    # -------------------------------------------------------------------------
    def _load(self):
        with open(self.yaml_path, "r", encoding="utf-8") as f:
            self._policy = yaml.safe_load(f)
        self.version = self._policy["metadata"]["version"]
        self._threats = {t["id"]: t for t in self._policy.get("threats", [])}
        self._policies = self._policy.get("policies", {})
        print(f"[gateway] Policy loaded v{self.version}, threats={list(self._threats.keys())}")

    def reload(self):
        """Closed Loop — /api/tmac/reload 호출 시 정책 갱신"""
        self._load()
        self._chain_history.clear()  # 체인 이력 초기화

    # -------------------------------------------------------------------------
    # 메인 평가 함수 — 입력 텍스트 위협 검사
    # -------------------------------------------------------------------------
    def evaluate(self, text: str, session_id: str = "default") -> dict:
        """
        tmac.yaml 의 모든 위협 룰을 순서대로 평가
        첫 번째 매칭된 위협의 response 반환
        """
        for threat_id, threat in self._threats.items():
            detection = threat.get("detection", {})
            method = detection.get("method")

            # 규칙 기반 평가 (T-01, T-02, T-04a, T-04c, T-06)
            if method == "rule_engine":
                result = self._eval_rules(text, threat)
                if result:
                    return self._build_response(threat, result)

            # Rate Limiter (T-08)
            elif method == "rate_limiter":
                result = self._eval_rate_limit(text, session_id, threat)
                if result:
                    return self._build_response(threat, result)

        # 위협 미탐지 — 기본 정책 적용
        default = self._policies.get("default_action", "allow")
        return {"action": default, "threat_id": None, "message": ""}

    # -------------------------------------------------------------------------
    # Tool 실행 후 Chain 누적 평가 (T-04b) — AIAssistant 에서 호출
    # -------------------------------------------------------------------------
    def evaluate_tool_call(self, tool_name: str, session_id: str) -> dict:
        """
        Agent가 Tool을 실행할 때마다 호출
        Chain Accumulator: window_size 내 누적 Risk Score 계산
        """
        threat = self._threats.get("T-04b")
        if not threat:
            return {"action": "allow"}

        detection = threat["detection"]
        window    = detection.get("window_size", 5)
        threshold = detection.get("risk_threshold", 0.75)
        scores    = detection.get("tool_risk_scores", {})

        # 세션별 이력 초기화
        if session_id not in self._chain_history:
            self._chain_history[session_id] = deque(maxlen=window)

        self._chain_history[session_id].append((tool_name, time.time()))
        history = list(self._chain_history[session_id])

        # 누적 Risk Score 산출 (최근 window 내 합산)
        cumulative = sum(scores.get(t, 0.3) for t, _ in history)
        normalized = min(cumulative, 1.0)

        print(f"[gateway] Chain [{session_id}]: {[t for t,_ in history]} score={normalized:.2f}")

        # 알려진 에스컬레이션 패턴 매칭
        chain_names = [t for t, _ in history]
        for pattern in detection.get("escalation_patterns", []):
            pat_chain   = pattern["chain"]
            pat_thresh  = pattern.get("cumulative_threshold", threshold)
            # 패턴 체인이 현재 이력의 끝부분과 일치하는지 확인
            if len(chain_names) >= len(pat_chain):
                tail = chain_names[-len(pat_chain):]
                if tail == pat_chain and normalized >= pat_thresh:
                    print(f"[gateway] Escalation pattern matched: {pattern['id']}")
                    return self._build_response(threat, {
                        "matched_rule": pattern["id"],
                        "confidence": normalized,
                    })

        # 단순 누적 임계값 초과
        if normalized >= threshold:
            return self._build_response(threat, {
                "matched_rule": "chain_accumulator",
                "confidence": normalized,
            })

        return {"action": "allow", "cumulative_score": normalized}

    # -------------------------------------------------------------------------
    # 내부 헬퍼
    # -------------------------------------------------------------------------
    def _eval_rules(self, text: str, threat: dict) -> Optional[dict]:
        """정규식 룰 매칭"""
        rules = threat.get("detection", {}).get("rules", [])
        for rule in rules:
            pattern = rule.get("pattern", "")
            try:
                if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                    return {"matched_rule": rule["id"], "confidence": rule.get("confidence", 0.8)}
            except re.error as e:
                print(f"[gateway] Regex error in {rule['id']}: {e}")
        return None

    def _eval_rate_limit(self, text: str, session_id: str, threat: dict) -> Optional[dict]:
        """메시지 길이 초과 체크 (분당 요청수는 별도 미들웨어 처리)"""
        rules = threat.get("detection", {}).get("rules", [])
        for rule in rules:
            max_len = rule.get("max_message_length")
            if max_len and len(text) > max_len:
                return {"matched_rule": rule["id"], "confidence": 1.0}
        return None

    def _build_response(self, threat: dict, match_info: dict) -> dict:
        """위협 탐지 결과 딕셔너리 구성"""
        resp = threat.get("response", {})
        return {
            "action":       resp.get("action", "block"),
            "message":      resp.get("message", "요청이 차단되었습니다."),
            "threat_id":    threat["id"],
            "threat_name":  threat["name"],
            "severity":     threat.get("severity", "high"),
            "matched_rule": match_info.get("matched_rule"),
            "confidence":   match_info.get("confidence"),
            "log_level":    resp.get("log_level", "warning"),
            "store_event":  resp.get("store_event", True),
        }
