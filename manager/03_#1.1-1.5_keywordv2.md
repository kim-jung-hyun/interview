# AI GRC Role

## Policy에서 Assurance까지 실행 가능한 기준을 만든다

`Policy Definition → Engineering Control → Evidence → Assessment → Policy Update`

---

# 1.1 Framework Architecture & Policy-as-Code

## 위협 모델을 실행 가능한 기준으로 전환

| 문제 | 설계 방향 |
|---|---|
| 위협 모델은 문서에 남고 정책·탐지·테스트는 각각 관리됨 | 경계를 기준 단위로 정의하는 **Threat Modeling as Code** |
| 통제 자산마다 변경 주기가 달라 drift 발생 | 하나의 정의에서 정책·탐지·테스트를 함께 생성 |

```text
Boundary × Trust Level = Baseline Specification
Threat × Response      = Rule Set
```

**산출물:** 특허 · 실행 데모

> 사람의 권리에 영향을 주는 자동화된 결정에 대응할 수 있도록 `REQUIRE_APPROVAL`을 정책 어휘에 포함한다.

## 모델의 판단과 실행 권한을 분리

```text
사용자 요청
    ↓
Model       Action 후보 제안
    ↓
Harness     형식·Schema 검증
    ↓
Policy      ALLOW · DENY · REQUIRE_APPROVAL 결정
    ↓
Guardrail   Runtime 집행
    ↓
Tool 실행
    ↓
Evidence    입력부터 실행 결과까지 연결 기록
    ↓
Assessment  통제의 설계·운영 효과성 독립 검증
```

| 계층 | 책임 | 핵심 질문 |
|---|---|---|
| **Model** | Action 후보 제안 | 무엇을 하려 하는가? |
| **Harness** | 출력 구조화와 Schema 검증 | 실행 가능한 요청인가? |
| **Policy** | Identity·Tool·Resource·Context를 기준으로 실행 여부 결정 | 허용되는가? |
| **Guardrail** | 정책 결정을 Runtime에서 집행 | 결정이 실제로 강제되는가? |
| **Evidence** | 입력·정책 버전·결정·승인·실행 결과를 연결해 기록 | 사후에 증명할 수 있는가? |
| **Assessment** | 통제가 설계대로 작동하는지 독립 검증 | 통제를 신뢰할 수 있는가? |

> 핵심은 모델의 판단과 실행 권한을 분리하는 것이다. 에이전트는 action을 제안할 수 있지만, 실제 실행은 별도의 authorization과 runtime enforcement를 통과해야 한다.

## Policy와 Guardrail의 구분

| 구분 | **Policy** | **Guardrail** |
|---|---|---|
| 역할 | 허용되는 행위를 선언 | 정책 결정을 실행 경로에서 강제 |
| 결과 | ALLOW · DENY · REQUIRE_APPROVAL | 통과 · 차단 · 승인 대기 |
| 변경 | Governance 승인과 버전 변경 | 운영 권한 내 배포·튜닝 |
| 책임 | AI GRC | Control Owner · Development |
| 실패 | 정책이 없거나 모호함 | 정책은 있으나 집행되지 않음 |
| 감사 | 감사 기준 | 감사 대상 |

### 판별 기준

1. 변경 시 governance approval이 필요한가?
2. Evidence가 해당 policy version에 연결되어야 하는가?
3. Policy intent를 유지한 채 구현을 교체하거나 튜닝할 수 있는가?

> 같은 policy intent 안에서 구현을 교체하거나 튜닝할 수 있다면 Guardrail에 가깝다.

| 변경 예시 | 분류 | 이유 |
|---|---|---|
| 특정 경계를 `untrusted`로 선언 | Policy change | Trust assumption과 책임 경계가 바뀜 |
| 탐지 threshold·pattern·detector 조정 | Guardrail tuning | 같은 policy intent 안에서 집행 방식을 조정 |

두 영역을 섞으면 룰 튜닝마다 governance 승인이 필요해지고, policy version의 감사 의미도 약해진다.

## PDP와 PEP: 결정과 집행의 분리

| 구성 | Full name | 기능 |
|---|---|---|
| **PDP** | Policy Decision Point | 정책을 평가해 ALLOW · DENY · REQUIRE_APPROVAL 결정 |
| **PEP** | Policy Enforcement Point | PDP의 결정을 실제 요청·행동 경로에서 강제 |

