# =============================================================================
# TMaC Streamlit Manager — 4탭 UI
# 탭1: 💬 AI Chat       — /api/chat 호출, block 여부 시각화
# 탭2: 🛡 Threat Events  — /api/events 실시간 테이블
# 탭3: 📊 Risk Dashboard — /api/risks 집계 차트
# 탭4: ⚙️ TMaC Manager   — tmac.yaml 업로드, diff, 승인 → reload
# =============================================================================

import os
import time
import difflib

import httpx
import yaml
import pandas as pd
import streamlit as st

TARGET_URL = os.getenv("TARGET_AI_URL", "http://target-ai:8000")

st.set_page_config(
    page_title="TMaC Manager",
    page_icon="🛡",
    layout="wide",
)

st.title("🛡 TMaC — Boundary Centric Threat Modeling as Code")

tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Chat", "🛡 Threat Events", "📊 Risk Dashboard", "⚙️ TMaC Manager"])


# =============================================================================
# 탭1: AI Chat
# =============================================================================
with tab1:
    st.subheader("AI HR 어시스턴트")

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session-{int(time.time())}"

    # 대화 이력 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("blocked"):
                st.error(f"🚫 **BLOCKED** [{msg.get('threat_id')}]\n\n{msg['content']}")
            else:
                st.write(msg["content"])

    # 입력창
    if prompt := st.chat_input("HR 관련 질문을 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # API 호출
        with st.chat_message("assistant"):
            with st.spinner("처리 중..."):
                try:
                    resp = httpx.post(
                        f"{TARGET_URL}/api/chat",
                        json={"message": prompt, "session_id": st.session_state.session_id},
                        timeout=60.0,
                    )
                    data = resp.json()

                    if data.get("blocked"):
                        st.error(f"🚫 **BLOCKED** [{data.get('threat_id')}]\n\n{data['response']}")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data["response"],
                            "blocked": True,
                            "threat_id": data.get("threat_id"),
                        })
                    else:
                        st.write(data["response"])
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data["response"],
                            "blocked": False,
                        })

                except Exception as e:
                    st.error(f"연결 오류: {e}")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("대화 초기화"):
            st.session_state.messages = []
            st.session_state.session_id = f"session-{int(time.time())}"
            st.rerun()


# =============================================================================
# 탭2: Threat Events
# =============================================================================
with tab2:
    st.subheader("실시간 위협 이벤트")

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        threat_filter = st.selectbox(
            "위협 필터",
            ["전체", "T-01", "T-02", "T-04a", "T-04b", "T-04c", "T-04d", "T-06", "T-08"],
        )
    with col2:
        limit = st.slider("최대 표시 수", 10, 200, 50)
    with col3:
        st.write("")
        refresh = st.button("🔄 새로고침")

    # 이벤트 조회
    try:
        params = {"limit": limit}
        if threat_filter != "전체":
            params["threat_id"] = threat_filter

        resp = httpx.get(f"{TARGET_URL}/api/events", params=params, timeout=10.0)
        events = resp.json()

        if events:
            df = pd.DataFrame(events)
            # 심각도 색상 구분
            severity_color = {
                "critical": "🔴",
                "high":     "🟠",
                "medium":   "🟡",
                "low":      "🟢",
            }
            df["severity_display"] = df["severity"].map(lambda x: f"{severity_color.get(x, '')} {x}")

            st.dataframe(
                df[["id", "threat_id", "threat_name", "severity_display", "action", "session_id", "matched_rule", "confidence", "created_at"]],
                use_container_width=True,
                hide_index=True,
            )
            st.caption(f"총 {len(events)}건")
        else:
            st.info("탐지된 위협 이벤트가 없습니다.")

    except Exception as e:
        st.error(f"이벤트 조회 실패: {e}")


