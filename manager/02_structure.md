# 기본 구조와 개념 — 거버넌스 매니저 인터뷰용

> **이 문서가 이번 인터뷰의 화면 표시 본체다.** 코드도 실험 수치도 없다. 그건 기술 인터뷰(`../tech/`)로 보낸다.
> 여기 있는 것은 **어휘·계층·소유권·게이트** 네 가지다. 매니저가 판단하려는 것이 그것이기 때문이다.
>
> 계층 어휘는 내가 만든 것이 아니라 세 참조 문서에서 가져왔다 — NIST AI RMF Profile, AWS SRA Scoping Matrix 2종, Microsoft Responsible AI Standard v2.
>
> **화면 표시 순서 (1시간 압축판, 내가 말하는 순서 그대로).** **§0(기준선 + 내 산출물 표)만 오프닝 3~4분에 항상 띄운다.** 이후 §1·§2(1.1 자료) → §3(1.2 자료) → §4·§5·§6·§7(1.5 자료) → §8(Q6 첫 90일) 순서로, **전부 질문이 그쪽으로 왔을 때만 편다** — 화면에서 뺀 게 아니라 말하는 순서대로 뒤로 보낸 것이다. 말하기 대본은 `00_note.md` §0-1(오프닝)·§0-2(물으면) 참조. **약어는 맨 뒤 부록으로 옮겼다** — 말하면서 필요할 때 검색해서 쓴다.

---

## 0. 기준선 — 이 인터뷰 전체의 기준

**모든 역할 질문은 이 사슬로 답한다.** 아래 §1~§7은 이 사슬의 각 칸을 설명하는 것이다.

    기준 (AI GRC · 내 자리)  →  구현 (Development)  →  판정 (Assurance)  →  수용 (Risk / Business)
    「기준 제공자」
    Staff AI Security Governance Engineer

| 분리선 | 내용 | 사이 |
|---|---|---|
| **①** | 만든 사람이 판정하지 않는다 | 구현 ↔ Assurance |
| **②** | 판정한 사람이 위험을 수용하지 않는다 | Assurance ↔ 수용 |
| **③** | **기준을 만든 사람이 그 기준으로 판정하지 않는다** | **내 자리 ↔ Assurance** |

**Assurance = 실행 · 모니터링 · 시험 · 승인 · 감사.** Control Owner · QE/TEVV · **Release Approver** · Internal Audit이 여기 있다.

### 내 자리 = 「기준 제공자」

지원 직함이 `Staff AI Security Governance **Engineer** (AI GRC)`다. **관리자가 아닌 개별 기여자(IC)**이고 `Governance`는 기준을 세우는 일이다. **직함 자체가 승인자가 아니라 기준 제공자임을 말한다.**

### 내 산출물

| # | 산출물 | 받는 쪽 | 내용 |
|---|---|---|---|
| **①** | **개발팀용 기준과 가이드** | Development · AI System Owner | **규제 등의 requirement를 SW 구조에 넣을 수 있는 형태로** 변환한 기준 |
| **②** | **Assurance용 구조 요건** | Control Owner · QE/TEVV · Release Approver · Internal Audit | **assessment 가능한 evidence**와 **audit 가능한 구조**가 나오게 하는 요건 |

**말할 한 문장 — 이번 인터뷰에서 가장 먼저 말한다**
> **"제 자리는 「기준 제공자」입니다. 저는 승인하지 않습니다 — 승인이 가능하도록 만듭니다. 제 산출물은 결정이 아니라 결정의 전제입니다."**

**「기준 제공자」라는 말을 쓰는 이유** 지원 직함이 `Staff AI Security Governance **Engineer**`다. 관리자가 아니라 **개별 기여자(IC)** 포지션이고, `Governance`는 기준을 세우는 일이다. **직함 자체가 승인자가 아니라 기준 제공자임을 말한다.**

**근거는 운영모델 표의 구조다** — `05_ai_lifecycle.md` §2의 11단계 표에서 **AI GRC는 「최종 책임」 열에 한 번도 나오지 않는다.** 수행 책임과 검토 열에만 나온다. 내 해석이 아니다.

### 자기 진단 — 내 PoC는 이 기준선의 어디가 없는가

| 분리선 | 내 PoC |
|---|---|
| ① 만든 사람 ↔ 판정 | **혼재.** 내가 만들고 내가 E2E 테스트를 썼다. 다만 **테스트가 실제로 내 구현의 실패를 잡아냈다** |
| ② 판정 ↔ 수용 | **없음.** residual risk를 수용할 주체가 정의되지 않았다 |
| **③ 기준 ↔ 판정** | **없음. 내가 기준을 쓰고 내가 그 기준으로 판정했다** |

