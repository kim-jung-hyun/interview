# AI GRC Control Architecture

## 기준을 실행 가능한 통제로 전환하는 구조

누가 기준을 만들고, 누가 구현하며, 누가 검증하고, 누가 위험을 수용하는가?

---

# 1. 역할 분리의 기준선

| 분리 원칙 | 분리되는 역할 |
|---|---|
| 만든 사람이 판정하지 않는다 | 구현 ↔ Assurance |
| 판정한 사람이 위험을 수용하지 않는다 | Assurance ↔ Risk Acceptance |
| 기준을 만든 사람이 그 기준으로 판정하지 않는다 | AI GRC ↔ Assurance |

## AI GRC의 자리: 기준 제공자

- 개발팀에는 규제·위험 요구사항을 SW 구조에 반영할 수 있는 기준과 가이드를 제공한다.
- Assurance 조직에는 assessment 가능한 evidence와 audit 가능한 구조 요건을 제공한다.

> AI GRC는 직접 구현하거나 최종 판정하는 역할이 아니라, 구현과 판정에 사용할 기준을 운영한다.

---

# 2. 모델의 판단과 실행 권한을 분리한다

```text
Identity / Session Context
          ↓
외부 데이터 수집 · RAG · Tool Result
          ↓  신뢰 등급 선언
Prompt / Context Builder
          ↓
MODEL: Action Candidate 제안
          ↓
HARNESS: Schema · Parameter 검증
          ↓
PDP: ALLOW · DENY · REQUIRE_APPROVAL 결정
          ↓
PEP: Runtime Enforcement
          ↓
Tool 실행: Mail · Calendar · DB
```

전 과정에서 다음 evidence를 연결해 기록한다.

`입력 · Context · Policy Version · Decision · Approval · Execution Result`

E2E Test는 이 전체 경로에 위험 입력을 주입해 통제의 실제 작동을 검증한다.

> 에이전트는 action을 제안할 수 있지만, 실제 실행은 결정론적 authorization과 runtime 집행을 통과해야 한다.

**출처 기반:** NIST AI RMF Profile

---

# 3. Policy와 Guardrail은 다르다

| 구분 | Policy | Guardrail |
|---|---|---|
| 역할 | 무엇을 허용할지 선언 | 결정을 실행 경로에서 강제 |
| 결과 | ALLOW · DENY · REQUIRE_APPROVAL | 통과 · 차단 · 승인 대기 |
| 변경 | Governance 승인과 버전 변경 | 운영 권한 내 배포·튜닝 |
| 책임 | AI GRC | Control Owner · 개발팀 |
| 실패 | 정책이 없거나 모호함 | 정책은 있으나 집행되지 않음 |
| 감사 | 감사 기준 | 감사 대상 |

## 세 가지 판별 질문

1. 변경 시 governance approval이 필요한가?
2. Evidence를 해당 policy version에 연결해야 하는가?
3. Policy intent를 유지한 채 구현을 교체하거나 튜닝할 수 있는가?

> 세 번째 질문이 가장 실용적이다. 동일한 policy intent 안에서 교체·튜닝할 수 있다면 Guardrail에 가깝다.

---

# 4. 정책 변경과 집행 튜닝을 분리한다

| 변경 예시 | 분류 | 이유 |
|---|---|---|
| 특정 경계를 `untrusted`로 선언 | Policy change | Trust assumption과 책임 경계가 바뀜 |
| 탐지 threshold · pattern · detector 조정 | Guardrail tuning | 동일한 policy intent 안에서 집행 방식을 조정 |

예: `tmac.yaml`의 `trust_level` 변경과 그 아래 탐지 정규식 변경은 승인 의미가 다르다.

두 영역을 섞으면 다음 문제가 생긴다.

- 룰 튜닝마다 governance 승인을 거치면서 승인 절차가 형식화된다.
- 정책 버전이 튜닝마다 증가해 evidence에 연결된 policy version의 의미가 약해진다.

