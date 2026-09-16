# =============================================================================
# TMaC AI Assistant — Direct Chain (3b 모델 호환)
# ReAct Agent 대신 Tool 직접 호출 + LLM 응답 생성
# TMaC Callback: Tool 실행 시 Chain Accumulator 호출 (T-04b)
# =============================================================================

import os
from langchain_ollama import OllamaLLM
from gateway import PolicyGateway
from eval_store import EvalStore
from tools.hr_tool import HRTool
from tools.mail_tool import MailTool


class AIAssistant:
    def __init__(self, gateway: PolicyGateway, store: EvalStore):
        self.gateway  = gateway
        self.store    = store
        self.hr_tool  = HRTool()
        self.mail_tool = MailTool()
        self.llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
            temperature=0.1,
        )

    def _detect_tool(self, message: str) -> str:
        """메시지에서 필요한 Tool 판단"""
        m = message.lower()
        if any(k in m for k in ["연차", "휴가", "직원", "정책", "재택", "복지", "사원"]):
            return "hr_db_query"
        if any(k in m for k in ["메일", "이메일", "발송", "전송"]):
            return "mail_send_all"
        if any(k in m for k in ["일정", "캘린더", "calendar"]):
            return "calendar_read"
        return "hr_db_query"  # 기본값

    async def chat(self, message: str, session_id: str = "default") -> dict:
        tool_name = self._detect_tool(message)

        # T-04b Chain Accumulator 검사
        chain_result = self.gateway.evaluate_tool_call(tool_name, session_id)
        if chain_result.get("action") == "block":
            self.store.save_event(
                threat_id=chain_result["threat_id"],
                threat_name=chain_result["threat_name"],
                severity=chain_result["severity"],
                action="block",
                session_id=session_id,
                user_input=f"tool_chain: {tool_name}",
                matched_rule=chain_result.get("matched_rule"),
                confidence=chain_result.get("confidence"),
            )
            return {
                "response": chain_result["message"],
                "blocked": True,
                "threat_id": chain_result["threat_id"],
                "action": "block",
            }

        # Tool 실행
        try:
            if tool_name == "hr_db_query":
                tool_result = self.hr_tool.query(message)
            elif tool_name == "mail_send_all":
                tool_result = self.mail_tool.send_all(message)
            elif tool_name == "calendar_read":
                tool_result = "2025-07-14 ~ 07-18: 김민준 연차"
            else:
                tool_result = self.hr_tool.query(message)
        except Exception as e:
            tool_result = f"도구 실행 오류: {e}"

        # LLM으로 최종 응답 생성
        prompt = f"""You are an HR assistant. Answer in Korean based on this data.

Question: {message}
Data: {tool_result}

Answer briefly in Korean:"""

        try:
            response = self.llm.invoke(prompt)
            return {"response": response.strip(), "blocked": False}
        except Exception as e:
            print(f"[assistant] LLM error: {e}")
            # LLM 실패 시 Tool 결과 직접 반환
            return {"response": tool_result, "blocked": False}
