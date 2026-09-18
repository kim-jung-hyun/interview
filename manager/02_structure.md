# 기준선 — 거버넌스 매니저 인터뷰용

> **이 문서에는 기준선만 남는다.** 다섯 계층·Policy/Guardrail·역할 소유권·Scope·게이트·규제 등 나머지 내용은 전부 `03_#1.1-1.5_keywords.md`의 1.1·1.2·1.3 절로 옮겼다. 이 문서는 오프닝에서 항상 먼저 띄우는 기준선 한 장만 남긴다.
>
> 계층 어휘는 내가 만든 것이 아니라 세 참조 문서에서 가져왔다 — NIST AI RMF Profile, AWS SRA Scoping Matrix 2종, Microsoft Responsible AI Standard v2.

---

## 0. 기준선 — 이 인터뷰 전체의 기준

**모든 역할 질문은 이 사슬로 답한다.**

    기준 (AI GRC · 내 자리)  →  구현 (Development)  →  판정 (Assurance)  →  수용 (Risk / Business)
    「기준 제공자」
    Staff AI Security Governance Engineer

| 분리선 | 내용 | 사이 |
|---|---|---|
| **①** | 만든 사람이 판정하지 않는다 | 구현 ↔ Assurance |
| **②** | 판정한 사람이 위험을 수용하지 않는다 | Assurance ↔ 수용 |
| **③** | **기준을 만든 사람이 그 기준으로 판정하지 않는다** | **내 자리 ↔ Assurance** |

**Assurance = 실행 · 모니터링 · 시험 · 승인 · 감사.** Control Owner · QE/TEVV · **Release Approver** · Internal Audit이 여기 있다.

**"기준과 구현 사이엔 뭐가 있습니까?"라고 물으면 (분리선 표에 없는 구간이다)**
> "그 경계가 하나 더 있습니다 — **저는 「무엇을 충족해야 하는가」를 정하고, Security Architecture 팀이 「어떻게 만들 것인가」를 설계**합니다. 제가 설계까지 하면 그 팀의 자리를 침범하고 제 기준이 특정 설계에 묶입니다. 그래서 제 산출물①의 1차 수신자가 Security Architecture입니다."

### 내 자리 = 「기준 제공자」

지원 직함이 `Staff AI Security Governance **Engineer** (AI GRC)`다. **관리자가 아닌 개별 기여자(IC)**이고 `Governance`는 기준을 세우는 일이다. **직함 자체가 승인자가 아니라 기준 제공자임을 말한다.**

### 내 산출물

| # | 산출물 | 받는 쪽 | 내용 |
|---|---|---|---|
| **①** | **개발팀용 기준과 가이드** | **1차: Security Architecture**(별도 팀) → 2차: Development · AI System Owner | **규제 등의 requirement를 SW 구조에 넣을 수 있는 형태로** 변환한 기준 |
| **②** | **Assurance용 구조 요건** | Control Owner · QE/TEVV · Release Approver · Internal Audit | **assessment 가능한 evidence**와 **audit 가능한 구조**가 나오게 하는 요건 |

**이 산출물이 시스템에서 잡는 지점** (`07_system_architecture.md` §6 근거) — **산출물①은 Model·Harness·Guardrail의 설계 요건**이 되고, **산출물②는 Evidence·Test/E2E Test의 구조 요건**이 된다. 물으면 이 한 줄로 architecture.svg와 연결한다.

**말할 한 문장 — 이번 인터뷰에서 가장 먼저 말한다**
> **"제 자리는 「기준 제공자」입니다. 저는 승인하지 않습니다 — 승인이 가능하도록 만듭니다. 제 산출물은 결정이 아니라 결정의 전제입니다."**

**근거는 운영모델 표의 구조다** — `05_ai_lifecycle.md` §2의 11단계 표에서 **AI GRC는 「최종 책임」 열에 한 번도 나오지 않는다.** 수행 책임과 검토 열에만 나온다. 내 해석이 아니다.

### 다음 화면 — 실행 흐름 그림 (질문이 시스템 구조 쪽으로 오면)

**그림 먼저, 말은 그 다음이다.** `figures/architecture.svg`(정본 `07_system_architecture.md` §2·§3, 내용 변경 금지) — Identity/Context → Model → Harness → Policy(PDP) → Guardrail(PEP) → Tool 실행까지의 흐름과, 모든 단계에서 Evidence로 점선이 모이는 것, Test/E2E Test가 그 경로에 입력을 주입해 검증하는 것을 한 장으로 보여준다.

> "그림으로 먼저 보여드리면, 요청이 Model → Harness → Policy → Guardrail을 거쳐 실행되고, 모든 단계가 Evidence로 기록됩니다. **이 그림을 말로 풀면 다음과 같습니다."** → 다섯 계층 설명(`03_#1.1-1.5_keywords.md` 1.1)으로 이어간다.

---

## 다섯 계층·Policy/Guardrail·역할·Scope·게이트·규제는 어디 있나

전부 `03_#1.1-1.5_keywords.md`로 옮겼다.

| 옮긴 내용 | 이동한 곳 |
|---|---|
| 통제 원칙 — 다섯 계층 | 1.1 Framework Architecture & Policy-as-Code |
| Policy와 Guardrail은 다르다 (+ PDP/PEP, Test/E2E) | 1.1 |
| 정책이 살아 있게 만드는 구조 — 기준 변경 게이트 | 1.1 |
| 규제를 게이트 조건으로 (PIPA/EU AI Act/AI기본법 + REQUIRE_APPROVAL 실행 답변) | 1.1 |
| 누가 무엇을 소유하는가 — 역할 상세·Accountability | 1.2 Assurance Partnering |
| 통제 범위 (AWS SRA Scope 1~5) | 1.3 AI Risk Evaluation & Safeguards |
| 자율성 범위 (Agency Scope, Fail-safe) | 1.3 |
| 약어 부록 | 파일 끝 |

NIST 4 Function 정합성(Q6 첫 90일용)은 `08_ai_rmf_profile.md`에 이미 더 상세히 있어 별도로 옮기지 않았다.
