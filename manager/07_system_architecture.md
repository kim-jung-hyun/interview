# AI System 구조 — Model · Harness · Policy · Evidence · Test · E2E Test

> **책임 체계(`06_ai_responsibility.md`)를 실제로 작동시키기 위한 시스템 구조다.**
> 역할이 책임을 지려면 **그 역할이 붙잡을 지점이 시스템에 있어야 한다.** 이 문서는 그 지점을 정의한다.
>
> **근거** `03. NIST AI RMF Profile` §6 Target Control Architecture · §7 Validation Criteria / `04. AWS SRA Agentic AI Scoping Matrix` / `06. 특허` 구성요소
>
> **기준선** `02_structure.md` §0. 이 문서는 **내 산출물 ①(개발팀용 기준이 SW 구조로 들어간 형태)**과 **②(Assurance가 쓸 evidence·audit 구조)**를 동시에 정의한다.
>
> 그림: `figures/architecture.dot` / `.svg`

---

## 1. 통제 원칙

**출처 원문** — NIST Profile §6

> **Model proposes. Harness authorizes. Policy decides. Guardrail enforces. Evidence proves.**

여기에 검증 계층을 더하면 **Test verifies.**

**핵심** 모델의 **판단**과 실행 **권한**을 분리한다.

> (원문) AI assistant가 action을 제안할 수는 있지만, 실제 tool 실행은 별도의 deterministic authorization, runtime enforcement 및 evidence 체계를 통과해야 한다.

---

## 2. 여섯 구성요소

| # | 요소 | 책임 | 질문 | 이 요소가 없으면 |
|---|---|---|---|---|
| 1 | **Model** | 사용자 요청과 데이터로 action **후보를 제안**한다 | 무엇을 하려 하는가 | — |
| 2 | **Harness** | 모델 출력을 **구조화**하고 실행 가능한 action인지 확인한다 (schema·parameter 검증) | 형식적으로 유효한가 | 모델 출력이 검증 없이 tool call로 파싱된다 — **데이터가 명령으로 바뀌는 지점이 무방비** |
| 3 | **Policy (PDP)** — Policy Decision Point | 정책을 평가해 **`ALLOW`/`DENY`/`REQUIRE_APPROVAL` 결정을 내린다** | 허용되는가 | 판단 기준이 코드에 흩어진다. 누가 바꿨는지 알 수 없다 |
| 4 | **Guardrail (PEP)** — Policy Enforcement Point | 그 결정을 **실제 요청·행동 경로에서 강제(enforce)한다** | 결정이 실제로 강제되는가 | 정책이 문서로만 존재한다 |

**PDP와 PEP의 실제 호출 순서**

    Request / Action  →  PEP  →  PDP  →  Decision  →  PEP Enforcement

**PEP가 먼저 온다.** 실행 경로에 앉아 요청을 가로채고, PDP에 물어보고, 돌아온 결정을 강제한다. §3의 선형 그림은 이걸 펼쳐 놓은 것이다 — **결정이 집행보다 먼저라는 뜻이지, PDP가 경로에 앉아 있다는 뜻은 아니다.**
| 5 | **Evidence** | 입력·context·**정책 버전**·결정·승인·실행 결과를 **연결해 기록**한다 | 나중에 증명할 수 있는가 | 무엇이 왜 일어났는지 사후에 알 수 없다 |
| 6 | **Test / E2E Test** | 위 다섯이 **설계대로 작동하는지 검증**한다 | 믿을 수 있는가 | **선언과 집행의 차이를 구조적으로 볼 수 없다** |

### Policy와 Guardrail은 왜 따로인가

| | **Policy (PDP)** | **Guardrail (PEP)** |
|---|---|---|
| 성격 | 선언적 — 무엇이 허용되는가 | 실행적 — 결정을 강제하는 기계 |
| 산출물 | **ALLOW / DENY / REQUIRE_APPROVAL** | 집행 결과 |
| 변경 절차 | **승인 경유. 버전이 올라간다** | 배포로 바뀐다. 튜닝 대상 |
| 소유 역할 | **AI GRC** ← 내 자리 | **Control Owner** (Assurance) |
| 실패 양상 | 정책이 없거나 모호함 | 정책은 있는데 **집행되지 않거나 우회됨** |
| 감사 위치 | 감사 **기준** | 감사 **대상** |

