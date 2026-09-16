# 참조 모델 — Policy · Enforcement · Evidence · Assessment

> **이 문서가 포트폴리오의 최상위 뼈대다.** `02_portfolio.md`보다 먼저 보여준다.
>
> **왜 필요한가.** 지금까지의 자료는 `tmac.yaml` 한 파일로 1.1(정책 설계)과 1.2(검증 기준)를 동시에
> 주장했다. 그러면 **정책(policy)과 가드레일(guardrail)이 구별되지 않는다.** 구별되지 않으면
> "policy-as-code를 설계했다"는 주장이 "탐지기 설정 파일을 썼다"와 같은 말이 된다. AI GRC 역할
> 면접에서 가장 먼저 무너질 지점이다.
>
> 계층 어휘는 **내가 만든 것이 아니라** 세 참조 문서에서 가져왔다. 출처를 각 절에 표기했다.

---

## 1. 통제 원칙 — 다섯 계층

**출처** `03. NIST AI RMF Profile` §6 Target Control Architecture, 통제 원칙

> **Model proposes. Harness authorizes. Policy decides. Guardrail enforces. Evidence proves.**

| # | 계층 | 책임 | 질문 |
|---|---|---|---|
| **L1** | **Model** | 사용자 요청과 데이터를 바탕으로 action **candidate를 제안**한다 | 무엇을 하려 하는가 |
| **L2** | **Harness** | Model output을 **구조화**하고 실행 가능한 action인지 확인한다 | 이게 형식적으로 유효한 요청인가 |
| **L3** | **Policy (PDP)** | Identity·tool·resource·parameter·context를 근거로 **실행 여부를 결정**한다 | 이게 허용되는가 |
| **L4** | **Guardrail (PEP)** | 정책 결정을 **runtime에 집행**한다 | 결정이 실제로 강제되는가 |
| **L5** | **Evidence** | input·context·policy version·decision·approval·실행 결과를 **연결하여 기록**한다 | 나중에 증명할 수 있는가 |

여기에 독립 계층 하나가 더 붙는다.

| **L6** | **Assessment** | 위 다섯 계층이 설계대로 작동하는지 **독립적으로 검증**한다 | 믿을 수 있는가 |

**출처** L6은 NIST MEASURE·MANAGE(§5.3, §5.4)와 `05. MS RAI v2 운영모델`의 QE/TEVV·Internal Audit 역할에서 온다.

### 실행 순서

    Identity / Session Context
      → Email Search / Retrieval
      → Prompt/Context Builder
      → Model                          ← L1 제안
      → Action Candidate
      → Schema / Parameter Validation  ← L2 확인
      → Policy Decision Point          ← L3 결정: ALLOW / DENY / REQUIRE_APPROVAL
      → Policy Enforcement Point       ← L4 집행
      → Email / Calendar Tool
      → Execution Evidence / Monitoring ← L5 기록
                                        ← L6 독립 검증 (주기적)

**말할 한 문장**
> **"핵심은 모델의 판단과 실행 권한을 분리하는 것입니다. 에이전트가 action을 제안할 수는 있지만, 실제 도구 실행은 별도의 결정론적 authorization과 runtime 집행, 그리고 증거 체계를 통과해야 합니다."**

---

## 2. Policy와 Guardrail을 구별하는 기준

이 표가 이 문서의 존재 이유다. **둘 다 "차단"을 하지만 성질이 다르다.**

| 구별 축 | **Policy (L3, PDP)** | **Guardrail (L4, PEP)** |
|---|---|---|
| 성격 | **선언적** — 무엇이 허용되는가 | **실행적** — 결정을 강제하는 기계 |
| 산출물 | 결정(ALLOW / DENY / REQUIRE_APPROVAL) | 집행 결과(차단됨 / 통과됨 / 승인 대기) |
| 변경 절차 | **승인을 경유한다.** 버전이 올라간다 | 배포로 바뀐다. 튜닝 대상이다 |
| 변경 주체 | **AI GRC** (기준) | **Control Owner** / Developers (튜닝) |
| 근거 | identity·tool·resource·parameter·context | 점수·임계값·패턴·속도 |
| 실패 양상 | 정책이 **없거나 모호함** | 정책은 있는데 **집행되지 않음** 또는 **우회됨** |
| 증거에 남는 것 | `policy_version` + `decision` + `decision_reason` | `enforcement_result` + `matched_rule` + `score` |
| 감사에서의 위치 | 감사 **기준** | 감사 **대상** |
| 독립성 요건 | — | **agent runtime 밖에 있어야 한다** (AWS) |
| 실패 시 거동 | — | **fail-safe: DENY / STOP / REQUIRE_APPROVAL** (AWS) |