---

# 5. PDP와 PEP가 결정과 집행을 분리한다

| 구성 | Full name | 기능 |
|---|---|---|
| **PDP** | Policy Decision Point | 정책을 평가해 ALLOW · DENY · REQUIRE_APPROVAL을 결정 |
| **PEP** | Policy Enforcement Point | PDP의 결정을 실제 요청·행동 경로에서 강제 |

```text
Request / Action
      ↓
PEP가 요청을 가로챔
      ↓
PDP에 정책 결정 요청
      ↓
Decision 반환
      ↓
PEP가 실행 · 차단 · 승인 대기 강제
```

> 이 분리를 통해 Policy를 유지하면서 enforcement 수단만 교체할 수 있다.

---

# 6. Accountability를 역할별로 분리한다

| 영역 | 역할 | Accountability |
|---|---|---|
| 기준 | **AI GRC** | 기준·분류·oversight·gap escalation 체계 운영 |
| 설계 | Security Architecture | 기준을 보안 설계로 변환 |
| 구현 | Development Owner · AI System Owner | 설계·코드·모델 통합 및 control 운영 |
| Assurance | Control Owner | Control 실행 상태와 효과성 모니터링 |
| Assurance | QE / TEVV Owner | 평가 방법과 시험 결과의 신뢰성 확보 |
| Assurance | Release Approver | Evidence 기반 Go / No-go 결정 |
| Assurance | Internal Audit | 설계대로 작동하는지 독립적으로 보증 |
| 수용 | Risk Owner · Business Owner | Residual risk와 use case 위험에 대한 결정 |

> AI GRC는 기준을 제공한다. Release Approver가 배포를 판정하고, Risk Owner가 잔여 위험을 수용한다.

**출처 기반:** Microsoft Responsible AI Standard v2 운영모델, NIST AI RMF Profile GOVERN

---

# 7. 도입 형태에 따라 통제 범위가 달라진다

| Scope | 도입 형태 | 우리가 통제하는 범위 | 주요 통제 |
|---|---|---|---|
| 1 | Consumer App | 고객 데이터와 사용 방식 | Acceptable use · 데이터 분류 · DLP · 교육 |
| 2 | Enterprise App | 사용자·접근·사용 정책 | 계약·보증·데이터 사용 조건 |
| 3 | Pre-trained Model | Application 전체 | AppSec · IAM/Authorization · 입출력 검증 · Logging |
| 4 | Fine-tuned Model | Fine-tuning 데이터 포함 | 학습데이터 보호 · Poisoning 방지 |
| 5 | Self-trained Model | Model lifecycle 전체 | 전 수명주기 통제 |

> 직접 통제할 수 없는 영역은 공급자 계약과 assurance evidence로 요구한다.

**출처 기반:** AWS SRA Generative AI Security Scoping Matrix  
**해석:** Enterprise 도입 심사용 통제 범위

---

# 8. 자율성이 높을수록 독립 통제가 필요하다

| Agency Scope | 사람의 위치 | 주요 통제 |
|---|---|---|
| No Agency | 읽기 전용·고정 workflow | Workflow 무결성 · 입출력 검증 · Audit |
| Prescribed Agency | 영향 있는 action은 사람 승인 | 승인 우회 방지 · Approver 신원 검증 · 승인 기록 |
| Supervised Agency | 사람이 시작하고 이후 자율 실행 | Runtime monitoring · 권한 경계 · Scope creep 방지 · Kill switch |
| Full Agency | 스스로 시작하고 지속 운영 | 지속 검증 · 자동 격리 · Human override · Fail-safe |

## Supervised Agency 이상에서 필요한 구조

```text
Primary Agent
     ↓ Action / Telemetry
Independent Monitor
     ↓
Containment Controller
     ↓ Throttle · 권한 회수 · Session 격리 · STOP
Human Override
```