> "1인 프로젝트라 세 분리선이 다 없습니다. **특히 ③이 없습니다.** 다만 ①의 대용으로 테스트를 썼고 그게 실제로 제 구현의 실패를 잡아냈습니다. **혼자 하면서도 '내가 만든 걸 내가 판정하지 않는다'를 흉내낼 수 있는 방법이 테스트라고 생각합니다.**"

그림: `figures/baseline.svg` — **이 한 장을 가장 먼저 띄운다.**

---

## 1. 통제 원칙 — 다섯 계층

> **1.1 자료 · 오프닝에서는 안 띄운다.** Q3류("policy냐 guardrail이냐") 질문이 오면 편다 — `00_note.md` §0-2.

> **기준선 위치** 이 계층은 **구현**의 형태다. 내가 산출물 ①로 개발팀에 넘기는 구조가 이것이다.

**출처** NIST AI RMF Profile, Target Control Architecture

> **Model proposes. Harness authorizes. Policy decides. Guardrail enforces. Evidence proves.**

| 계층 | 책임 | 질문 |
|---|---|---|
| **Model** | action **후보를 제안**한다 | 무엇을 하려 하는가 |
| **Harness** | 출력을 구조화하고 실행 가능한 요청인지 확인한다 | 형식적으로 유효한가 |
| **Policy** | identity·tool·resource·parameter·context로 **실행 여부를 결정**한다 | 허용되는가 |
| **Guardrail** | 정책 결정을 **runtime에 집행**한다 | 결정이 실제로 강제되는가 |
| **Evidence** | 입력·context·정책 버전·결정·승인·실행 결과를 **연결해 기록**한다 | 나중에 증명할 수 있는가 |
| **Assessment** | 위 다섯이 설계대로 작동하는지 **독립 검증**한다 | 믿을 수 있는가 |

**말할 한 문장**
> **"핵심은 모델의 판단과 실행 권한을 분리하는 것입니다. 에이전트가 action을 제안할 수는 있지만, 실제 실행은 별도의 결정론적 authorization과 runtime 집행, 증거 체계를 통과해야 합니다."**

---

## 2. Policy와 Guardrail은 다르다

> **1.1 자료 · 오프닝에서는 안 띄운다.** 오프닝에서는 한 문장("산출물①은 Policy 계층")으로 접는다. 이 절 전체는 Q3·1.1 자기진단 질문이 오면 편다 — `00_note.md` §0-2.

> **기준선 위치** **Policy = 기준(내 자리) / Guardrail = 판정·집행 도구(Control Owner = Assurance).** 이 절은 **분리선 ③의 기술적 형태**다 — 기준과 집행이 한 파일에 섞이면 ③이 무너진다.

**이 절이 이번 인터뷰의 핵심이다.** 둘 다 "차단"을 하지만 성질이 다르고, 구별하지 않으면 거버넌스가 성립하지 않는다.

| | **Policy** | **Guardrail** |
|---|---|---|
| 성격 | 선언적 — 무엇이 허용되는가 | 실행적 — 결정을 강제하는 기계 |
| 산출물 | 결정 (허용 / 거부 / **승인 요구**) | 집행 결과 (차단됨 / 통과됨 / 대기) |
| 변경 절차 | **승인을 경유한다. 버전이 올라간다** | 배포로 바뀐다. 튜닝 대상이다 |
| 변경 주체 | **AI GRC** (기준) | **Control Owner** · 개발팀 (튜닝) |
| 실패 양상 | 정책이 **없거나 모호함** | 정책은 있는데 **집행되지 않음** |
| 감사에서의 위치 | 감사 **기준** | 감사 **대상** |

### 구별하는 질문 세 개

무엇이 정책이고 무엇이 가드레일인지 판단할 때 쓴다.

1. **변경 시 governance approval이 필요한가?** → 필요하면 **Policy**
2. **evidence가 해당 policy version에 binding되어야 하는가?** → 그래야 하면 **Policy**
3. **Policy intent를 바꾸지 않고 구현을 교체·튜닝할 수 있는가?** → 가능하면 **Guardrail**

### 네 축으로 보면 차이가 선명해진다

| 판단 기준 | **Policy** | **Guardrail** |
|---|---|---|
| **변경 의미** | **허용/금지/책임 경계가 바뀜** | enforcement 방법·threshold·rule이 바뀜 |
| **승인** | 원칙적으로 **governance 승인 대상** | 정해진 **운영 권한 내 tuning** 가능 |
| **Evidence version** | **Policy version과 연결 필요** | rule/config version을 별도 기록 가능 |
| **구현 변경** | **Policy 자체는 유지** | 동일 Policy를 만족하면 **교체·튜닝 가능** |