**핵심 구별 질문 세 개** — 어떤 설정을 보고 policy인지 guardrail인지 판단할 때.

1. **변경 시 governance approval이 필요한가?** 필요하면 **policy** — 허용·금지·책임 경계가 바뀌는 것이다. guardrail 변경은 정해진 운영 권한 내 tuning이다.
2. **evidence가 해당 `policy_version`에 binding되어야 하는가?** 그래야 하면 **policy**. guardrail은 rule·config version을 별도 기록하면 된다.
3. **동일한 policy intent를 유지한 채 enforcement implementation을 교체·튜닝할 수 있는가?** 가능하면 **guardrail** — policy 자체는 유지되고, 같은 policy를 만족하는 다른 구현으로 갈아탈 수 있다.

**③이 가장 실용적인 판별식이다.** `detector_engine.py`를 DistilBERT에서 다른 모델로 바꿔도 "외부 데이터의 지시가 시스템 권한을 바꾸지 못하게 한다"는 policy는 불변이다 → **탐지기는 guardrail**. 반면 `B-02 rag_retrieval`의 `trust_level`을 바꾸면 허용 범위 자체가 달라진다 → **policy**.

**두 문장으로 정리**
- "어떤 경계를 신뢰할 수 없다고 선언한다" → **trust assumption 또는 normative requirement가 바뀌는 것** → **Policy change에 가깝다**
- "탐지 룰의 threshold·pattern·detector를 조정한다" → **동일한 policy intent 안에서 enforcement를 조정하는 것** → **Guardrail tuning에 근접하다**

`tmac.yaml`의 `trust_level`이 문자 그대로 trust assumption의 선언이다.

**기본값 규칙** 이 구분은 이진이 아니다. 중간에 걸리는 항목은 **policy로 분류하고, 어디까지를 운영 권한 내 tuning으로 위임할지 명시한다.** 보수적으로 잡고 위임을 여는 방향이 반대보다 안전하다. **이 분류 규칙 자체가 policy다.**

(독립 monitor가 필요한 근거는 이 판별식이 아니라 AWS SRA의 Scope 3 요건이다 — §4-3.)

**말할 것**
> "정규식 룰 하나를 고치는 것과 어떤 경계를 untrusted로 선언하는 것은 둘 다 '차단'에 영향을 주지만, **승인 절차가 달라야 합니다.** 전자는 튜닝이고 후자는 정책 변경입니다. 이게 섞이면 두 가지 문제가 생깁니다 — 룰 튜닝마다 승인을 받아야 하니 실무에서 승인을 우회하게 되고, 반대로 policy version이 튜닝마다 올라가서 증거의 policy_version이 의미를 잃습니다."

---

## 3. 내 자산을 이 모델에 놓으면 — 진단

### 3-1. `tmac.yaml`은 한 파일이 5계층을 담고 있다

| `tmac.yaml`의 절 | 실제 계층 | 판정 |
|---|---|---|
| `boundaries` (B-01~05, `trust_level`, `data_classification`) | **L3 Policy** | 선언 — 정책이 맞다 |
| `threats[].boundary`, `severity`, `category` | **L3 Policy** | 위협 분류 — 정책이 맞다 |
| `threats[].response.action` (`block`/`sanitize_and_log`/`warn_and_confirm`/`throttle`) | **L3 Policy 결정** | 정책이 맞다 |
| `threats[].detection.rules` (정규식 11개 + `confidence`) | **L4 Guardrail** | ⚠️ **정책 파일 안에 탐지 구현이 들어 있다** |
| `detection.method` (`rule_engine` / `chain_accumulator` / `rate_limiter` / `intent_mismatch`) | **L4 Guardrail** | ⚠️ 같은 문제 |
| `tool_risk_scores`, `risk_threshold`, `window_size` | **L4 튜닝 파라미터** | ⚠️ 같은 문제 |
| `policies.risk_score_threshold` | **L4 튜닝 파라미터** | ⚠️ 같은 문제 |
| `eval_store` (테이블·색인·보관 90일) | **L5 Evidence** 설정 | 위치는 타당 |
| `test` 정의 (특허 스키마) | **L6 Assessment** | 위치는 타당 |
| `policies.closed_loop` (`semi_auto`, `approval_required`) | **L3 변경 승인** | 정책이 맞다 |

