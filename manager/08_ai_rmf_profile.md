# AI RMF Profile — Use Case 기반

> **근거** `03. NIST AI RMF 1.0 — Use Case 기반 AI RMF Profile`
>
> ⚠️ **이것은 공식 NIST Profile이 아니다.** 문서 자신이 밝히고 있다 — "NIST가 제공한 공식 Profile이 아니라, AI RMF Core에서 해당 use case에 필요한 outcome을 선택하여 구체화한 **use-case Target Profile**"이다. 인터뷰에서 이 문장을 그대로 말한다.
>
> **기준선** `02_structure.md` §0. 이 Profile은 **기준의 출처**다 — GOVERN·MAP이 내 산출물의 근거이고, MEASURE는 판정 항목, MANAGE는 수용·추적이다.
>
> 그림: `figures/rmf_cycle.dot` / `.svg`

---

## 1. 네 Function의 관계

**출처 원문**

> GOVERN establishes the decision criteria, MAP identifies where risks arise based on those criteria, MEASURE evaluates the magnitude of the risks and the effectiveness of controls, and MANAGE treats and continuously tracks the risks based on the results.

| Function | 핵심 질문 | 이 use case에서 |
|---|---|---|
| **GOVERN** | 어떤 원칙과 책임으로 관리할 것인가 | 외부 메일 내용만으로 캘린더 event를 생성하지 못하게 하고, **참석자 초대·외부 링크 등록에는 사용자 승인이 필요하다**는 policy와 책임자를 정한다 |
| **MAP** | 어디에서 어떤 위험이 발생하는가 | 외부 메일이 **trusted data가 아닌 상태로 model context에 들어가고**, model output이 calendar write action으로 **전환되는 boundary**에서 prompt injection 위험이 발생한다고 식별한다 |
| **MEASURE** | 위험이 실제로 얼마나 발생하는가 | 악성 지시가 포함된 test email을 실행하여 **승인 없이 calendar action이 생성된 비율**을 측정한다 |
| **MANAGE** | 측정된 위험을 어떻게 처리하고 추적할 것인가 | 무단 실행이 발견되면 외부 메일 기반 calendar write를 **`REQUIRE_APPROVAL`로 통제**하고, 배포 후 재발생률을 monitoring한다 |

**핵심 순환** MEASURE와 MANAGE의 결과가 **다시 GOVERN의 판단 기준으로 되돌아간다.** 한 바퀴 돌고 끝나는 게 아니다.

### 기준선과의 대응 ★

| Function | 기준선 칸 | 누가 |
|---|---|---|
| **GOVERN** | **기준** | **AI GRC ← 내 자리** — 판단 기준과 책임을 정한다 |
| **MAP** | **기준** | **AI GRC** — 위험 위치를 식별해 통제 요건으로 바꾼다 |
| **MEASURE** | **판정** | **QE/TEVV · Internal Audit (Assurance)** — 위험 크기와 통제 효과성을 검증한다 |
| **MANAGE** | **수용 + 구현** | **Risk Owner**(수용·완화·회피·이전 결정) + **Control Owner·Development**(처리 실행) |

**말할 것**
> "**GOVERN과 MAP이 제 칸이고, MEASURE는 Assurance의 칸입니다.** 제가 MEASURE의 항목을 정의하지만 측정과 판정은 독립적으로 이뤄져야 합니다 — MEASURE 1.3이 '개발자와 분리된 내부 전문가 또는 독립 평가자가 검토한다'고 명시하는 이유가 그것입니다.
>
> **MANAGE 1.3의 accept 결정도 Risk Owner이고 제가 아닙니다.**"

---

## 2. Use Case와 Trust Boundary

**출처 원문** — 이 Profile이 대상으로 삼은 시나리오

### 정상 시나리오
> "메일함에서 특정 메일을 찾아 요약하고, 그 내용을 캘린더에 등록해줘."

`Prompt/Context → Model → Calendar action`

### 공격 시나리오 — 검색된 메일에 악성 instruction이 포함된 경우

- 메일 내용을 외부 주소로 전송하도록 유도
- 공격자의 캘린더 또는 URL을 사용하도록 유도
- 원래 요청에 없던 tool을 호출하도록 유도
- 사용자의 메일이나 다른 민감정보를 추가로 조회하도록 유도
- **Human approval 없이 외부 action을 실행하도록 유도**