**③이 가장 실용적인 판별식이다.** 두 문장으로 정리한다.

- **"어떤 경계를 신뢰할 수 없다고 선언한다"** → **trust assumption 또는 normative requirement가 바뀌는 것**이므로 **Policy change에 가깝다**
- **"탐지 룰의 threshold·pattern·detector를 조정한다"** → **동일한 policy intent 안에서 enforcement를 조정하는 것**이므로 **Guardrail tuning에 가깝다**

**자산으로 내려가면** `tmac.yaml`의 `trust_level: untrusted / semi_trusted / trusted`가 문자 그대로 **trust assumption의 선언**이다. 그 값을 바꾸는 것과 그 아래 정규식·임계값을 바꾸는 것은 성질이 다르다.

**"가깝다"라고 쓴 이유 — 그리고 애매할 때의 기본값 규칙**
이 구분은 이진이 아니고 중간에 걸리는 항목이 있다. 그래서 판별식에 **기본값 규칙**을 함께 둔다.

> **애매하면 policy로 분류하고, 그중 어디까지를 운영 권한 내 tuning으로 위임할지 명시한다.**

보수적으로 잡아 두고 위임 범위를 열어 주는 방향이 그 반대보다 안전하다. **그리고 이 분류 규칙 자체가 policy다** — 분류가 바뀌면 승인 절차가 바뀌기 때문이다.

**말할 것**
> "탐지 룰 하나를 고치는 것과 어떤 경계를 신뢰할 수 없다고 선언하는 것은 둘 다 차단에 영향을 주지만 **승인 절차가 달라야 합니다.**
>
> 섞이면 두 문제가 생깁니다 — **룰 튜닝마다 governance 승인을 받아야 하니 승인 절차가 형식화되고**, 반대로 **정책 버전이 튜닝마다 올라가서 evidence에 붙은 policy version이 의미를 잃습니다.**"

**원칙으로 말한다 — 내 PoC 얘기는 기술 인터뷰로**
> "**하나의 정의에서 파생시키는 것과 하나의 파일에 섞어 두는 것은 다른 설계입니다.** 섞이면 승인 절차가 하나로 묶여서, 룰 튜닝마다 승인을 받거나 정책 버전이 튜닝마다 올라갑니다. **그래서 도입 첫 단계에서 이 구별 기준을 세워야 한다고 봅니다.**"

*(내 PoC가 섞여 있다는 실측은 `../tech/` 자료다. 물으면 답하고, 먼저 꺼내지 않는다.)*

### PDP와 PEP — 결정과 집행이 구조적으로 분리된다

Policy와 Guardrail의 구별은 **시스템에서 두 지점으로 나타난다.**

| 약어 | 원어 | 하는 일 |
|---|---|---|
| **PDP** | **P**olicy **D**ecision **P**oint | 정책을 평가해서 **`ALLOW` / `DENY` / `REQUIRE_APPROVAL` 같은 결정을 내리는 지점** |
| **PEP** | **P**olicy **E**nforcement **P**oint | PDP의 결정을 **실제 요청·행동 경로에서 강제(enforce)하는 지점** |

**구조적으로는 보통 이 순서다**

    Request / Action  →  PEP  →  PDP  →  Decision  →  PEP Enforcement

**PEP가 먼저 온다.** 실행 경로에 앉아 있으면서 요청을 가로채고, PDP에 물어보고, 돌아온 결정을 강제한다.

**말할 것**
> "정책과 가드레일의 구별이 시스템에서는 **PDP와 PEP 두 지점으로 나타납니다.**
> **PDP는 정책을 평가해서 허용·거부·승인 요구를 결정하고, PEP는 그 결정을 실제 실행 경로에서 강제합니다.**
> 순서는 **요청이 먼저 PEP를 지나고, PEP가 PDP에 물어보고, 돌아온 결정을 PEP가 강제하는** 형태입니다.
>
> **이 분리가 있어야 정책을 바꾸지 않고 집행 수단만 교체할 수 있습니다** — 아까 세 번째 판별식이 그것입니다."

→ **구별 기준(§2 앞부분)이 왜 실무적으로 의미가 있는지**를 이 구조가 보여준다. 분리되어 있지 않으면 정책을 고칠 때마다 집행 코드를 고쳐야 한다.

---

## 3. 누가 무엇을 소유하는가 — 기준선의 역할 상세

> **1.2 자료 · 오프닝에서는 안 띄운다.** 오프닝은 §0의 산출물 표 하나로 대신한다. 이 절은 역할 범위 질문(Q4-1·Q5)이 오면 편다 — `00_note.md` §0-2.