**진단 문장 (그대로 말한다)**
> **"지금 이 파일은 정책과 가드레일을 한 곳에 담고 있습니다. 특허의 의도는 그 둘을 동기화하는 것이었고 그건 맞습니다. 그런데 거버넌스 관점에서 보면 동기화와 혼재는 다릅니다. 하나의 정의에서 파생시키는 것과, 하나의 파일에 섞어 두는 것은 다른 설계입니다. 지금은 후자입니다."**

### 3-2. 계층을 분리하면 E2E 실패가 설명된다 ★

이 구별 부재가 **관념적 문제가 아니라는 증거**가 이미 있다. E2E 실패 13건 중 **11건이 계층 혼재의 증상**이다.

| 실패 분류 | 건수 | 계층 관점의 원인 |
|---|---:|---|
| (a) 위협 귀속 오류 | 8 | **평가 순서가 정책에 선언되어 있지 않다.** 순서는 "어느 위협을 먼저 적용하는가"이므로 **L3 정책 사항**인데, 실제로는 `gateway.py`가 dict를 순회하고 첫 매칭에서 반환하는 **L4 구현에 암묵적으로** 들어 있다. 그래서 정책 파일을 읽어도 어느 ID로 기록될지 알 수 없다 |
| (b) 집행 누락 | 3 | **L3에 선언됐는데 L4가 집행하지 않았다.** 선언과 집행이 분리되어 있지 않으면 이 차이를 **구조적으로 탐지할 방법이 없다** — 파일에 있으니 있는 줄 알게 된다 |
| (c) 과차단 | 1 | L4 임계값 문제 (계층 혼재와 무관) |
| (d) 미차단 | 1 | L4 탐지 설계 문제 (계층 혼재와 무관) |

**말할 것 — 이게 가장 강한 논증이다**
> (관측) "실패 13건 중 11건이 두 종류입니다. 8건은 차단은 되는데 위협 ID가 다르게 기록되고, 3건은 파일에 선언됐는데 집행되지 않았습니다."
>
> (해석) "**둘 다 정책과 가드레일을 구별하지 않은 결과입니다.** 평가 순서는 정책 사항인데 구현의 dict 순회 순서에 들어 있었고, 선언과 집행이 같은 파일에 있으니 '선언했는데 집행 안 됨'이라는 상태를 구조적으로 볼 수 없었습니다. **제가 만든 것에서 이 문제가 실제로 발생했기 때문에 이 구별이 필요하다고 말씀드리는 겁니다.**"

### 3-3. 없는 계층 두 개 — 정직하게 밝힌다

| 없는 것 | 무엇인가 | 왜 중요한가 | 현재 상태 |
|---|---|---|---|
| **L2 Harness** | Model output의 **schema·parameter 검증** | 모델 출력을 검증 없이 tool call로 파싱하면 data→control 전환 지점이 무방비다 (자체 seeded 결함 **V4**가 정확히 이것) | `tmac.yaml`에 없다. T-04c/T-04d가 부분적으로 겹치지만 **스키마 검증은 없다** |
| **L4의 안전 장치** | **Automated containment / Human override / Fail-safe** | AWS가 Scope 3 이상에서 필수로 제시 | **전부 없다** |

### 3-4. 가장 심각한 것 — 현재 설계는 fail-open이다 ★

**출처** `04. AWS SRA Agentic Scoping Matrix` — `Fail-safe = control failure나 불확실한 상태가 발생하면 위험한 action을 계속하는 대신 안전한 상태로 전환하는 것`. 예시: `authorization service 응답 없음 → action 실행이 아니라 DENY / STOP / REQUIRE APPROVAL`

내 구현은 반대다.

| 위치 | 코드 | 거동 |
|---|---|---|
| `tmac.yaml` | `policies.default_action: allow` | 위협 미탐지 시 **통과** |
| `gateway.py` | `default = self._policies.get("default_action", "allow")` | 정책 로드 실패 시에도 기본값이 allow |
| `signal_engine.py` | `# LlamaGuard 실패 시 안전하게 통과 (false negative 감수)` | 탐지기 장애 시 **통과** |