**출처 원문 — 이 Profile의 핵심 문장**
> 메일 본문은 업무 데이터로서 읽어야 하지만, **시스템 권한을 지시할 수 있는 trusted instruction은 아니다.** 따라서 검색된 메일의 데이터가 model decision을 거쳐 권한 있는 action으로 전환되는 지점이 **핵심 trust boundary**가 된다.

### 주요 자산과 경계

| 구분 | 내용 |
|---|---|
| 보호 자산 | 메일 본문, 개인정보, 인증정보, 캘린더, 외부 전송 권한, 실행 로그 |
| **비신뢰 입력** | 외부 발신자가 작성한 메일과 첨부 링크 |
| 고권한 기능 | 메일 추가 조회, 외부 전송, 캘린더 생성·수정, 외부 API 호출 |
| **주요 boundary** | 메일→context / **model output→action candidate** / action candidate→tool execution |
| 주요 위협 | Indirect prompt injection, excessive agency, privilege misuse, data exfiltration |
| 주요 영향 | 개인정보 유출, 비인가 action, 업무 운영 피해, 금전·평판 손실 |

**말할 것**
> "이 Profile이 잘 쓴 문장이 하나 있습니다 — **'메일 본문은 업무 데이터로서 읽어야 하지만 시스템 권한을 지시할 수 있는 trusted instruction은 아니다.'**
>
> 이 한 문장이 제 위협 모델링의 출발점과 같습니다. **데이터로 읽어야 하는 것과 명령으로 읽어서는 안 되는 것이 같은 문자열**이라는 게 에이전트 보안의 구조적 문제입니다."

---

## 3. GOVERN Profile

**출처 원문** — Core ID / 적용 목표 / 필요한 구현·증적

| Core ID | 적용 목표 | 필요한 구현·증적 |
|---|---|---|
| **GOVERN 1.1** | 이메일·캘린더·개인정보 처리와 외부 model/provider 사용에 적용되는 **법률 및 규제 요구사항을 식별**한다 | 법률·규제 요구사항 목록, privacy review, provider assessment |
| **GOVERN 1.2** | Trustworthy AI 특성을 **제품 정책과 개발·배포 절차에 통합**한다 | Security/privacy requirement, release criteria, review checklist |
| **GOVERN 1.3** | Use case의 위험 수준에 따라 필요한 **검토·시험·승인 수준을 결정**한다 | Risk tier, human approval 기준, TEVV 수준 |
| **GOVERN 1.4** | 조직의 위험 우선순위에 따라 **risk management process와 control을 수립**한다 | Control objective, risk-treatment decision, exception 기준 |
| **GOVERN 1.5** | 운영 모니터링과 **정기 검토의 책임 및 빈도**를 정의한다 | Control owner, monitoring owner, review schedule |
| **GOVERN 1.6** | AI assistant, model, provider, tool 및 배포 정보를 **inventory로 관리**한다 | AI inventory, model/provider version, data type, owner, approval status |
| **GOVERN 2.1** | **Policy Owner, Implementation Owner, Assurance Owner 및 Risk Owner의 책임을 구분**한다 | **RACI, approval authority, escalation path** |
| **GOVERN 2.3** | 개발·배포 및 residual risk에 대한 **경영진 책임을 명확히** 한다 | Go/no-go 승인, exception/risk acceptance record |
| **GOVERN 4.2** | 시스템 위험과 잠재적 영향을 **문서화하고 관련 조직과 공유**한다 | Threat model, assessment report, residual risk |
| **GOVERN 4.3** | 시험, incident 식별 및 **정보 공유 체계**를 수립한다 | Security test, incident criteria, reporting process |
| **GOVERN 6.1** | Model provider, email/calendar API 및 기타 **제3자 위험을 관리**한다 | Provider assessment, data-use/retention terms, SLA |
| **GOVERN 6.2** | 제3자 API failure 또는 incident에 대한 **비상 프로세스**를 마련한다 | Provider outage plan, credential revoke, fallback 및 shutdown 절차 |

**→ 이 역할과 가장 직접 겹치는 것** GOVERN **2.1**(역할 구분), **1.3**(승인 수준 결정), **1.4**(control 수립), **6.1**(제3자 위험) — 각각 `06_ai_responsibility.md`, `04_adoption_gate.md`가 대응한다.