**출처** Microsoft Responsible AI Standard v2 운영모델 / NIST AI RMF Profile GOVERN — "Policy Owner, Implementation Owner, Assurance Owner 및 Risk Owner의 책임을 구분한다"

| 진영 | 역할 | Accountability |
|---|---|---|
| **기준** | **AI GRC** ← **내 자리** | **기준·분류·oversight·gap escalation 체계의 운영** |
| **설계** | **Security Architecture** (별도 팀) | **내 요건을 보안 설계로 옮긴다** — 「무엇을」이 아니라 「어떻게」 |
| 구현 | Development Owner | 설계·코드·모델 통합 및 기술적 remediation |
| 구현 | AI System Owner | 승인된 요구사항과 control을 충족하도록 운영 |
| **Assurance** | **Control Owner** | 특정 control의 설계, 구현 상태 및 효과성 → **실행·모니터링** |
| **Assurance** | **QE / TEVV Owner** | 평가 방법의 적절성과 시험 결과의 신뢰성 → **시험** |
| **Assurance** | **Release Approver** | evidence를 근거로 한 **Go/No-go 결정** → **승인** |
| **Assurance** | **Internal Audit** | 설계된 대로 작동하는지 **독립적으로 보증** → **감사** |
| 수용 | **Risk Owner** | Residual risk의 수용·완화·회피·이전 결정 |
| 수용 | Business Owner | AI use case의 필요성·편익·intended use 및 사업상 위험 |

### 이 표가 JD를 갈라준다

| JD 항목 | 계층 | 내 역할 위치 |
|---|---|---|
| **1.1** Framework & Policy-as-Code | **Policy** 설계 + 개발팀 가이드 | **AI GRC** |
| **1.2** Assurance Partnering | **Assessment 기준 + evidence·audit 구조 요건** | 정의는 내가, **실행·시험·승인·감사는 Assurance** |
| **1.3** AI Risk Evaluation | 위협 식별 + 통제 선택 | AI GRC |
| **1.4** Cross-Functional Alignment | 계층 간 역할 정렬 | 조정 |
| **1.5** Enterprise AI Policy Owner | Policy·분류 기준 + Scope 판정 + escalation | **AI GRC** (승인은 Assurance) |

**말할 것**
> **"저는 승인하지 않습니다. 승인이 가능하도록 만듭니다."**
>
> "제 자리는 **AI GRC 하나**입니다. 두 가지를 만듭니다 — **규제 등의 requirement를 개발팀이 SW 구조에 넣을 수 있는 기준과 가이드**, 그리고 **그 구조에서 Assurance가 assessment할 evidence와 audit 가능한 형태가 나오게 하는 요건**입니다.
>
> **실행·모니터링·감사·승인은 전부 Assurance입니다. Release Approver도 Assurance 쪽이고 제 자리가 아닙니다.** JD 1.2가 'Assurance팀이 execute·monitor·audit한다'고 쓴 것과 같습니다.
>
> 이건 제 해석이 아니라 **운영모델 표의 구조입니다** — AI GRC는 lifecycle 11단계 어디에서도 최종 책임 열에 나오지 않고 수행 책임과 검토 열에만 나옵니다.
>
> **제 산출물은 결정이 아니라 결정의 전제입니다.** 제가 기준을 만들고 제가 그 기준으로 판정하면 기준 자체를 검증할 사람이 없어집니다."

**내 산출물 두 가지**

| # | 산출물 | 받는 쪽 |
|---|---|---|
| ① | **기준과 가이드** — 규제 requirement가 SW 구조에 들어갈 수 있는 형태 | **1차: Security Architecture** → 2차: Development · AI System Owner |
| ② | **Assurance용 구조 요건** — assessment 가능한 evidence, audit 가능한 구조 | Control Owner · QE/TEVV · Release Approver · Internal Audit |

**【미작성】 조직 실제 역할로의 매핑 — 조직 확인 후**

> MS Standard의 역할은 **직책 이름이 아니라 책임의 종류**다. 조직에 그 이름의 자리가 없어도 책임은 어딘가에 있어야 한다.
> **Responsible AI Approver · Review Board · Release Approver · Internal Audit이 실제 어느 조직인지 확인한 뒤 배정**한다. 지금 채우면 추측이 된다.

> **물으면** — "**MS 표준의 역할은 직책이 아니라 책임의 종류입니다.** 조직 역할 구조를 확인한 뒤 맞추는 것이 도입 초기 작업이라고 봅니다."

상세와 근거는 `06_ai_responsibility.md` §3·§4.

---

## 4. 통제 범위 — 누가 무엇을 control하는가

