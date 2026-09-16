# =============================================================================
# TMaC Eval Store — PostgreSQL 위협 이벤트 저장 및 조회
# Risk Calculator 집계도 여기서 수행
# =============================================================================

import json
from datetime import datetime, timezone
from typing import Optional

import psycopg2
import psycopg2.extras


class EvalStore:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._connect()

    def _connect(self):
        self.conn = psycopg2.connect(self.dsn)
        self.conn.autocommit = True
        print(f"[eval_store] Connected to store DB")

    def _ensure_connection(self):
        """연결 끊김 시 재연결"""
        try:
            self.conn.cursor().execute("SELECT 1")
        except Exception:
            self._connect()

    # -------------------------------------------------------------------------
    # 이벤트 저장
    # -------------------------------------------------------------------------
    def save_event(
        self,
        threat_id: str,
        threat_name: str,
        severity: str,
        action: str,
        session_id: str = "default",
        user_input: str = "",
        matched_rule: Optional[str] = None,
        confidence: Optional[float] = None,
        risk_score: Optional[float] = None,
        extra: Optional[dict] = None,
        boundary_id: Optional[str] = None,
    ) -> int:
        self._ensure_connection()
        sql = """
            INSERT INTO threat_events
                (threat_id, threat_name, boundary_id, severity, action,
                 session_id, user_input, matched_rule, confidence, risk_score, extra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, (
                threat_id,
                threat_name,
                boundary_id,
                severity,
                action,
                session_id,
                user_input[:2000] if user_input else "",
                matched_rule,
                confidence,
                risk_score,
                json.dumps(extra) if extra else None,
            ))
            event_id = cur.fetchone()[0]
            print(f"[eval_store] Event saved: id={event_id} threat={threat_id} action={action}")
            return event_id

    # -------------------------------------------------------------------------
    # 이벤트 조회
    # -------------------------------------------------------------------------
    def get_events(self, limit: int = 50, threat_id: Optional[str] = None) -> list[dict]:
        self._ensure_connection()
        if threat_id:
            sql = """
                SELECT id, threat_id, threat_name, severity, action,
                       session_id, matched_rule, confidence, created_at
                FROM threat_events
                WHERE threat_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            params = (threat_id, limit)
        else:
            sql = """
                SELECT id, threat_id, threat_name, severity, action,
                       session_id, matched_rule, confidence, created_at
                FROM threat_events
                ORDER BY created_at DESC
                LIMIT %s
            """
            params = (limit,)

        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    # -------------------------------------------------------------------------
    # Risk 집계 — Risk Calculator
    # -------------------------------------------------------------------------
    def get_risk_summary(self) -> dict:
        """
        최근 24시간 위협 통계 기반 Risk Score 산출
        tmac.yaml risk_calculator.weight 참고
        """
        self._ensure_connection()
        sql = """
            SELECT
                threat_id,
                threat_name,
                severity,
                COUNT(*) AS total_count,
                COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '24 hours') AS count_24h,
                ROUND(AVG(confidence)::numeric, 3) AS avg_confidence,
                MAX(created_at) AS last_seen
            FROM threat_events
            GROUP BY threat_id, threat_name, severity
            ORDER BY count_24h DESC
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()

        summary = []
        for r in rows:
            row = dict(r)
            # Risk Score 산출: severity 가중치 × 빈도 가중치
            severity_weight = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
            sw = severity_weight.get(row["severity"], 0.5)
            freq_score = min(row["count_24h"] / 10.0, 1.0)  # 10회 이상이면 1.0
            risk = round(sw * 0.5 + freq_score * 0.3 + float(row.get("avg_confidence") or 0) * 0.2, 3)
            row["risk_score"]        = risk
            row["last_seen"]         = row["last_seen"].isoformat() if row["last_seen"] else None
            row["propose_update"]    = risk >= 0.75  # Closed Loop 트리거 여부
            summary.append(row)

        return {"risks": summary, "generated_at": datetime.now(timezone.utc).isoformat()}