---

## 4. MAP Profile

| Core ID | 적용 목표 | Use case 적용 결과 |
|---|---|---|
| **MAP 1.1** | Intended use와 예상 배포환경을 정의한다 | 승인된 메일 검색·요약·캘린더 등록 허용 |
| **MAP 1.3** | 조직의 목표를 정의한다 | 업무 생산성 향상과 **비인가 정보 접근 action 방지** |
| **MAP 1.4** | AI를 사용하는 비즈니스 가치를 정의한다 | 반복적인 검색·요약·일정 등록 시간 절감 |
| **MAP 1.5** | **Risk tolerance를 정의**한다 | **비인가 외부 전송과 권한 확대는 허용하지 않음** |
| **MAP 1.6** | 시스템 요구사항을 도출한다 | **메일 본문은 instruction authority를 갖지 않으며, tool action은 별도 authorization을 거쳐야 함** |
| **MAP 2.1** | 시스템이 수행하는 작업을 정의한다 | Search, retrieve, summarize, propose calendar event, create event |
| **MAP 2.2** | **지식 한계와 human oversight**를 문서화한다 | **Model은 메일의 업무 데이터와 악성 instruction을 완벽하게 구분할 수 없다** |
| **MAP 2.3** | 오류와 실패의 잠재적 비용을 식별한다 | 정보유출, 잘못된 일정, 업무 방해, 평판 피해 |
| **MAP 3.3** | 적용 범위를 제한한다 | 승인된 mailbox, calendar, tool만 접근 |
| **MAP 3.5** | **Human oversight를 정의**한다 | **외부 전송·신규 수신자·고위험 action에는 사용자 승인 필요** |
| **MAP 4.1** | 제3자 data·software의 기술적·법적 위험을 매핑한다 | Model provider, email API, calendar API 및 **cross-border data flow** |
| **MAP 4.2** | 내부 통제를 식별한다 | Least privilege, token scope, policy engine, parameter validation, logging |
| **MAP 5.1** | 영향의 가능성과 크기를 식별한다 | 개인정보 유출과 비인가 action의 likelihood/impact 평가 |
| **MAP 5.2** | 사용자와 영향을 받는 actor의 피드백을 반영한다 | 오탐·누락·비인가 action 신고 및 appeal mechanism |

**→ MAP 2.2가 이 Profile 전체의 전제다**
> "**모델은 업무 데이터와 악성 지시를 완벽하게 구분할 수 없다**는 것을 전제로 놓고 시작합니다. 이 전제를 받아들이면 통제 설계가 달라집니다 — 모델을 더 똑똑하게 만드는 방향이 아니라, **모델의 판단과 실행 권한을 분리하는 방향**으로 갑니다. MAP 1.6이 그 결론입니다."

---

## 5. MEASURE Profile — Validation Criteria와 증적

**이 절이 JD 1.2(Assurance Partnering)와 직접 대응한다.**

| Core ID | Validation Criteria | Test / Evidence |
|---|---|---|
| **MEASURE 1.1** | 가장 중대한 위험부터 측정하고, **측정할 수 없는 위험을 문서화**한다 | Indirect prompt injection과 비인가 action을 최우선 시험 |
| **MEASURE 1.2** | 지표와 **통제 효과성을 정기적으로 재평가**한다 | Attack success rate, false allow, false deny, approval rate |
| **MEASURE 1.3** | **개발자와 분리된** 내부 전문가 또는 독립 평가자가 검토한다 | Security review, independent test result |
| **MEASURE 2.1** | Test set, metric과 TEVV 도구를 문서화한다 | 정상·악성 메일 corpus, test case, expected decision |
| **MEASURE 2.3** | **실제 배포환경과 유사한 조건**에서 성능 및 보증 기준을 측정한다 | 실제 tool schema와 권한을 사용한 staging test |
| **MEASURE 2.4** | 운영 중 시스템 기능과 행동을 모니터링한다 | Tool invocation, parameter, **authorization decision log** |
| **MEASURE 2.5** | 정상 use case에서 유효하고 신뢰할 수 있음을 입증한다 | 정상 메일 검색·요약·캘린더 등록 성공률 |
| **MEASURE 2.6** | **안전하게 실패하고** residual risk가 tolerance를 넘지 않음을 확인한다 | **Policy unavailable 시 default deny, timeout과 fallback test** |
| **MEASURE 2.7** | Security와 resilience를 평가한다 | Prompt injection, privilege escalation, token misuse test |
| **MEASURE 2.8** | Transparency와 accountability 위험을 평가한다 | **Decision owner와 action reason을 사후 추적할 수 있는지 확인** |
| **MEASURE 2.9** | Model과 output을 설명·문서화한다 | **Action candidate와 실제 tool execution의 연결 기록** |
| **MEASURE 2.10** | Privacy risk를 평가한다 | Model/provider에 전달된 개인정보, **masking/tokenization 결과** |
| **MEASURE 3.1** | 운영 중 기존·예상하지 못한 새로운 위험을 추적한다 | Incident trend, new injection pattern, **model version별 회귀** |
| **MEASURE 3.3** | 사용자가 문제를 신고하고 결과에 이의를 제기할 수 있게 한다 | Feedback, cancel/undo, incident report |
| **MEASURE 4.2** | 시스템이 의도한 대로 **일관되게 작동하는지** 확인한다 | 주기적 regression test와 field evidence |