> **1.5 자료 · 오프닝에서는 안 띄운다.** Scope 질문·Q2(외부 SaaS)가 오면 편다.

> **기준선 위치** Scope 좌표는 **기준**이 정한다. 그 좌표에 따라 통제를 직접 구현할지(구현) 계약·증빙으로 요구할지가 갈리고, **충족 판정은 Assurance**다.

**출처** AWS SRA Generative AI Security Scoping Matrix

도입 심사에서 **가장 먼저 찍는 좌표**다. 이 좌표가 우리가 통제할 수 있는 것과 계약으로 요구해야 하는 것을 가른다.

| Scope | 분류 | 우리가 통제하는 것 | 주 통제 초점 |
|---|---|---|---|
| **1** | Consumer app | 고객 데이터와 사용 방식만 | **acceptable-use 정책, 데이터 분류, DLP, 사용자 교육** |
| **2** | Enterprise app | + user/access, 사용 정책 | + **계약·보증·opt-out·데이터 사용 조건** |
| 3 | Pre-trained model | + application 전체 | + application security, IAM/authorization, 입출력 검증, 로깅 |
| 4 | Fine-tuned model | + fine-tuning 데이터 | + 학습데이터 보호, poisoning 방지 |
| 5 | Self-trained | 전부 | + 모델 lifecycle 전체 |

**핵심 문장**
> **"JD가 말하는 3rd-party AI SaaS는 보통 Scope 1~2이고, 제가 만들어 본 것은 Scope 3입니다.** 이 차이가 제 공백의 정확한 이름입니다. Scope 3에서는 입출력 검증과 authorization을 직접 구현할 수 있었지만, Scope 1~2에서는 **같은 통제를 계약과 증빙 요구로 대체**해야 합니다. 묻는 항목은 같고 확보 수단이 다릅니다."

---

## 5. 자율성 범위 — 에이전트에 어디까지 권한을 줄 것인가

> **1.5 자료 · 오프닝에서는 안 띄운다.** Q4(통제 실패·fail-safe)가 오면 편다.

> **기준선 위치** Scope를 선언하는 것은 **기준**. Scope가 요구하는 통제를 만드는 것은 **구현**. 그게 실제로 작동하는지는 **판정**. 남는 위험은 **수용**.

**출처** AWS SRA Agentic AI Security Scoping Matrix

| Scope | 분류 | 사람의 위치 | 필요한 통제 |
|---|---|---|---|
| 1 | No Agency | 읽기 전용, 고정 워크플로 | 워크플로 무결성, 입출력 검증, audit |
| **2** | Prescribed Agency | **결과 있는 action은 사람 승인 필수** | **승인 워크플로 보호, 승인 우회 방지, approver 신원 검증, 승인 기록** |
| **3** | Supervised Agency | **사람이 시작하고 이후는 자율 실행** | **runtime 모니터링, 권한 경계, scope creep 방지, kill switch** |
| 4 | Full Agency | 스스로 시작, 지속 운영 | 지속 검증, 자동 격리, 변조 불가 human override, fail-safe |

### Scope 3 이상에서 요구되는 구조

    Primary Agent
      ▼  action / telemetry
    Independent Monitor          ← primary agent와 분리되어야 한다
      ▼
    Containment Controller       ← throttle · 권한 회수 · 세션 격리 · STOP
      ▼
    Human Override               ← kill switch를 agent runtime 밖에 둔다

| 용어 | 의미 |
|---|---|
| Agency boundary enforcement | 허용된 권한 범위 밖으로 나가지 못하도록 runtime에서 강제 |
| Automated containment | 위반 감지 시 **사람을 기다리지 않고** 영향 범위 축소·격리 |
| Tamper-resistant human override | 사람이 강제 중지할 수 있고 **에이전트가 그 수단을 수정·우회할 수 없다** |
| **Fail-safe** | 통제 실패 시 위험한 action을 계속하는 대신 **거부·중지·승인 요구**로 전환 |

**원칙으로 말한다 ★**
> **"Scope를 선언하는 것과 그 Scope가 요구하는 통제를 갖추는 것은 다른 일입니다.**
> 그래서 **Scope를 선언할 때 그 Scope의 필수 통제 목록을 기준에 같이 명시해야 한다고 봅니다.** Scope 3이면 runtime 모니터링·권한 경계·kill switch·자동 격리가 필수 항목입니다.
>
> 그리고 **통제가 실패할 때의 기본 거동을 정책에서 선언해야 합니다.** 탐지기가 응답하지 않을 때 통과시킬 것인지 거부할 것인지가 기준에 없으면 구현이 임의로 정하게 됩니다. AWS SRA 기준으로는 **거부·중지·승인 요구**로 가야 합니다.
>
> 덧붙이면, 여기서 **'안전하게'라는 말이 두 가지로 쓰입니다** — 가용성 관점의 안전(통과)과 보안 관점의 안전(거부)은 반대 방향입니다. **그래서 기준에는 거동을 명시적으로 적어야 합니다.**"

