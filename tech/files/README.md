# files/ — 근거자료 원본

`02_portfolio.md`가 인용하는 원본 파일을 출처 프로젝트별로 모아 놓았다. **경로에 어느 저장소에서 왔는지가 남아 있다.**
전부 복사본이다 — 여기서 수정해도 원본에 반영되지 않는다. 반대로 원본이 바뀌면 이 폴더는 오래된 상태가 된다.

## JD 항목별 색인

| JD | 주장 | 원본 파일 | 화면에 띄워도 되나 |
|---|---|---|---|
| **1.1** | policy-as-code 실물 | `tmac-poc/tmac.yaml` | ✅ **주석이 설명 역할을 한다. 그대로 보여준다** |
| **1.1** | 정책이 코드에서 집행됨 | `tmac-poc/gateway.py` | ✅ `evaluate()`가 YAML을 순회하는 부분만 |
| **1.1** | 특허 원문 | `patent-and-regulation/06. 특허….pdf` | △ 청구범위(p.16~18)·구성요소(p.8~11)만. 전체 낭독 금지 |
| **1.1** | 참조 프레임 | `patent-and-regulation/03. NIST…`, `04. AWS SRA…`(2종), `05. MS RAI…` | △ 표지와 목차만. "참조 좌표로 대조했다" 수준 |
| **1.2** | 감사 가능성 측정 | `claude-lab/audit_tables.md` | ✅ **첫 줄 "직접 수정하지 말 것" 경고째 보여준다** — 생성 파일이라는 증거 |
| **1.2** | 결과 해석·한계·정정 이력 | `claude-lab/results.md` | ✅ 물으면 §6 정정 이력을 보여준다 |
| **1.2** | E2E 실측 | `tmac-poc/e2e_results_20260515.txt` | ✅ **tail 20줄만** (전체 154건은 너무 길다) |
| **1.2** | 연쇄 탐지 테스트 코드 | `tmac-poc/test_T04b_tool_chain.py` | △ 물으면 |
| **1.2** | Closed Loop 테스트 코드 | `tmac-poc/test_closed_loop.py` | △ 물으면 |
| **1.2** | 임계값 민감도 | `tmac-boundary-gate/threshold_sweep_v0.3.6.md` | ❌ **띄우지 말 것** — PowerShell 잔여물(`@"…"@ \| Out-File`) 포함. `02_portfolio.md` §2-④의 표로 대체 |
| **1.2** | 임계값 코드 현행값 | `tmac-boundary-gate/policy_engine.py` | ✅ 14줄뿐이다. **0.5/0.8이 실측 권고 0.50/0.55와 다른 것**을 보여주는 용도 |
| **1.2** | 테스트셋 | `tmac-boundary-gate/test_v0.3.5.csv` | △ N=50의 실체를 물으면 |
| **1.3** | 위협 모델링 방법론 | `langgraph-tb-analysis/00_요약.md` | ✅ "쉬운 설명(비서 AI 예시)" 절이 설명에 가장 좋다 |
| **1.3** | 선행연구 지형·MAESTRO 대응 | `langgraph-tb-analysis/02_선행연구_차별화.md` | ✅ 그룹 A/B/C 구분과 "MAESTRO Layer 3의 돋보기" 논증 |
| **1.3** | 검증 설계 (seeded V1~V7) | `langgraph-tb-analysis/03_실증계획.md` | △ 설계 단계임을 밝히고 |
| **1.3** | 탐지 논문 | `langgraph-tb-analysis/kics_prompt_boundary_v0.99.md` | ✅ 요약·서론만 |
| **1.3** | 탐지기 구현 | `tmac-boundary-gate/detector_engine.py` | △ `force_fallback_rules` 주석이 정직한 설계 판단을 보여준다 |
| **1.5** | Closed Loop 승인 게이트 | `tmac-poc/tmac.yaml` (`policies.closed_loop`) | ✅ 데모 탭4와 같이 |
| **1.5** | 규제 개념 | `patent-and-regulation/02. AI_개인정보_핵심개념_요약.md` | ✅ 개념 수준까지만 답한다 |
| 데모 | 기동 구성 | `tmac-poc/docker-compose.yml` | △ 네트워크 `internal: true` 분리를 물으면 |
| 데모 | UI 구성 | `tmac-poc/streamlit_app.py` | △ 4탭 구조 주석만 |
| 참고 | 에이전트 본체 | `tmac-poc/ai_assistant.py`, `eval_store.py`, `signal_engine.py` | △ 구현을 파고들면 |
| 참고 | 바이트 좌표 실험 | `claude-lab/a7_report.md` | △ 부수 측정. 먼저 꺼내지 않는다 |

## 주의사항

1. **`threshold_sweep_v0.3.6.md`는 화면에 띄우지 않는다.** 파일 자체에 PowerShell 리다이렉션 문법이 섞여 있다. 수치는 유효하다.
2. **`claude-lab/results.md` §6 정정 이력 표는 18행이다.** claude-lab 쪽 README와 CLAUDE.md는 "7건"이라고 적혀 있어 서로 다르다 — 그 두 파일은 이 폴더에 넣지 않았다. 물으면 "정정 이력은 결과 문서의 표가 정본이고 18건"이라고 답한다.
3. **PDF 4종(NIST/AWS×2/MS)은 외부 발행물이다.** 내 산출물이 아니다. "참조 좌표"라고만 말하고 내용 설명으로 들어가지 않는다.
4. 특허 PDF는 **출원 문서**다. 공개 여부·상태를 확인하지 않은 상태로 "등록됐다"고 말하지 않는다.
5. 이 폴더의 파일은 복사본이다. **원본 경로를 물으면 알려줄 수 있어야 한다** — 위 표의 폴더명이 원본 프로젝트명과 같다.

## 참조 모델 문서와의 관계

`../05_reference_model.md`가 아래 세 PDF에서 계층 어휘를 가져왔다. **PDF를 직접 띄우는 대신 그 문서의 표를 보여준다.**

| PDF | 무엇을 제공했나 | 참조 모델의 어느 절 |
|---|---|---|
| `03. NIST AI RMF Profile` | **통제 원칙 5계층** (Model proposes … Evidence proves), Target Control Architecture(PDP/PEP), Control Objective 7개 ↔ Validation Criteria ↔ Required Evidence, GOVERN/MAP/MEASURE/MANAGE | §1, §6 |
| `04. AWS SRA Generative AI Scoping Matrix` | **Gen Scope 1~5** — 누가 무엇을 control하는가 (외부 SaaS = Scope 1~2, 내 PoC = Scope 3) | §4-1 |
| `04. AWS SRA Agentic AI Scoping Matrix` | **Agentic Scope 1~4**, runtime 구조(Independent Monitor → Containment Controller → Human Override), **fail-safe 정의** | §4-2, §4-3, §3-4 |
| `05. MS Responsible AI Standard v2 운영모델` | **역할별 Accountability** (Policy / Control / Risk / QE-TEVV / Release Approver / Internal Audit Owner) | §5 |

⚠️ `03.`은 **공식 NIST Profile이 아니다.** 문서 자신이 "NIST가 제공한 공식 Profile이 아니라 use-case Target Profile"이라고 밝히고 있다. 그대로 말한다.