**용어가 충돌하고 있다.** 코드 주석은 "안전하게 통과"라고 쓰는데, 그건 **가용성 관점의 안전**이고 **보안 관점의 fail-safe와 정반대**다. AWS 기준으로는 `DENY / STOP / REQUIRE_APPROVAL`로 가야 한다.

**말할 것 (물어보면, 또는 먼저 꺼내도 좋다)**
> "제 구현은 fail-open입니다. 탐지기가 죽으면 통과시킵니다. 코드 주석에는 '안전하게 통과'라고 써 있는데, **그건 서비스 가용성 관점의 안전이고 보안 관점에서는 반대 방향입니다.** AWS SRA 기준으로는 authorization이 응답하지 않을 때 실행이 아니라 DENY나 승인 요구로 가야 합니다. 이건 제 PoC의 결함이고, **용어를 혼동하면 이런 설계가 나온다는 사례로 쓰고 있습니다.**"

이 대목이 "자기 산출물을 참조 프레임으로 비판할 수 있는가"를 보여준다. 프레임을 읽기만 한 것과 **자기 것에 적용해 본 것**의 차이다.

---

## 4. 소유권 축 — 누가 무엇을 통제하는가

계층이 "무엇을"이라면, 이 축은 "누가"다. **외부 SaaS를 심사할 때 이 축이 먼저 결정된다.**

### 4-1. Generative AI Scope 1~5 — 통제 범위의 경계

**출처** `04. AWS SRA Generative AI Security Scoping Matrix` — "Application, data, model 중 누가 무엇을 control하는가"

| Scope | AWS 분류 | 내가 통제하는 것 | Provider가 통제하는 것 | 주 통제 초점 |
|---|---|---|---|---|
| 1 | Consumer app | 고객 데이터와 사용 방식만 | application·학습·모델 전부 | **acceptable-use policy, 데이터 분류, DLP, 사용자 교육** |
| 2 | Enterprise app | 고객 데이터, user/access, 사용 정책 | application과 기반 모델 | Scope 1 + **계약·보증·opt-out·data-use 조건** |
| 3 | Pre-trained model | **application 전체** + 고객 데이터 | 사전학습 모델과 학습 데이터 | + **application security, IAM/authorization, 입출력 검증, RAG/tool 접근, 로깅·모니터링** |
| 4 | Fine-tuned model | Scope 3 + fine-tuning 데이터·커스텀 모델 | 기반 모델·원 학습 데이터 | + 학습데이터 보호, poisoning 방지, 모델 산출물 보호 |
| 5 | Self-trained | 전부 | 없음 | + 학습 파이프라인·모델 lifecycle 전체 |

**내 PoC의 좌표 — 이걸 밝히는 게 중요하다**

| 자산 | Gen Scope | 근거 |
|---|---|---|
| `tmac-poc` | **Scope 3** | Ollama `llama3.2:3b` 온프레미스 — 모델은 받아 쓰고 application은 내가 만들었다 |
| `claude-lab` | **Scope 2~3** | Bedrock provider API + 내가 만든 에이전트·mock 도구 |

**말할 것**
> "**JD가 말하는 3rd-party AI SaaS는 보통 Scope 1~2이고, 제 PoC는 Scope 3입니다.** 이 차이가 제 공백의 정확한 이름입니다. Scope 3에서는 입출력 검증과 authorization을 제가 직접 구현할 수 있었지만, Scope 1~2에서는 같은 통제를 **계약과 증빙 요구로 대체**해야 합니다. 묻는 항목은 같고 확보 수단이 다릅니다."

→ 이것이 `04_saas_review_checklist.md`의 이론적 근거다.

### 4-2. Agentic Scope 1~4 — 자율성과 행동 권한

**출처** `04. AWS SRA Agentic AI Security Scoping Matrix` — "Agent에게 무엇을 할 권한을 주며, 어느 정도까지 human approval 없이 행동하게 할 것인가"