→ **요건만 말한다.** "실무에서 흔하다" 같은 일반화와 "코드에는 이렇게 적힌다" 같은 예시를 **뺐다** — 내 PoC 얘기로 들릴 여지를 없앤 것이다. 실측은 `../tech/`에 있고 **물으면 그때 답한다**(`00_note.md` Q4).

---

## 6. 정책이 살아 있게 만드는 구조 — 기준 변경 게이트

> **1.5 자료 · 오프닝에서는 안 띄운다.** 탭4 승인 화면 데모 직전, 또는 Q1(maintain)이 오면 편다.

> **기준선 위치** 이 루프의 게이트는 **기준 변경 승인**이고 그것만 내 자리다. **시스템 배포 승인(Go/No-go)은 판정 = Assurance**다. 두 승인을 섞으면 분리선 ③이 무너진다.

정책은 한 번 쓰고 끝나지 않는다. 운영 결과가 기준을 다시 바꾸고, **그 변경을 승인으로 통제**한다.

    [기준 정의]  정책 파일 (버전 관리)
        ↓ 정책 설정 / 테스트 명세
    [집행]  Gateway  +  경계 테스트
        ↓ 이벤트 (요청·응답·테스트 결과)
    [수집·평가]  위협 이벤트 저장소
        ↓ 집계·분석
    [위험 산출]  빈도 · 심각도 · 오탐율 가중
        ↓ 기준 변경 제안
    [기준 변경 승인]  ← ★ AI GRC 체계 운영 (중대 변경은 심의체계로 escalation)
        ↓
    [기준 정의]로 복귀

**설계 판단 두 개**

1. **자동 반영이 아니라 승인 경유.** 자동으로 둘 수 있었지만 승인을 필수로 했다.
   > "정책이 스스로 바뀌면 오너가 없어집니다. **이 승인 단계가 오너십의 물리적 위치입니다.**"

2. **위험 계산에 오탐율을 넣었다.**
   > "심각도와 빈도만 보면 오탐이 많은 룰도 위험해 보이고, 그러면 현장에서 통제를 꺼버립니다. **끄지 않게 만드는 것까지가 정책 오너의 일이라고 봤습니다.**"

**두 종류의 승인을 구분한다 ★**

| 무엇을 승인하나 | 누가 |
|---|---|
| **기준(정책) 변경** — 위 루프의 게이트 | **AI GRC** — 기준 체계의 운영이 내 Accountability다. 중대 변경은 심의체계로 escalation |
| **시스템 배포** — Go / No-go | **Release Approver (Assurance)** — evidence를 근거로 판정한다. **내 자리가 아니다** |

> "제가 승인하는 것은 **기준의 변경**입니다. **시스템을 배포해도 되는지는 Assurance가 evidence를 보고 판정합니다.** 이 둘을 섞으면, 제가 기준을 바꾸고 제가 그 기준으로 통과시키는 구조가 됩니다."

**그리고 이게 maintain에 대한 답이다**
> "유지·운영을 사람이 반복하는 게 아니라 **갱신 구조가 대신합니다.** 운영 실행과 판정은 Assurance가 가져가고, 저는 **그 판정이 가능한 기준과 증거 구조**를 유지합니다."

---

## 7. 규제를 게이트 조건으로

> **1.5 자료 · 오프닝에서는 안 띄운다.** 규제(PIPA·EU AI Act·AI기본법) 질문이 오면 편다.

> **기준선 위치** 규제 요건을 **기준**으로 번역하는 것이 내 산출물 ①이다. 그 기준의 충족 여부는 **판정**, 잔여 위험 수용은 **수용**이다.

**출처** AI·개인정보 3대 법령 핵심 개념 요약