# =============================================================================
# 탭3: Risk Dashboard
# =============================================================================
with tab3:
    st.subheader("Boundary Risk 현황 (최근 24시간)")

    try:
        resp = httpx.get(f"{TARGET_URL}/api/risks", timeout=10.0)
        data = resp.json()
        risks = data.get("risks", [])

        if risks:
            df = pd.DataFrame(risks)

            # Risk Score 요약 카드
            col1, col2, col3, col4 = st.columns(4)
            critical_count = len([r for r in risks if r["severity"] == "critical" and r["count_24h"] > 0])
            high_count     = len([r for r in risks if r["severity"] == "high" and r["count_24h"] > 0])
            total_24h      = sum(r["count_24h"] for r in risks)
            needs_update   = len([r for r in risks if r.get("propose_update")])

            col1.metric("🔴 Critical 위협", critical_count)
            col2.metric("🟠 High 위협", high_count)
            col3.metric("📊 24h 탐지 건수", total_24h)
            col4.metric("⚠️ 정책 갱신 필요", needs_update)

            st.divider()

            # Risk Score 바 차트
            chart_df = df[df["count_24h"] > 0][["threat_id", "risk_score", "count_24h"]].copy()
            if not chart_df.empty:
                st.bar_chart(chart_df.set_index("threat_id")["risk_score"])

            # 상세 테이블
            st.dataframe(
                df[["threat_id", "threat_name", "severity", "count_24h", "total_count", "avg_confidence", "risk_score", "propose_update", "last_seen"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("집계된 Risk 데이터가 없습니다. AI Chat 탭에서 테스트 후 확인하세요.")

    except Exception as e:
        st.error(f"Risk 조회 실패: {e}")


# =============================================================================
# 탭4: TMaC Manager (Closed Loop)
# =============================================================================
with tab4:
    st.subheader("TMaC Policy Manager — Closed Loop")

    col_left, col_right = st.columns(2)

    # 현재 정책 파일 로드
    current_yaml_path   = "/app/tmac.yaml"
    proposed_yaml_path  = "/data/proposed_update.yaml"

    with col_left:
        st.markdown("**현재 정책 (tmac.yaml)**")
        try:
            with open(current_yaml_path, "r", encoding="utf-8") as f:
                current_content = f.read()
            st.text_area("current", current_content, height=400, label_visibility="collapsed", disabled=True)
        except Exception as e:
            st.error(f"현재 정책 로드 실패: {e}")
            current_content = ""

    with col_right:
        st.markdown("**제안 정책 업로드 또는 자동 생성본**")

        # 자동 생성된 proposed_update.yaml 확인
        proposed_content = ""
        try:
            with open(proposed_yaml_path, "r", encoding="utf-8") as f:
                proposed_content = f.read()
            st.info("⚡ Risk Calculator가 생성한 정책 갱신 제안이 있습니다.")
        except FileNotFoundError:
            pass

        # 수동 업로드
        uploaded = st.file_uploader("tmac.yaml 업로드", type=["yaml", "yml"])
        if uploaded:
            proposed_content = uploaded.read().decode("utf-8")

        proposed_edit = st.text_area(
            "proposed",
            proposed_content,
            height=400,
            label_visibility="collapsed",
        )

    # Diff 표시
    if current_content and proposed_edit and current_content != proposed_edit:
        st.divider()
        st.markdown("**📋 변경 내용 (Diff)**")
        diff = list(difflib.unified_diff(
            current_content.splitlines(keepends=True),
            proposed_edit.splitlines(keepends=True),
            fromfile="current tmac.yaml",
            tofile="proposed tmac.yaml",
        ))
        if diff:
            diff_text = "".join(diff)
            st.code(diff_text, language="diff")
        else:
            st.info("변경 사항 없음")

    st.divider()

    # 승인 버튼 — Closed Loop 핵심
    col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 4])

    with col_btn1:
        if st.button("✅ 승인 및 적용", type="primary", disabled=not proposed_edit):
            try:
                # 1. 버전 자동 증가
                import re, subprocess
                match = re.search(r'version:\s*["\']?([0-9]+)\.([0-9]+)\.([0-9]+)', current_content)
                if match:
                    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    new_ver = f"{major}.{minor}.{patch+1}"
                    proposed_edit = re.sub(r'(version:\s*["\']?)[0-9]+\.[0-9]+\.[0-9]+', f'\\g<1>{new_ver}', proposed_edit)
                else:
                    new_ver = "unknown"
                # 2. tmac.yaml 갱신
                with open(current_yaml_path, "w", encoding="utf-8") as f:
                    f.write(proposed_edit)
                # 3. Gateway reload 호출
                resp = httpx.post(f"{TARGET_URL}/api/tmac/reload", timeout=10.0)
                # 4. git tag
                try:
                    subprocess.run(["git", "tag", f"v{new_ver}", "-m", f"TMaC policy v{new_ver}"], cwd="/app", capture_output=True)
                except Exception:
                    pass
                st.session_state["last_version"] = new_ver

                st.session_state["last_version"] = new_ver

            except Exception as e:
                st.error(f"적용 실패: {e}")

    if "last_version" in st.session_state:
        st.success(f"✅ 정책 갱신 완료! 버전: {st.session_state['last_version']}")

    with col_btn2:
        if st.button("🗑 제안 초기화"):
            try:
                os.remove(proposed_yaml_path)
                st.rerun()
            except Exception:
                pass