`Request → PEP → PDP → Decision → PEP Enforcement`

> PDP와 PEP를 분리하면 policy를 유지하면서 enforcement 수단을 교체할 수 있다.

## 기준 변경과 배포 승인의 분리

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

| 승인 대상 | 책임 역할 |
|---|---|
| 기준·정책 변경 | AI GRC. 중대 변경은 별도 심의체계로 escalation |
| 시스템 배포 Go / No-go | Release Approver. Evidence를 근거로 판정 |

> 정책 변경 승인 단계가 policy ownership의 실제 위치다.

**출처 기반:** NIST AI RMF Profile

---

# 1.2 Assurance Partnering

## AI GRC 기준을 검증 가능한 형태로 정의

Assurance는 AI GRC뿐 아니라 신뢰성·성능 등 여러 기준을 함께 평가한다. AI GRC의 역할은 자신의 기준을 검증 가능한 형태로 정의하고, 검증팀이 이를 확인할 수 있도록 지원하는 것이다.

| 역할 | 책임 |
|---|---|
| **AI GRC** | 위험 분류·통제 기준·예외 처리 기준 정의 |
| **Development Review** | 설계와 구현이 요구사항에 부합하는지 검토 |
| **QE / TEVV** | 품질·안전·control effectiveness 독립 시험 |
| **Release Approver** | Evidence에 근거한 Go / No-go 판정 |
| **Internal Audit** | 프로세스와 통제 준수 여부 사후 독립 검증 |
| **Risk Owner** | Residual risk 수용·완화·회피·이전 결정 |

전용 evidence가 필요한 핵심 영역은 다음과 같다.

- 선언된 trust level 복원
- 모델 입력과 전송 byte 대조

```text
Requirement → Verification → Evidence → Assessment
```

> AI GRC는 승인하지 않는다. 승인할 수 있는 기준과 evidence 구조를 만든다.

**산출물:** 작성 중인 논문

**출처 기반:** Microsoft Responsible AI Standard v2 · NIST AI RMF Profile GOVERN

---

# 1.3 AI Risk Evaluation & Safeguards

## 데이터가 명령으로 바뀌고 권한으로 실행되는 지점을 식별

**Use case:** “메일을 찾아 요약하고 캘린더에 등록해줘.”

| 흐름 | 확인할 위험 |
|---|---|
| **Data Flow** | 어떤 데이터가 어디로 이동하는가? |
| **Control Flow** | 외부 데이터가 에이전트의 명령으로 바뀌는가? |
| **Privilege Flow** | 생성된 명령이 누구의 권한으로 실행되는가? |

경계는 컴포넌트가 배치된 위치가 아니라 **흐름의 종류가 바뀌는 지점**이다.

```text
메일 조회 허용
        +
전사 발송 허용
        ↓
조회한 메일 내용을 전사에 발송
        ↓
개별 권한 심사에 없던 새로운 경계를 통과
```

개별 action이 정상 권한 안에 있어도 연쇄되면 새로운 위험이 만들어질 수 있다. 따라서 단일 action의 탐지 성능만이 아니라 action 조합과 trust boundary를 함께 설계해야 한다.

## 도입 형태에 따른 통제 범위

| Scope | 도입 형태 | 우리가 통제하는 범위 | 주요 통제 |
|---|---|---|---|
| 1 | Consumer App | 고객 데이터와 사용 방식 | Acceptable use · 데이터 분류 · DLP · 교육 |
| 2 | Enterprise App | 사용자·접근·사용 정책 | 계약·보증·데이터 사용 조건 |
| 3 | Pre-trained Model | Application 전체 | AppSec · IAM/Authorization · 입출력 검증 · Logging |
| 4 | Fine-tuned Model | Fine-tuning 데이터 포함 | 학습데이터 보호 · Poisoning 방지 |
| 5 | Self-trained Model | Model lifecycle 전체 | 전 수명주기 통제 |

> 직접 통제할 수 없는 영역은 공급자 계약과 assurance evidence를 통해 요구한다.

## 자율성에 따른 통제 수준