| 축 | 핵심 개념 | 게이트 조건으로 |
|---|---|---|
| **PIPA** 국외이전 | 원칙 금지 + 법정 예외(동의·계약상 필요·인증·적정성 인정 등). **해외에 보관만 해도 국외이전** (서울 리전=해당 없음 / 도쿄·싱가포르=대상) | 추론·보관 리전 확인이 **심사 1번 항목** |
| **PIPA** 역외적용 | 벤더 본사가 해외라도 한국 이용자 정보를 처리하면 **벤더에게 직접 적용** | 벤더가 적용 대상임을 인지하는가 |
| **PIPA** 자동화된 결정 | 완전자동 결정 시 정보주체의 **거부권·설명요구권** 발생 | → **"승인 요구"라는 통제가 반드시 어휘에 있어야 하는 이유** |
| **EU AI Act** 4단계 | 금지 / 고위험(채용·신용·생체) / 제한적(챗봇·딥페이크) / 최소. **같은 AI라도 용도로 등급이 갈린다** | 용도 선언 → 등급 → 의무 수준 |
| **EU AI Act** 시행 | 2025.2.2 금지 · 2025.8.2 범용AI · 2026.8.2 투명성 · 2027.12.2 고위험(단독형) · 2028.8.2 고위험(제품내장형) | 게이트 발효 시점 |
| **AI기본법** | 고영향 / 생성형 / 대규모 분류. 사전 고지 + 결과물 표시 의무. 계도기간 중 | 도입 심사의 분류 질문 |

**연결 문장 — 개념이 통제로 이어지는 자리**
> "PIPA의 자동화된 결정 조항이 제 통제 어휘를 바꿨습니다. **사람에 관한 결정을 완전자동으로 하면 거부권과 설명요구권이 발생하므로, 허용/차단 이진이 아니라 '사람 확인 경유'라는 조치가 반드시 있어야 합니다.** 규제 요건이 정책 파일의 필드가 되는 지점입니다."

**시행 일정에서 얻은 판단**
> "고위험 두 건은 연기된 일정입니다. **규제 일정 자체가 움직이므로 게이트 조건을 날짜로 하드코딩하면 안 되고 버전 관리되는 정의에 둬야 합니다.**"

**답변 경계 (반드시 지킨다)**
- 개념 수준(원칙-예외 구조, 역외적용, 리전 판정, 4단계, 3분류)까지 답한다.
- **조문 번호·과징금 수치는 "확인해서 회신하겠습니다."**
- PIPA 국외이전 예외를 **"몇 가지"라고 개수로 말하지 않는다.** 근거 문서가 4개 + "등"으로 적고 있어 전체 목록을 확인하지 않은 상태다.

---

## 8. NIST 4 Function과의 정합성 (물으면)

> **Q6 자료 · 오프닝에서는 안 띄운다.** "첫 90일에 뭘 하시겠습니까" 질문이 오면 편다.

> GOVERN이 판단 기준을 정하고, MAP은 그 기준으로 위험 위치를 찾고, MEASURE는 위험의 크기와 통제 효과를 검증하며, MANAGE는 결과에 따라 위험을 처리하고 지속 추적한다.

| Function | 내 계층 |
|---|---|
| GOVERN | 경계·신뢰등급 선언, 승인 게이트, 규제 판정 |
| MAP | 경계 식별 — 어디서 데이터가 명령으로 바뀌는가 |
| MEASURE | **Assessment** — 통제가 집행됐는지 독립 검증 |
| MANAGE | 집행 + 기록 + 기준 재갱신 |

### 통제 목표 대비 내 위치 (첫 90일 질문용)

NIST Profile이 이 use case에 요구하는 통제 목표 7개에 내 자산을 대조한 결과다.

| 통제 목표 | 상태 |
|---|---|
| 외부 데이터의 지시가 시스템 권한을 바꾸지 못하게 한다 | **부분** |
| 모든 도구 action을 독립적으로 authorization한다 | **부분** |
| 실행 과정을 사후 추적할 수 있다 (출처→결정→정책→승인→action) | **있음** |
| 통제 변경 후 회귀를 방지한다 | **부분** |
| **고위험 action에 human approval을 요구한다** | ❌ **없음** |
| **최소권한을 적용한다 (negative test 포함)** | ❌ **미측정** |
| **개인정보 전달을 최소화한다 (masking)** | ❌ **없음** |

**말할 것**
> "**1개는 있고 3개는 부분이고 3개가 없습니다.** 없는 것이 human approval 증거, 최소권한 negative test, 개인정보 masking입니다. **그 빈칸이 제 첫 90일 목록입니다.**"

---

## 9. 이 문서를 쓰는 규율

1. **계층 어휘는 내가 만든 게 아니다.** 출처를 밝힌다. "제가 프레임워크를 만들었다"고 말하지 않는다.
2. **NIST Profile은 공식 NIST Profile이 아니다.** 문서 자신이 use-case Target Profile이라고 밝히고 있다.
3. **수치로 들어가지 않는다.** 이번 인터뷰에서 실험 수치와 코드는 "기술 인터뷰에서 자세히 말씀드리겠다"로 넘긴다.
4. **자기 진단 세 개는 먼저 꺼낸다** — 정책·가드레일 혼재 / fail-open / Scope 3에 Scope 1 통제. 먼저 말하면 강점, 질문받고 답하면 약점이 된다.
5. **역할 경계를 침범하지 않는다.** Control Owner 실행과 Internal Audit 보증은 내 자리가 아니라고 명시한다.