**구별 질문 세 개**
① **변경 시 governance approval이 필요한가** — 필요하면 Policy
② **evidence가 해당 policy version에 binding되어야 하는가** — 그래야 하면 Policy
③ **동일한 policy intent를 유지한 채 enforcement implementation을 교체·튜닝할 수 있는가** — 가능하면 Guardrail

**③의 적용 — 두 문장**
- "어떤 경계를 신뢰할 수 없다고 선언한다" → **trust assumption / normative requirement 변경** → **Policy change에 가깝다**
- "탐지 룰의 threshold·pattern·detector를 조정한다" → **동일 policy intent 내 enforcement 조정** → **Guardrail tuning에 근접하다**

**기본값 규칙** 중간에 걸리는 항목은 **policy로 분류하고 운영 권한 내 tuning 위임 범위를 명시한다.** 이 분류 규칙 자체도 policy다.

### Test와 E2E Test는 왜 따로인가

| | **Test** | **E2E Test** |
|---|---|---|
| 대상 | 요소 하나 | **경계를 통과하는 전체 경로** |
| 확인하는 것 | 이 요소가 명세대로 동작하는가 | **선언된 통제가 실제로 집행되는가** |
| 예 | 정책 파서가 YAML을 맞게 읽는가 | 악성 입력이 실제 tool 실행까지 도달하지 못하는가 |
| 잡아내는 것 | 구현 버그 | **정의와 집행의 불일치 (drift)** |
| 소유 역할 | Development Owner | **QE / TEVV Owner** |

**말할 것 — 이 구분이 이 문서의 핵심이다**
> "**단위 테스트는 '내가 만든 게 내 명세대로 동작하는가'를 봅니다. E2E 테스트는 '내 명세가 실제로 집행되는가'를 봅니다.** 둘은 다른 질문이고, 거버넌스가 필요한 건 후자입니다.
>
> 제 PoC에서 실제로 그 차이가 나왔습니다 — **경계 테스트 154건 중 13건이 실패했고, 그중 11건이 '정책 파일에는 선언됐는데 집행이 어긋난' 경우**였습니다. 특히 8건은 차단은 되는데 위협 ID가 다르게 기록돼서 **로그만 보면 정상으로 보입니다.** 단위 테스트로는 절대 안 잡힙니다."

---

## 3. 실행 흐름

    Identity / Session Context
        ↓
    외부 데이터 수집 (검색 · RAG · 도구 결과)     ← 신뢰 등급을 여기서 선언한다
        ↓
    Prompt / Context Builder
        ↓
    ┌──────────────┐
    │  1 MODEL     │  action 후보 제안
    └──────┬───────┘
           ↓  Action Candidate
    ┌──────────────┐
    │  2 HARNESS   │  schema · parameter 검증
    └──────┬───────┘
           ↓  구조화된 실행 요청
    ┌──────────────┐
    │  3 POLICY    │  ── ALLOW ──────────────┐
    │     (PDP)    │  ── DENY ───────────▶ 거부 + 기록
    └──────┬───────┘  ── REQUIRE_APPROVAL ─▶ 사람 승인 ──┐
           │                                             │
           ↓◀────────────────────────────────────────────┘
    ┌──────────────┐
    │  4 GUARDRAIL │  runtime 집행
    │     (PEP)    │
    └──────┬───────┘
           ↓
      Tool 실행 (메일 · 캘린더 · DB)
           ↓
    ┌──────────────────────────────────────────────┐
    │  5 EVIDENCE — 위 모든 단계에서 기록이 내려온다      │
    │  입력 · context · 정책버전 · 결정 · 승인 · 실행결과  │
    └──────────────────────────────────────────────┘
           ╎
    ┌──────────────────────────────────────────────┐
    │  6 TEST / E2E TEST — 위 경로를 주입해 검증한다     │
    └──────────────────────────────────────────────┘

### 결정이 세 갈래인 것이 중요하다

`ALLOW` / `DENY` / **`REQUIRE_APPROVAL`**

**왜 세 번째가 필요한가 — 규제가 요구한다**
> "PIPA의 **자동화된 결정** 조항 때문입니다. 완전자동 시스템이 개인의 권리·의무에 중대한 영향을 주는 결정을 하면 정보주체에게 **거부권과 설명요구권**이 발생합니다.
>
> 그래서 통제 어휘가 허용·차단 이진이면 안 됩니다. **'사람 확인을 경유한다'는 결정이 반드시 있어야 하고, 그게 시스템 구조의 분기로 존재해야 합니다.** 규제 요건이 아키텍처의 분기가 되는 지점입니다."