| Agency Scope | 사람의 위치 | 주요 통제 |
|---|---|---|
| No Agency | 읽기 전용·고정 workflow | Workflow 무결성 · 입출력 검증 · Audit |
| Prescribed Agency | 영향 있는 action은 사람 승인 | 승인 우회 방지 · Approver 신원 검증 · 승인 기록 |
| Supervised Agency | 사람이 시작하고 이후 자율 실행 | Runtime monitoring · 권한 경계 · Scope creep 방지 · Kill switch |
| Full Agency | 스스로 시작하고 지속 운영 | 지속 검증 · 자동 격리 · Human override · Fail-safe |

> Fail-safe는 통제 실패 시 위험한 action을 계속하지 않고 거부·중지·승인 요구로 전환하는 구조다.

**출처 기반:** AWS SRA Generative AI Security Scoping Matrix · AWS SRA Agentic AI Security Scoping Matrix

---

# 1.4 Cross-Functional Engineering Alignment

## 같은 기준을 조직별 실행 언어로 변환

| 이해관계자 | 기준을 읽는 방식 |
|---|---|
| Development | 코드에 무엇을 구현해야 하는가? |
| QE / TEVV | 무엇을 통과 조건으로 검증할 것인가? |
| Planning / Marketing | 제품 일정과 출시 조건에 무엇이 영향을 주는가? |
| AI GRC | 어떤 evidence로 gate를 운영할 것인가? |

과거에는 사업자·PM·Quality 요구를 SW·HW·검증팀과 조율하며 북미·캐나다향 Production Release를 리딩했다. 현재는 보안 개발팀, 사업부 SW·HW, 상품기획, 마케팅과 선행 보안 기술의 적용 방향을 조율하고 있다.

> 한 정의를 개발팀은 rule로, 검증팀은 test case로, AI GRC는 gate로 읽을 수 있어야 한다.

## Rogers 사업자 인증: 판단 근거를 먼저 확보

캐나다향 단말의 Rogers 사업자 인증이 lock-in 2주 전에 확정됐다. Protocol 개발팀은 요구 band와 대응 범위가 확정되지 않아 일정을 수용하기 어렵다고 판단했다.

| 순서 | 실행 |
|---|---|
| 1 | Lock-in 전에 사업자 문서를 사전 검토 |
| 2 | 현지 검증·사업자 전달·TAM 대응용 개발 시료 선발송 |
| 3 | 현지 인력이 call test를 수행하고 로그를 Protocol 개발팀에 전달 |
| 4 | 개발팀이 로그로 요구 band 지원 여부를 확인 |
| 5 | 사업자 specification에 맞게 band configuration을 변경하고 SW 전달 |

로그가 “2주 안에 무엇을 해야 하는가”를 확정하자 개발팀은 일정을 수용했다.

> 게이트 운영은 마지막에 심사 항목을 통보하는 것이 아니라, 통과 조건과 인정할 evidence를 설계 단계로 앞당기는 일이다.

---

# 1.5 Enterprise AI Policy Owner

## Policy ownership은 운영 구조에서 성립한다

```text
정책 기준
    ↓ 배포 Gate
Control Implementation
    ↓ 실행 결과
Verification & Evidence
    ↓ 평가 결과
Policy Update
```

| 책임 | 운영 방식 |
|---|---|
| Scope 판정 | Use case와 risk tier에 따라 적용할 기준 결정 |
| Policy 변경 승인 | Evidence에 근거해 기준 변경 여부 판단 |
| Gap management | 미충족 항목과 예외를 추적하고 escalation |
| Version governance | 실행 evidence를 당시 policy version과 연결 |

> Framework Architecture에서 만든 기준이 배포 gate가 되고, Assurance 결과가 다시 기준을 갱신할 때 policy ownership이 실제 운영 구조로 작동한다.

---

# 부록. 약어

| 약어 | 원어 | 우리말 |
|---|---|---|
| **AI GRC** | AI Governance, Risk and Compliance | AI 거버넌스·위험·컴플라이언스 |
| **QE / TEVV** | Quality Engineering / Test, Evaluation, Verification and Validation | 품질 엔지니어링 / 시험·평가·검증·확인 |
| **PDP / PEP** | Policy Decision Point / Policy Enforcement Point | 정책 결정 지점 / 정책 집행 지점 |
| **AI RMF** | AI Risk Management Framework | AI 위험관리 프레임워크 |
| **SRA** | Security Reference Architecture | 보안 참조 아키텍처 |
| **PIPA** | Personal Information Protection Act | 개인정보보호법 |
| **E2E** | End-to-End | 종단 간 |
| **PoC** | Proof of Concept | 개념 검증 |