---

## 부록. 약어 — 처음 말할 때는 풀어서

**인터뷰에서 약어를 처음 쓸 때 괄호로 풀어 말한다.** 매니저가 그 약어를 모를 수 있고, 아는 경우에도 풀어 말하는 쪽이 정확하다. **말하는 순서에는 없다 — 필요할 때 이 부록에서 검색해서 쓴다.**

### 역할·조직

| 약어 | 원어 | 우리말 |
|---|---|---|
| **AI GRC** | AI **G**overnance, **R**isk and **C**ompliance | AI 거버넌스·위험·컴플라이언스 — **지원 포지션명에 포함**: `Staff AI Security Governance Engineer (AI GRC)` |
| **QE** | **Q**uality **E**ngineering | 품질 엔지니어링 |
| **TEVV** | **T**est, **E**valuation, **V**erification and **V**alidation | 시험·평가·검증·확인 |
| **PO** | **P**roduct **O**wner | 제품 책임자 (Scrum 공식 역할) |
| **SM** | **S**crum **M**aster | 스크럼 마스터 (Scrum 공식 역할) |
| **BO** | **B**usiness **O**wner | 사업 책임자 |
| **RAI Approver** | **R**esponsible **AI** Approver | 책임 있는 AI 승인자 |
| **MLOps** | **M**achine **L**earning **Op**eration**s** | 모델 운영 |
| **SOC** | **S**ecurity **O**peration **C**enter | 보안 관제 센터 |
| **RACI** | **R**esponsible · **A**ccountable · **C**onsulted · **I**nformed | 수행·최종책임·협의·통보 |

### 통제·구조

| 약어 | 원어 | 우리말 |
|---|---|---|
| **PDP** | **P**olicy **D**ecision **P**oint | 정책 결정 지점 — 허용 여부를 판단하는 곳 |
| **PEP** | **P**olicy **E**nforcement **P**oint | 정책 집행 지점 — 결정을 강제하는 곳 |
| **KRI** | **K**ey **R**isk **I**ndicator | 핵심 위험 지표 |
| **DLP** | **D**ata **L**oss **P**revention | 데이터 유출 방지 |
| **E2E** | **E**nd-**to**-**E**nd | 종단 간 — 경계를 통과하는 전체 경로 |
| **DoD** | **D**efinition **o**f **D**one | 완료 정의 (Scrum) |

### 프레임워크·규제

| 약어 | 원어 | 우리말 |
|---|---|---|
| **AI RMF** | AI **R**isk **M**anagement **F**ramework (NIST) | NIST AI 위험관리 프레임워크 |
| **NIST** | **N**ational **I**nstitute of **S**tandards and **T**echnology | 미국 국립표준기술연구소 |
| **SRA** | **S**ecurity **R**eference **A**rchitecture (AWS) | 보안 참조 아키텍처 |
| **RAI Standard** | **R**esponsible **AI** Standard (Microsoft) | 마이크로소프트 책임 있는 AI 표준 |
| **PIPA** | **P**ersonal **I**nformation **P**rotection **A**ct | 개인정보보호법 |
| **EU AI Act** | European Union **A**rtificial **I**ntelligence **Act** | EU 인공지능법 |
| **GPAI** | **G**eneral-**P**urpose **AI** | 범용 인공지능 |
| **PIPC** | **P**ersonal **I**nformation **P**rotection **C**ommission | 개인정보보호위원회 |

### AI·기술

| 약어 | 원어 | 우리말 |
|---|---|---|
| **LLM** | **L**arge **L**anguage **M**odel | 대형 언어 모델 |
| **RAG** | **R**etrieval-**A**ugmented **G**eneration | 검색 증강 생성 |
| **SaaS** | **S**oftware **a**s **a** **S**ervice | 서비스형 소프트웨어 |
| **IAM** | **I**dentity and **A**ccess **M**anagement | 신원·접근 관리 |
| **PoC** | **P**roof **o**f **C**oncept | 개념 검증 |
| **JD** | **J**ob **D**escription | 직무 기술서 |

**풀어 말할 때 예시**
> "AI GRC — **AI 거버넌스·위험·컴플라이언스** 역할입니다."
> "PDP와 PEP, 즉 **정책 결정 지점과 정책 집행 지점**을 분리합니다."
> "TEVV — **시험·평가·검증·확인**을 담당하는 조직입니다."