| Scope | AWS 명칭 | Agency | Autonomy / 사람 감독 | 주 security focus |
|---|---|---|---|---|
| 1 | No Agency | 없음 — 읽기 전용, 고정 워크플로 | 없음 | workflow integrity, injection 방지, 실행 간 isolation, 입출력 검증, audit |
| 2 | Prescribed Agency | 제한 — 시스템 변경 capability는 있음 | **결과 있는 action은 사람 승인 필수** | **승인 워크플로 보호, authorization bypass 방지, approver 신원 검증, 승인 기록** |
| **3** | **Supervised Agency** | **높음 — 시스템 변경·동적 도구 선택 가능** | **높음 — 사람이 시작하지만 이후는 자율 실행** | **runtime action 모니터링, agency boundary, scope creep, identity propagation, behavioral anomaly, kill switch** |
| 4 | Full Agency | 전면 — 다중 시스템 오케스트레이션 | 전면 — 스스로 시작, 지속 운영 | 지속적 behavioral validation, capability drift, 자동 격리, tamper-resistant human override, fail-safe |

**내 PoC의 좌표**

| 자산 | Agentic Scope | 근거 |
|---|---|---|
| `tmac-poc` | **Scope 3** | 사용자가 시작하지만 에이전트가 도구를 자체 선택해 실행한다. `policy_gate`가 있으나 승인은 **통과(pass-through)** |
| `claude-lab` | **Scope 3** | 동일. `policy_gate`가 `evaluated: false`인 통과 노드 |

**여기서 나오는 정직한 지적 — 스스로 말한다**
> "**제 PoC는 Agentic Scope 3인데, Scope 3가 요구하는 통제 중 kill switch와 자동 격리가 없습니다.** Scope 2로 낮추려면 결과 있는 action에 사람 승인을 필수로 걸어야 하는데, 제 `policy_gate`는 자리만 잡아 둔 통과 노드입니다. **즉 저는 Scope 3 시스템을 만들고 Scope 1 수준의 통제를 붙인 상태입니다.** 이 격차를 아는 것이 제가 이 프레임을 읽고 얻은 것입니다."

### 4-3. Scope 3 이상에서 요구되는 runtime 구조

**출처** 같은 문서

    Primary Agent
      │ action / telemetry
      ▼
    Independent Monitor          ← rule/policy · behavioral baseline · ML/AI anomaly detector
      ▼
    Containment Controller       ← throttle · revoke permission · isolate session · STOP
      ▼
    Human Override               ← tamper-resistant = 최종 human authority
                                   Fail-safe = control 실패 시 안전한 default

| 용어 | 의미 | 예시 |
|---|---|---|
| Agency boundary enforcement | 허용된 tool·resource·action·permission 범위 밖으로 나가지 못하도록 **runtime에서 강제** | `read_calendar`만 허용된 agent가 `send_email` 호출 → policy layer에서 DENY |
| Automated containment | policy violation 감지 시 **사람을 기다리지 않고** 영향 범위를 축소·격리 | 비정상 tool call 반복 → 세션 중단, tool revoke, agent isolation |
| Tamper-resistant human override | 사람이 강제 중지할 수 있고, **그 수단을 agent가 수정·우회할 수 없다** | kill switch를 **agent runtime 밖 control plane**에 둔다 |
| Fail-safe | control 실패 시 위험한 action을 계속하는 대신 안전한 상태로 | authorization 무응답 → **DENY / STOP / REQUIRE_APPROVAL** |

**핵심** Independent Monitor가 **primary agent와 분리**되어야 하고, kill switch가 **agent runtime 밖**에 있어야 한다. 이게 L4 Guardrail의 독립성 요건이고, **정책 파일 안의 정규식으로는 충족되지 않는다.**

---

## 5. 역할 축 — 누가 각 계층을 소유하는가

**출처** `05. MS RAI v2 운영모델` (역할별 핵심 Accountability), `03. NIST Profile` GOVERN 2.1 — "Policy Owner, Implementation Owner, Assurance Owner 및 Risk Owner의 책임을 구분한다"

| 계층 | 소유 역할 | Accountability (MS RAI v2 표현) |
|---|---|---|
| L3 Policy | **AI GRC** ← 내 자리 | 기준·분류·oversight·gap escalation 체계의 운영 |
| L4 Guardrail | **Control Owner** (Assurance) | 특정 control의 설계, 구현 상태 및 효과성 |
| L4 구현 | Development Owner | 설계·코드·모델 통합 및 기술적 remediation |
| L5 Evidence | AI System Owner | AI system이 승인된 요구사항과 control을 충족하도록 운영 |
| L6 Assessment | **QE/TEVV Owner** (Assurance) | 평가 방법의 적절성과 시험 결과의 신뢰성 |
| L6 독립 보증 | **Internal Audit** (Assurance) | governance와 control이 설계대로 작동하는지 독립적으로 보증 |
| 잔여위험 | **Risk Owner** | residual risk의 수용·완화·회피·이전 결정 |
| 배포 판단 | **Release Approver** (Assurance) | release criteria와 evidence를 근거로 한 Go/No-go — **내 자리가 아니다** |