- Monitor와 override는 primary agent의 runtime 밖에 둔다.
- 통제 실패 시 위험한 action을 계속하지 않고 거부·중지·승인 요구로 전환한다.

**출처 기반:** AWS SRA Agentic AI Security Scoping Matrix  
독립 모니터링과 격리를 통해 통제 실패 시 안전하게 중지하는 **Fail-safe 구조**다.

---

# 9. 정책은 운영 결과를 반영하되 자동 변경하지 않는다

```text
정책 정의 · Version 관리
        ↓
Gateway 집행 · Boundary Test
        ↓
Event · Test Result 수집
        ↓
빈도 · 심각도 · 오탐률 평가
        ↓
Policy 변경 제안
        ↓
AI GRC 승인 · 중대 변경 Escalation
        ↓
새 Policy Version 배포
```

## 두 종류의 승인

| 승인 대상 | 책임 역할 |
|---|---|
| 기준·정책 변경 | AI GRC. 중대 변경은 심의체계로 escalation |
| 시스템 배포 Go / No-go | Release Approver. Evidence를 근거로 판정 |

---

# 10. 규제 요구사항을 심사 게이트로 번역한다

| 규제 축 | 도입 심사 게이트 |
|---|---|
| PIPA 국외이전 | 추론·저장 리전과 적법 근거 확인 |
| PIPA 역외적용 | 해외 공급자의 적용 대상 인지와 이행 확인 |
| PIPA 자동화된 결정 | 사람 확인, 거부·설명 요구 대응 구조 확인 |
| EU AI Act 위험 분류 | Intended use 선언 후 위험 등급과 의무 결정 |
| EU AI Act 시행 일정 | 발효 시점을 versioned policy definition으로 관리 |
| AI기본법 | 고영향·생성형·대규모 분류와 고지·표시 요건 확인 |

## 통제 어휘에 `REQUIRE_APPROVAL`이 필요한 이유

사람에 관한 완전자동 결정은 정보주체의 권리에 영향을 줄 수 있다. 따라서 정책 결과를 ALLOW와 DENY만으로 설계하지 않고, 사람 확인을 거치는 상태를 포함해야 한다.

> 규제 일정은 변경될 수 있으므로 application code에 날짜를 하드코딩하지 않고, 버전 관리되는 policy definition에 둔다.

**출처 기반:** 개인정보보호법, EU AI Act, AI기본법 주요 개념  
**해석·제안:** 규제 개념을 policy gate로 변환

---

# 11. NIST AI RMF와의 정합성

| NIST AI RMF Function | Control Architecture의 역할 |
|---|---|
| **GOVERN** | 경계·신뢰등급·책임·승인 게이트 정의 |
| **MAP** | 데이터가 명령과 action으로 바뀌는 경계 식별 |
| **MEASURE** | Control 집행과 효과성을 독립적으로 검증 |
| **MANAGE** | 집행·기록·위험 처리·정책 재갱신 |

```text
규제·표준
   ↓
Policy / Control Requirement
   ↓
Architecture Enforcement
   ↓
Test / Evidence
   ↓
Monitoring / Policy Update
```

> **최종 메시지**  
> AI GRC의 산출물은 규제 문서의 요약이 아니라, 개발팀이 구현하고 Assurance가 검증할 수 있는 기준 구조다.

**출처 기반:** NIST AI RMF  
**해석:** Enterprise AI control lifecycle과의 매핑

---

# 부록. 약어: AI·기술

| 약어 | 원어 | 우리말 |
|---|---|---|
| **LLM** | **L**arge **L**anguage **M**odel | 대형 언어 모델 |
| **RAG** | **R**etrieval-**A**ugmented **G**eneration | 검색 증강 생성 |
| **SaaS** | **S**oftware **a**s **a** **S**ervice | 서비스형 소프트웨어 |
| **IAM** | **I**dentity and **A**ccess **M**anagement | 신원·접근 관리 |
| **PoC** | **P**roof **o**f **C**oncept | 개념 검증 |
|