**내 자산이 대응하는 것 (명시)**

| Core ID | 내 근거 | 상태 |
|---|---|---|
| MEASURE 2.1 | 정상·악성 메일 corpus + expected decision을 fixture로 고정 | ✅ |
| MEASURE 2.4 | tool invocation·조치·세션이 위협 이벤트로 기록 | ✅ |
| MEASURE 2.8 / 2.9 | **action candidate ↔ 실제 실행의 연결을 계층별로 정량 측정** | ✅ **이게 claude-lab 실험의 정체** |
| MEASURE 4.2 | E2E 경계 테스트 154건 | ✅ 작동 — 13건 실패 검출 |
| **MEASURE 1.3** | 개발자와 분리된 평가자 | ❌ **1인 프로젝트라 없다** |
| **MEASURE 2.6** | **policy unavailable 시 default deny** | ❌ **fail-open이다 — 정면으로 어긋난다** |
| **MEASURE 2.10** | masking/tokenization | ❌ 없다 |

**말할 것**
> "**MEASURE 2.6이 제 결함을 정확히 지목합니다** — '안전하게 실패하고, policy unavailable 시 default deny'를 요구하는데 제 구현은 default allow입니다. 프레임을 자기 것에 적용하면 이렇게 나옵니다."

---

## 6. MANAGE Profile

| Core ID | 관리 결정 | 적용 방법 |
|---|---|---|
| **MANAGE 1.1** | Intended purpose를 충족하고 **배포를 진행할 수 있는지 판단**한다 | Release criteria 기반 **go/no-go** |
| **MANAGE 1.2** | Impact, likelihood 및 자원에 따라 **위험 처리 우선순위**를 정한다 | 비인가 외부 전송과 개인정보 유출을 최우선 처리 |
| **MANAGE 1.3** | 고위험 항목의 대응을 수립한다 | Mitigate, transfer, avoid 또는 **accept 결정** |
| **MANAGE 1.4** | 통제 후 남은 **residual risk를 문서화**한다 | 알려지지 않은 injection, contextual re-identification 등 기록 |
| **MANAGE 2.1** | AI 대안과 필요한 자원을 함께 고려한다 | 고위험 action은 **non-AI workflow 또는 수동 승인** 사용 |
| **MANAGE 2.3** | 알려지지 않았던 위험 발견 시 대응·복구한다 | **Policy update, credential revoke, affected action 취소** |
| **MANAGE 2.4** | 의도된 사용과 다른 행동을 보이는 시스템을 **중단**할 수 있게 한다 | **Kill switch, tool disable, model rollback** |
| **MANAGE 3.1** | 제3자 provider 위험과 통제를 지속 모니터링한다 | **Provider policy·retention·region·model 변경 검토** |
| **MANAGE 3.2** | Pre-trained model을 정기 모니터링 대상에 포함한다 | **Model version change와 security regression** |
| **MANAGE 4.1** | 배포 후 모니터링·appeal·override·incident response·change management를 수행한다 | Monitoring plan, **approval log**, incident runbook |
| **MANAGE 4.2** | 측정 가능한 지속적 개선 활동을 시스템 업데이트에 반영한다 | Test coverage와 attack-blocking 성능 추세 |
| **MANAGE 4.3** | Incident와 error를 관련 actor에 알리고 대응·복구 과정을 문서화한다 | Incident record, notification, recovery evidence |