### 이 표가 JD를 정확히 갈라준다 ★

| JD 항목 | 계층 | 역할 | 근거 자산 (이제 겹치지 않는다) |
|---|---|---|---|
| **1.1** Framework & Policy-as-Code | **L3 Policy** 설계 + 개발팀 가이드 | **AI GRC** | `tmac.yaml`의 `boundaries` + `response.action` + `closed_loop` |
| **1.2** Assurance Partnering | **L6 Assessment** 기준 정의 | QE/TEVV 기준을 정의하고 Assurance가 실행 | `tmac.yaml`의 `test` 정의 + **E2E 141/154** + `claude-lab` 계층 능력 행렬 |
| **1.3** AI Risk Evaluation | **L1~L4 위협 식별 + 통제 선택** | AI GRC | `langgraph-tb-analysis`(경계 식별) + KICS 논문(탐지) + `threats` 절 |
| **1.4** Cross-Functional | **계층 간 역할 정렬** | — | 경력 (같은 파일을 개발팀·검증팀·기획이 다르게 읽는다) |
| **1.5** Enterprise AI Policy Owner | **L3 기준·분류 + Scope 판정 + escalation** | **AI GRC** — 승인은 Assurance(Release Approver) | `closed_loop.approval_required` + 규제 판정 + Scope 1~5 |

**말할 것 — 이게 이 문서를 만든 이유다**
> "이전에는 1.1과 1.2의 근거가 둘 다 같은 파일이었습니다. **계층을 나누면 갈립니다.** 1.1은 경계 선언과 정책 결정이고, 1.2는 그 정책이 집행됐는지 확인하는 기준입니다. **제 E2E 실패 13건이 정확히 1.2가 없으면 어떻게 되는지를 보여줍니다** — 1.1은 잘 써 뒀는데 11건이 집행 단계에서 어긋났습니다."

---

## 6. NIST 4 Function과의 대응 — 전체 정합성

**출처** `03. NIST AI RMF Profile` §5, §9

> GOVERN establishes the decision criteria, MAP identifies where risks arise based on those criteria, MEASURE evaluates the magnitude of the risks and the effectiveness of controls, and MANAGE treats and continuously tracks the risks based on the results.

| Function | 핵심 질문 | 내 계층 | 내 자산 |
|---|---|---|---|
| **GOVERN** | 어떤 원칙과 책임으로 관리할 것인가 | L3 Policy + 역할 | `boundaries`·`trust_level` 선언, `closed_loop` 승인, 규제 판정 |
| **MAP** | 어디에서 어떤 위험이 발생하는가 | L1~L4 경계 식별 | data/control/privilege 3축, L0~L8 / TB-1~9, 특허 Threat Taxonomy |
| **MEASURE** | 위험이 실제로 얼마나 발생하는가 | **L6 Assessment** | E2E 141/154, threshold sweep N=50, 계층 능력 행렬, 재호출 이탈률 |
| **MANAGE** | 측정된 위험을 어떻게 처리·추적할 것인가 | L4 집행 + L5 기록 + 재갱신 | `response.action`, Risk Calculator, `proposed_update.yaml`, 이벤트 90일 |

### NIST Profile이 요구하는 Validation Criteria ↔ 내가 가진 Evidence

**출처** `03. NIST Profile` §7