그리고 **AWS Agentic Scope 2**가 요구하는 것이 정확히 이 분기다 — `결과 있는 action은 사람 승인 필수`, 그리고 **승인 기록·approver 신원 검증·승인 우회 방지**.

---

## 4. 실패했을 때 — Fail-safe

**출처 원문** — AWS SRA Agentic Scoping Matrix

> Fail-safe = control failure나 불확실한 상태가 발생하면 위험한 action을 계속하는 대신 **안전한 상태로 전환**하는 것. 예: authorization service 응답 없음 → action 실행이 아니라 **DENY / STOP / REQUIRE APPROVAL**

### Scope 3 이상에서 요구되는 추가 구조

    Primary Agent
        ↓ action / telemetry
    Independent Monitor       ← primary agent와 **분리**되어야 한다
        ↓
    Containment Controller    ← throttle · 권한 회수 · 세션 격리 · STOP
        ↓
    Human Override            ← kill switch를 **agent runtime 밖**에 둔다

| 용어 | 의미 |
|---|---|
| Agency boundary enforcement | 허용된 권한 범위 밖으로 못 나가게 runtime에서 강제 |
| Automated containment | 위반 감지 시 **사람을 기다리지 않고** 영향 범위 축소·격리 |
| Tamper-resistant human override | 사람이 강제 중지할 수 있고 **에이전트가 그 수단을 수정·우회할 수 없다** |
| Fail-safe | 통제 실패 시 **거부·중지·승인 요구**로 전환 |

**말할 것**
> "**Independent Monitor가 감시 대상과 분리되어야 하고, kill switch가 agent runtime 밖에 있어야 합니다.** 정책 파일 안의 룰로는 이게 충족되지 않습니다 — 에이전트가 도는 프로세스 안에 있으면 그 프로세스가 죽을 때 감시도 같이 죽습니다."

---

## 5. 내 PoC를 이 구조에 대조하면 — 자기 진단

| 요소 | 내 구현 | 판정 |
|---|---|---|
| 1 Model | Ollama 온프레미스 / Bedrock | ✅ |
| **2 Harness** | **없다.** schema·parameter 검증 단계가 없다 | ❌ **내가 설계한 검증 실험의 결함 V4가 정확히 이것** — 모델 출력을 검증 없이 tool call로 파싱 |
| 3 Policy | 경계 선언 + 위협별 조치 4종 (`block`/`sanitize`/`warn_and_confirm`/`throttle`) | ⚠️ **가드레일과 한 파일에 섞여 있다** |
| 4 Guardrail | Gateway가 정책 파일을 읽어 집행 | ⚠️ 평가 **순서**가 정책이 아니라 구현에 암묵적으로 있다 |
| 5 Evidence | 위협 이벤트 저장소 (위협ID·세션·조치·시각·심각도, 보관 90일) | ⚠️ **정책 버전이 증거에 연결되지 않는다** |
| 6 Test / E2E | E2E 경계 테스트 154건 | ✅ **작동했다** — 13건 실패를 잡아냈다 |
| **Fail-safe** | **fail-open이다.** 기본 조치가 `allow`, 탐지기 장애 시 통과 | ❌ **보안 fail-safe와 반대 방향** |
| **Human Override / Containment** | **없다** | ❌ Scope 3 시스템인데 Scope 1 수준 통제 |

**말할 것 (먼저 꺼낸다)**
> "이 구조에 제 것을 대조하면 **두 개가 없고 세 개가 어긋납니다.**
>
> 없는 것은 **Harness와 안전장치**입니다. 모델 출력의 스키마 검증 단계가 없고, kill switch와 자동 격리가 없습니다.
>
> 어긋난 것은 **정책과 가드레일이 한 파일에 있다는 것, 평가 순서가 정책이 아니라 구현에 있다는 것, 그리고 정책 버전이 증거에 연결되지 않는다는 것**입니다.
>
> 그리고 가장 심각한 건 **fail-open**입니다. 탐지기가 죽으면 통과시킵니다. 코드 주석에는 '안전하게 통과'라고 써 있는데 **그건 가용성 관점의 안전이고 보안 관점에서는 반대입니다.** 용어를 혼동하면 이런 설계가 나온다는 사례로 쓰고 있습니다."