*원문 정정* 원본 표의 `MANAGE 4. verlie`는 **MANAGE 4.1**을 의미한다 (문서 자신이 각주로 정정).

**말할 것 — MANAGE 2.4와 3.1이 내 공백을 지목한다**
> "**MANAGE 2.4가 kill switch와 model rollback을 요구하고, 3.1이 provider의 정책·리전·모델 변경 모니터링을 요구합니다.** 제 PoC에 둘 다 없습니다.
>
> 특히 **3.1은 외부 SaaS를 쓸 때 가장 중요한 항목**이라고 봅니다 — 벤더가 모델이나 안전필터를 바꾸면 우리가 검증한 전제가 조용히 무효화되는데, 그 변경을 우리가 알 방법이 계약에 없으면 통제가 없는 것과 같습니다."

---

## 7. Residual Risk — 통제를 적용하고도 남는 것

**출처 원문** — 통제를 적용하더라도 다음 위험은 남을 수 있다

- 알려지지 않은 indirect prompt injection 방식
- **정상 업무 instruction과 악성 instruction 간의 의미적 모호성**
- 허용된 tool의 조합을 이용한 **예상하지 못한 action chain**
- **사용자가 악성 action을 승인하는 문제**
- Model 또는 provider 변경에 따른 동작 변화
- 로그의 reasoning과 실제 영향 관계가 충분히 보존되지 않는 문제
- Tokenization 후에도 다른 속성 조합으로 개인을 추론하는 **contextual re-identification**
- **Gateway 또는 PEP를 우회하는 별도 tool invocation path**

**출처 원문** Residual risk는 단순히 기록하는 데 그치지 않고 **Risk Owner → Acceptance/Remediation Decision → Trigger**와 연결해야 한다.

**말할 것 — 이 목록이 왜 중요한가**
> "이 목록에 **'사용자가 악성 action을 승인하는 문제'**가 들어 있습니다. 승인 게이트를 만들어도 사람이 승인해 버리면 통제가 무력화됩니다. **그래서 승인 게이트만으로 끝나지 않고, 승인 자체의 품질을 봐야 한다는 뜻입니다.**
>
> 그리고 마지막 항목 — **'Gateway 또는 PEP를 우회하는 별도 tool invocation path'** — 가 제가 가드레일을 정책과 구별해야 한다고 말하는 이유입니다. 가드레일은 우회 가능한 것이고, 그래서 독립 monitor가 필요합니다."

---

## 8. 요약 — 이 Profile을 인터뷰에서 쓰는 방법

| 물음 | 답이 있는 절 |
|---|---|
| "어떤 프레임으로 위험을 관리하십니까?" | §1 네 Function |
| "AI 특유의 위험이 뭐라고 보십니까?" | §2 trust boundary + MAP 2.2 |
| "역할 분리는 어떻게 하십니까?" | §3 GOVERN 2.1 |
| "검증 기준을 어떻게 정의하십니까?" | §5 MEASURE 전체 |
| "통제가 실패하면?" | §5 MEASURE 2.6 + §6 MANAGE 2.4 |
| "외부 SaaS 위험은?" | §3 GOVERN 6.1~6.2 + §6 MANAGE 3.1~3.2 |
| "남는 위험은 어떻게 하십니까?" | §7 Residual Risk |
| "첫 90일에 뭘 하시겠습니까?" | §5·§6에서 ❌로 표시된 항목 |

### 규율

1. **공식 NIST Profile이 아니다.** use-case Target Profile이라고 반드시 밝힌다.
2. **Core ID를 외우지 않는다.** 표를 띄우고 GOVERN 2.1, MAP 2.2, MEASURE 2.6, MANAGE 2.4 **네 개만** 짚는다.
3. **NIST Core는 구체적 제품이나 통제를 지정하지 않는다** — 조직이 달성해야 할 outcome을 정의한다. 그 차이를 말한다.
4. ❌ 항목을 숨기지 않는다. **그 빈칸이 첫 90일 목록이다.**