| Control Objective | Validation Criteria | Required Evidence | 내 상태 |
|---|---|---|---|
| 메일 본문의 instruction이 시스템 권한을 변경하지 못하게 한다 | 악성 instruction이 추가 tool 권한이나 외부 전송을 발생시키지 않는다 | 공격 test 결과, action trace, 최종 decision | **부분** — T-01 룰 11개 + E2E, 단 EP-001 미차단 1건 |
| 모든 tool action을 독립적으로 authorization한다 | model이 생성한 action은 policy evaluation 없이 실행되지 않는다 | Gateway log, policy decision, execution log | **부분** — Gateway는 있으나 귀속 오류 8건 |
| 고위험 action에는 human approval을 요구한다 | 외부 전송·신규 수신자·민감정보 포함 action은 승인 전 미실행 | Approval request, approver identity, 승인 전 미실행 | ❌ **없음** — `policy_gate`가 통과 노드 |
| 최소권한을 적용한다 | 승인된 mailbox·calendar·tool·action에만 접근 | IAM/OAuth scope, access policy, negative test | ❌ **미측정** |
| 개인정보 전달을 최소화한다 | 모델에 최소 데이터만 전달 | data-flow diagram, request log, masking 결과 | ❌ **없음** — masking 미구현 |
| **실행 과정을 사후 추적할 수 있다** | **source–decision–policy–approval–action을 동일 run에서 연결** | **run ID, source reference, policy version, action evidence** | ✅ **`claude-lab`이 이것을 정량 측정한 것** — 단 `policy_version` 연결은 미구현 |
| 통제 변경 후 회귀를 방지한다 | policy·model 변경 후 기존 정상·공격 test 반복 | versioned test suite, regression report | **부분** — E2E는 있으나 정책 버전과 연동 안 됨 |

**이 표를 쓰는 방법**
> "제 자료가 이 Control Objective 7개 중 어디에 있는지 표시했습니다. **두 개는 있고, 세 개는 부분이고, 세 개는 없습니다.** 특히 human approval evidence가 없는 게 Agentic Scope 3에서 가장 큰 공백입니다. **이 빈칸을 아는 것이 제가 첫 90일에 할 일의 목록입니다.**"

---

## 7. 이 문서를 인터뷰에서 쓰는 방법

### 배치

| 순서 | 무엇 | 시간 |
|---|---|---|
| 1 | **§1 다섯 계층 + 통제 원칙 한 문장** | 1분 — 여기서 프레임을 잡는다 |
| 2 | **§2 Policy vs Guardrail 구별 표** | 1분 — "제가 구별하는 기준입니다" |
| 3 | §5 JD 항목 ↔ 계층 대응 | 30초 — 이후 1.1~1.5가 이 표의 행으로 들린다 |
| 4 | (1.1~1.5 진행) | — |
| 5 | **§3-2 계층 혼재가 E2E 실패를 설명한다** | 1.2에서 |
| 6 | **§3-4 fail-open 자기 진단** | Q&A 또는 1.2 끝 |
| 7 | §4 Scope 좌표 | Q2(외부 SaaS) 받으면 |
| 8 | §6 Control Objective 7개 중 내 위치 | 첫 90일 질문(Q6) 받으면 |

### 이 문서가 답해 주는 질문

| 질문 | 답이 있는 절 |
|---|---|
| "그래서 policy를 만드신 건가요, guardrail을 만드신 건가요?" | §2 + §3-1 |
| "정책이 실제로 집행됐다는 건 어떻게 압니까?" | §3-2 + §6 |
| "우리는 외부 SaaS를 씁니다. 직접 만든 것과 뭐가 다릅니까?" | §4-1 Scope 1~5 |
| "에이전트에 어디까지 권한을 줘야 합니까?" | §4-2 Scope 1~4 |
| "이 역할과 Assurance팀의 경계가 어디입니까?" | §5 역할 표 |
| "첫 90일에 뭘 하시겠습니까?" | §6 빈칸 목록 |

### 규율

1. **계층 어휘는 내가 만든 게 아니다.** NIST Profile §6, AWS SRA 2종, MS RAI v2에서 왔다고 출처를 밝힌다. "제가 프레임워크를 만들었다"고 말하지 않는다.
2. **§3의 진단은 자기 비판이다.** 방어적으로 말하지 말고 담담하게 말한다. 프레임을 자기 것에 적용해 본 결과라는 게 요점이다.
3. **fail-open은 결함이다.** "의도한 설계"라고 포장하지 않는다.
4. **Scope 좌표를 먼저 말한다.** 내 PoC는 Gen Scope 3 / Agentic Scope 3이고 JD의 대상은 Gen Scope 1~2다. 이 차이를 숨기면 나머지가 과장이 된다.
5. NIST Profile은 **공식 NIST Profile이 아니다.** 문서 자신이 "NIST가 제공한 공식 Profile이 아니라 use-case Target Profile"이라고 밝히고 있다. 그대로 말한다.