→ **이 대답이 "프레임을 읽기만 한 것"과 "자기 것에 적용해 본 것"을 가른다.**

---

## 6. 역할이 붙잡는 지점 — 구조와 책임의 연결

이 문서가 `06_ai_responsibility.md`를 위해 존재하는 이유다. **역할이 책임을 지려면 붙잡을 지점이 있어야 한다.**

**기준선 순서로 읽는다.** 기준 → 구현 → 판정 → 수용.

| 기준선 | 역할 | 시스템에서 붙잡는 지점 | 그 지점이 없으면 |
|---|---|---|---|
| **기준** | **AI GRC ← 내 자리** | **Policy 정의 + 개발팀 가이드 + evidence·audit 구조 요건** | 기준이 코드에 흩어지고, **Assurance가 쓸 증거가 안 나온다** |
| **구현** | Development Owner | **Model · Harness · Guardrail 구현** | 기준이 문서에만 남는다 |
| **구현** | AI System Owner | 승인된 통제로 운영 | — |
| **판정** | **Control Owner** | **Guardrail 실행·모니터링과 그 효과성** | 통제가 있다고 말할 근거가 없다 |
| **판정** | **QE / TEVV Owner** | **Test / E2E Test와 그 결과** | "충족됐다"를 확인할 방법이 없다 |
| **판정** | **Release Approver** | **Evidence + Test 결과 → Go/No-go** | 승인이 서명이 된다 |
| **판정** | **Internal Audit** | **Evidence의 무결성과 정책 버전 이력** | 독립 검증 대상이 없다 |
| **수용** | **Risk Owner** | **Evidence에 남은 residual risk** | 무엇을 수용하는지 모르고 수용한다 |
| **수용** | Business Owner | 사업상 위험 판단 | — |

**말할 것 — 이 문서를 닫는 문장**
> "**책임 체계와 시스템 구조는 따로 만들 수 없다고 생각합니다.** Release Approver가 Go/No-go를 하려면 근거가 증거로 남아 있어야 하고, Internal Audit이 독립 검증을 하려면 정책 버전 이력이 있어야 합니다.
>
> 반대로 말하면 **시스템에 붙잡을 지점이 없는 역할은 문서상의 역할입니다.**
>
> **그래서 제 일이 기준을 쓰는 것에서 끝나지 않습니다.** 기준을 쓰고, 그게 SW 구조에 들어가게 개발팀을 가이드하고, **그 구조에서 Assurance가 판정할 증거가 나오게** 하는 것까지입니다. 여기까지가 분리선 ③을 성립시키는 조건입니다."

---

## 7. NIST 통제 목표 대비 현재 위치

**출처 원문** — NIST Profile §7 (Control Objective / Validation Criteria / Required Evidence)

| 통제 목표 | 필요 증적 | 내 상태 |
|---|---|---|
| 외부 데이터의 지시가 시스템 권한을 바꾸지 못하게 한다 | 공격 test 결과, action trace, 최종 decision | **부분** |
| 모든 tool action을 독립적으로 authorization한다 | Gateway log, policy decision, execution log | **부분** — 귀속 오류 존재 |
| 실행 과정을 사후 추적할 수 있다 (출처→결정→정책→승인→action) | run ID, source reference, **policy version**, action evidence | **부분** — 정책 버전 미연결 |
| 통제 변경 후 회귀를 방지한다 | versioned test suite, regression report | **부분** — 테스트가 정책 버전과 미연동 |
| **고위험 action에 human approval을 요구한다** | Approval request, **approver identity**, 승인 전 미실행 | ❌ **없음** |
| **최소권한을 적용한다** | IAM/OAuth scope, access policy, **negative test** | ❌ **미측정** |
| **개인정보 전달을 최소화한다** | data-flow diagram, request log, **masking 결과** | ❌ **없음** |

**말할 것 — 첫 90일 질문에 그대로 쓴다**
> "**4개는 부분이고 3개가 없습니다.** 없는 것이 human approval 증거, 최소권한 negative test, 개인정보 masking입니다.
>
> 그리고 **'부분'인 네 개의 공통 원인이 하나입니다 — 정책 버전이 증거에 연결되지 않는다는 것.** 정책 버전이 없으면 '그때 어떤 기준으로 허용했는가'를 답할 수 없고, 회귀 테스트도 무엇에 대한 회귀인지 알 수 없습니다. **그 한 줄을 먼저 연결하겠습니다.**"
