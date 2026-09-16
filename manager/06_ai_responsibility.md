# AI Responsibility — 책임 체계

> **근거** `05. Microsoft Responsible AI Standard v2 운영모델` / `03. NIST AI RMF Profile` GOVERN 2.1 — "Policy Owner, Implementation Owner, Assurance Owner 및 Risk Owner의 책임을 구분한다"
>
> 출처 표기 기준은 `05_ai_lifecycle.md` 머리말과 동일 (**MS Standard** / **MS Standard 기반 해석·재구성** / **Proposed Operating Model**)
>
> **이 문서 §3이 기준선의 근거 문서다.** 기준선 자체는 `02_structure.md` §0에 있고, 여기는 역할 9종 상세와 애자일 보정이다.
>
> 그림: `figures/baseline.svg` (기준선) · `figures/responsibility.dot` / `.svg` (역할 상세)

---

## 1. 역할별 핵심 Accountability

**MS Standard** — 원문 표

| 역할 | Accountability |
|---|---|
| **Business Owner** | AI use case의 **필요성, 편익, intended use 및 사업상 위험** |
| **AI System Owner** | AI system이 **승인된 요구사항과 control을 충족하도록 운영** |
| **Development Owner** | **설계·코드·모델 통합 및 기술적 remediation** |
| **QE / TEVV Owner** | **평가 방법의 적절성과 시험 결과의 신뢰성** |
| **Control Owner** | 특정 control의 **설계, 구현 상태 및 효과성** |
| **Risk Owner** | **Residual risk의 수용·완화·회피·이전 결정** |
| **Release Approver** | release criteria와 **evidence를 근거로 한 Go/No-go 결정** |
| **AI GRC** | **기준·분류·oversight·gap escalation 체계의 운영** |
| **Internal Audit** | governance와 control이 설계된 대로 작동하는지 **독립적으로 보증** |

---

## 2. Development Review · QE · AI GRC · Audit의 위치

Production 관점에서는 lifecycle마다 **수행 책임(Responsibility)**과 **최종 설명·의사결정 책임(Accountability)**을 분리해야 한다.

네 종류의 검토가 **서로 다른 것을 본다.**

| 검토 | 무엇을 보는가 | 주체 |
|---|---|---|
| **Development Review** | **설계와 구현이 요구사항에 맞는지** 검토 | **개발팀** (Development Owner) |
| **QE / TEVV** | **품질·안전·control effectiveness를 독립적으로 시험** | QE/TEVV Owner |
| **AI GRC** | **위험 분류, 통제 기준, residual risk 및 예외 처리** 검토 | **AI GRC ← 내 자리** |
| **Audit** | **프로세스와 통제가 실제로 준수되었는지 사후 독립 검증** | Internal Audit |

### 역할별로 lifecycle에서 무엇을 하는가

> **`05_ai_lifecycle.md` §2의 원문 11단계 표를 역할 기준으로 뒤집은 것이다.** 원문은 「단계별로 누가」이고 이 표는 「역할별로 어느 단계에서」다. **셀 내용은 원문 그대로이며 기호를 쓰지 않는다.**

| 역할 | **수행한다** (Responsibility) | **최종 책임을 진다** (Accountability) | **검토한다** |
|---|---|---|---|
| **Business Owner** | 1 use case 식별 | **1** use case 식별 · **2** Impact Assessment · **10** 재평가·중단 | — |
| **Product Owner** | 1 use case 식별 · 2 Impact Assessment · 10 재평가·중단 | — | — |
| **AI System Owner** | — | **2** Impact Assessment · **4** Release Criteria · **9** Gap Management | — |
| **Service / System Owner** | — | **7** Deployment · **8** Ongoing Monitoring | — |
| **개발 담당** (Development) | 2 Impact Assessment(AI/ML) · 4 Release Criteria · 9 Gap Management · 10 재평가 | — | — |
| **Platform · MLOps · DevOps · 운영팀** | 7 Deployment · 8 Ongoing Monitoring | — | — |
| **QE / TEVV** | 4 Release Criteria · 5 Pre-release Evaluation · 10 재평가 | **5** Pre-release Evaluation | 4 측정 가능성 · 8 주기적 평가 |
| **Security · Privacy 담당** | 2 Impact Assessment · 3 분류 · 4 Release Criteria · 5 Security Testing | — | 6 분야별 sign-off · 7 승인된 configuration 확인 |
| **Control Owner** | — | **9** Gap Management | — |
| **Risk Owner** | — | **6** Reviewer 승인 · **10** 재평가·중단 | — |
| **Release Approver** | — | **6** Reviewer 승인 | — |
| **Responsible AI Approver** | — | **3** Sensitive·Restricted Use 분류 | — |
| **Review Board** | — | — | 3 고위험 use case · **10 재승인 또는 중단 결정** |
| **Change Management** | — | — | 7 승인된 configuration 확인 |
| **Legal** | 3 Sensitive·Restricted Use 분류 | — | — |
| **지정 Reviewer** | 6 Reviewer 승인 | — | — |
| **Internal Audit** | 11 Lifecycle 전체 Audit | **11** (Audit 책임자) | — |
| ★ **AI GRC — 내 자리** | 3 분류 · 4 Release Criteria | **없다** | 1 intended use·stakeholder · 2 assessment 완전성·risk classification · 4 위험 coverage · 6 분야별 sign-off · 8 KRI·control 상태 · 9 remediation·residual risk·기한 |

**출처** 셀 내용은 **MS Standard** 원문 표를 옮긴 것이고, 역할 기준으로 뒤집은 것과 역할명 묶음은 **Proposed Operating Model**이다.

### 이 표를 읽는 법 세 가지

**1. AI GRC 행의 「최종 책임」이 비어 있다.**
수행은 두 곳(3·4단계), 검토는 여섯 곳이다. **기준선 그대로다 — 만들고 검토하되 판정하지 않는다.**

**2. 「최종 책임」이 두 개인 단계가 셋이다.**
- **6단계 Reviewer 승인** — Risk Owner(위험 수용)와 Release Approver(배포 결정)가 갈려 있다
- **2단계 Impact Assessment** — Business Owner와 AI System Owner
- **9단계 Gap Management** — Control Owner와 AI System Owner

→ **한 사람이 둘 다 갖지 않게 하는 것**이 분리선의 실제 작동 방식이다.

**3. 「검토」 열에만 나오는 주체가 셋이다.**
**Review Board**(3·10단계) · **Change Management**(7단계) · **Legal**(3단계 수행).
→ 조직에 이 셋이 없으면 **3·7·10단계의 검토가 비어 있게 된다.** 도입 시 먼저 확인할 항목이다.

**말할 것**
> "**이 표에서 제 행의 「최종 책임」이 비어 있습니다.** 수행이 두 곳, 검토가 여섯 곳입니다.
>
> **오너십이 넓은 게 좋은 게 아니라, 어디에서 멈추는지가 명확한 게 좋다고 생각합니다.** 3단계 분류를 제가 수행하지만 최종 책임은 Responsible AI Approver이고, 6단계 승인은 Risk Owner와 Release Approver가 나눠 갖습니다.
>
> 그리고 **최종 책임이 두 개인 단계가 셋 있습니다.** 위험을 수용하는 사람과 배포를 결정하는 사람이 갈려 있다는 뜻이고, **한 사람이 둘 다 가지면 분리선이 무너집니다.**"


---


### 조직 실제 역할로의 매핑

> **【미작성 — 조직 확인 후 작성】**
>
> MS Standard의 역할은 **직책 이름이 아니라 책임의 종류**다. 조직에 그 이름의 자리가 없어도 책임은 어딘가에 있어야 한다.
> **조직 역할 구조를 확인한 뒤 배정하는 것이 도입 초기 작업**이고, 지금 채워 넣으면 추측이 된다.
>
> **확인할 것**
> - Responsible AI Approver · Review Board · Release Approver · Internal Audit이 **실제 어느 조직인지**
> - Control Owner · Risk Owner에 해당하는 자리가 **있는지**
> - 없으면 **어느 기존 역할에 배정**할 것인지
>
> **인터뷰에서 이 절을 펼치지 않는다.** 물으면 이렇게 답한다 →
> "**MS 표준의 역할은 직책이 아니라 책임의 종류입니다.** 조직 역할 구조를 확인한 뒤 맞추는 것이 도입 초기 작업이라고 봅니다."


## 3. 역할 경계 — 기준선 ★

> 이 절이 **기준선의 정의**다. `02_structure.md` §0은 이 절의 요약이다.

### 네 진영

    ┌─ 기준을 만드는 쪽 ────────────────────────── ★ 내 자리 ─┐
    │ AI GRC    기준·분류·oversight·gap escalation 체계의 운영 │
    └─────────────────────────────────────────────────────────┘
        │ ① 기준·가이드              │ ② evidence·audit 가능 구조 요건
        ▼                            ▼  (설계·구현을 거쳐 Assurance에 도달)
    ┌─ 설계·구현하는 쪽 ────────────────────────────┐
    │ Security Architecture (별도 팀)  「어떻게」 설계 │
    │ Development Owner    설계·코드·모델 통합         │
    │ AI System Owner      승인된 요구사항과 control로 운영 │
    └──────────────────────────────────────────────┘
              ╎ 분리선 ①  — 만든 사람이 판정하지 않는다
    ┌─ 판정하는 쪽 = Assurance ─────────────────────────────────┐
    │ Control Owner     control의 설계·구현상태·효과성 → 실행·모니터링 │
    │ QE / TEVV Owner   평가 방법과 결과의 신뢰성        → 시험       │
    │ Release Approver  criteria와 evidence 기반 Go/No-go → 승인     │
    │ Internal Audit    설계된 대로 작동하는지 독립 보증  → 감사       │
    └───────────────────────────────────────────────────────────┘
              ╎ 분리선 ②  — 판정한 사람이 위험을 수용하지 않는다
    ┌─ 수용하는 쪽 ─────────────┐
    │ Risk Owner                │  residual risk 수용·완화·회피·이전 결정
    │ Business Owner            │  필요성·편익·사업상 위험
    └───────────────────────────┘

    분리선 ③ — **기준을 만든 사람이 그 기준으로 판정하지 않는다**   (내 자리 ↔ Assurance)

**Assurance는 실행·모니터링·감사 그리고 승인까지다.** Release Approver는 Assurance 쪽이다.

### 내 자리 = 「기준 제공자」 — 결정이 아니라 결정의 전제를 만든다

내 자리는 **AI GRC 하나**다. 지원 직함 `Staff AI Security Governance Engineer (AI GRC)`가 그걸 말한다 — **관리자가 아닌 개별 기여자(IC)이고, Governance는 기준을 세우는 일이다.**

두 가지를 만든다.

| # | 산출물 | 받는 쪽 | 내용 |
|---|---|---|---|
| **①** | **기준과 가이드** | **1차: Security Architecture** (별도 팀) → 2차: Development · AI System Owner | **규제 등의 requirement를 SW 구조에 넣을 수 있는 형태로** 변환한 기준 |
| **②** | **Assurance용 구조 요건** | Control Owner · QE/TEVV · Release Approver · Internal Audit | **assessment 가능한 evidence**와 **audit 가능한 구조**가 나오도록 하는 요건 |

### 근거는 원문 표의 구조다 — 내 해석이 아니다

`05_ai_lifecycle.md` §2의 11단계 표에서 **AI GRC는 「최종 책임」열에 한 번도 나오지 않는다.**

| AI GRC가 나오는 곳 | 어느 열 | 그 단계의 최종 책임 |
|---|---|---|
| 3단계 Sensitive·Restricted Use 분류 | **수행 책임** | Responsible AI Approver |
| 4단계 Release Criteria 정의 | **수행 책임** | AI System Owner |
| 6단계 Reviewer 승인 | **검토 / 분야별 sign-off** | Release Approver 또는 Risk Owner |
| 1·2·8·9단계 | **검토** | Business Owner / System Owner / Control Owner |

**말할 것 — 이번 인터뷰에서 가장 중요한 대사**
> **"제 자리는 「기준 제공자」입니다. 저는 승인하지 않습니다 — 승인이 가능하도록 만듭니다."**
>
> "제가 하는 일은 두 가지입니다. 하나는 **규제나 거버넌스 requirement를 개발팀이 SW 구조에 넣을 수 있는 기준과 가이드로 바꾸는 것**입니다. 다른 하나는 **그 구조가 Assurance가 assessment할 수 있는 evidence를 내고 audit 가능하도록 만드는 것**입니다.
>
> **실행·모니터링·감사·승인은 전부 Assurance입니다.** Release Approver도 Assurance 쪽이고 제 자리가 아닙니다. JD 1.2가 'Assurance팀이 execute·monitor·audit한다'고 쓴 것과 같습니다.
>
> 그리고 이건 제 해석이 아니라 **운영모델 표의 구조입니다** — AI GRC는 11단계 어디에서도 최종 책임 열에 나오지 않고, 수행 책임과 검토 열에만 나옵니다.
>
> **제 산출물은 결정이 아니라 결정의 전제입니다.** 제가 기준을 만들고 제가 그 기준으로 판정하면, 기준 자체를 검증할 사람이 없어집니다."

### 왜 이 경계가 더 강한가

| | |
|---|---|
| 게이트에 서지 않는다 | **개발 속도를 직접 막지 않는다.** 막는 쪽이 아니라 **통과 조건을 제공하는 쪽**이다 |
| 자기 채점을 하지 않는다 | 내 기준의 품질이 **Assurance의 판정 결과로 검증된다** |
| JD와 맞는다 | 1.5의 `establishing clear decision **Framework**` — **framework를 세우는 것이고 decision을 하는 것이 아니다** |

---

## 4. 조직 적용 — adaptation

> **【미작성 — 조직 확인 후 작성】**
>
> §1~§3의 **MS Standard 기준이 정본**이다. 실제 조직의 역할 구조에 맞춰 배정하는 작업은 **조직을 확인한 뒤** 한다.
>
> **근거 문서가 명시하는 제약 하나** — 일반적인 애자일/Scrum 조직에는 **Control Owner · Risk Owner · Release Approver가 직책으로 존재하지 않는다.** Scrum의 공식 Accountability는 Product Owner · Developers · Scrum Master 세 개뿐이다.
> 그래서 조직이 애자일 구조라면 **기존 역할에 책임을 배정하고 팀 권한을 넘는 위험만 관리계층으로 올리는** 형태가 된다. **구체 배정은 조직 확인 후.**

<details>
<summary>원문 보관 — 애자일 역할 기반 운영모델 (인터뷰에 쓰지 않음)</summary>

### (원문) 애자일 역할 기반 운영모델



**MS Standard** Scrum의 공식 Accountability는 **Product Owner / Developers / Scrum Master 세 가지뿐**이다. Control Owner·Risk Owner·Release Approver는 **애자일 기본 역할로 존재하지 않는다.**

> (원문) 애자일 팀은 Product Owner가 risk와 control requirement를 backlog로 관리하고 Developers가 구현·시험·모니터링한다. 팀의 권한을 초과하거나 중대한 residual risk가 존재하는 경우에는 조직에서 지정한 관리책임자 또는 governance review 체계로 escalation한다.

| 애자일 역할 | Responsibility — 수행 업무 | **Accountability — 최종 책임** |
|---|---|---|
| **Product Owner** | AI use case, intended use, stakeholder, 제품 요구사항, risk·control requirement를 Product Backlog에 반영하고 우선순위를 결정 | 제품 가치, 사용 범위, backlog 및 release 우선순위 |
| **Developers** | 모델·데이터·prompt·application·security control 구현, 테스트, monitoring instrumentation 및 gap 수정 | Sprint Increment의 품질과 Definition of Done 충족 |
| **Scrum Master** | AI GRC·Security·QE 검토가 workflow에 포함되도록 협업을 지원하고 impediment 제거 | Scrum Team의 프로세스 효과성과 지속적 개선 |
| **QE / Tester** ¹ | Release Criteria를 test case로 변환하고 성능·안전·보안·회귀시험 수행 | 시험 범위와 test evidence의 신뢰성 |
| **Security / Privacy 담당자** ¹ | Threat modeling, security·privacy requirement 정의 및 전문 검토 | 전문영역 검토 결과와 발견된 위험의 escalation |
| **운영 / MLOps 담당자** ¹ | 배포, logging, drift·failure monitoring, rollback과 incident response 수행 | Production 운영 안정성과 monitoring evidence |
| **AI GRC 담당자** ¹ | Impact Assessment, use classification, 정책·규제 적용 여부 및 미충족 gap 검토 | **Governance review의 일관성과 미해결 중요 위험의 escalation** |
| **Business Sponsor / Management** ² | 중대한 residual risk와 예외를 검토하고 배포·계속 운영·중단 결정 | 조직이 수용하는 중대한 AI 위험에 대한 **최종 의사결정** |

¹ 별도의 직책이 아니라 **Developers에 포함된 전문 역량이거나 공유 지원조직**일 수 있다.
² Scrum 역할은 아니지만 **팀의 권한을 넘는 위험에 대한 조직적 의사결정 주체**다.

**주목** 애자일 모델에서도 **AI GRC의 Accountability는 「escalation」까지다.** 결정이 아니다.

### Lifecycle별 현실적인 배정

| Lifecycle | 주 수행 역할 | **최종 판단** |
|---|---|---|
| AI use case 식별 | Product Owner | Product Owner |
| Impact Assessment | PO + Developers + Security/Privacy + AI GRC | **Product Owner가 완결성을 확보** |
| Sensitive·Restricted Use 분류 | AI GRC + Legal/Security | **조직 정책상 지정된 관리자** |
| Release Criteria 정의 | PO + Developers + QE | Product Owner |
| Pre-release Evaluation | Developers + QE | 팀은 결과를 확인하고 **PO가 release 판단** |
| 일반 Release | Product Owner + Developers | Product Owner |
| **고위험·예외 Release** | 팀이 **evidence 제출** | **Business Sponsor / Management** |
| Deployment | Developers / MLOps | Developers가 Increment와 배포 품질 책임 |
| Ongoing Monitoring | Developers / MLOps | **Product Owner가 제품 대응 우선순위 결정** |
| Gap Management | PO가 backlog화, Developers가 수정 | **PO가 우선순위, Developers가 구현 완료 책임** |
| **중대한 residual risk 수용** | 팀이 **escalation** | **Business Sponsor / Management** |
| **중단** | PO가 제안하거나 긴급 조치 | **권한 범위에 따라 PO 또는 Management** |

---

</details>

## 5. Escalation 경계

> **【EXAMPLE — 조직에 맞게 조정 필요】**
> 아래 6개 기준은 **근거 문서에 명시된 것**이다. 그러나 **"어디까지 팀이 자체 처리하고 어디서부터 올리는가"라는 경계선은 조직마다 다르다.**
> 여기 적은 경계는 **예시이고 내 판단**이다. **조직의 위험 허용 수준과 심의체계를 확인한 뒤 정해야 한다.**

### 팀이 자체적으로 수용하면 안 되는 사안 — 6개

**MS Standard 기반 해석** — 이 경우에만 관리계층이나 공식 심의체계로 escalation한다.

| # | 기준 |
|---|---|
| 1 | 법률·규제 위반 가능성 |
| 2 | 개인정보 또는 중요정보 유출 |
| 3 | Sensitive·Restricted Use 해당 |
| 4 | Responsible Release Criteria의 **중대한 미충족** |
| 5 | **승인 우회나 안전 control 실패** |
| 6 | 대규모 고객·사용자 영향 |

### 그 아래는 어떻게 하는가 — **EXAMPLE**

> ⚠️ **이 경계선은 내 판단이고 예시다.** 조직 확인 후 조정한다.

**EXAMPLE** — 일반 gap은 개발팀 안에서 끝낸다.

    Monitoring alert → 백로그 등록 → 우선순위 결정 → 수정 → 검증 → 배포

**말할 것 — 경계선이 판단임을 밝힌다**
> "거버넌스의 실제 일은 **게이트를 몇 개 두느냐가 아니라 어디에 두느냐**라고 봅니다.
>
> 전부에 게이트를 걸면 현장이 우회합니다. 아무것도 안 걸면 거버넌스가 없습니다. **위 여섯 가지는 근거 문서가 제시한 것이고, 그 아래를 어떻게 처리할지는 조직의 위험 허용 수준에 따라 달라집니다.**
>
> **예를 들면** 일반 gap은 개발팀 백로그에서 끝내게 두는 형태가 있습니다. **다만 이건 제 예시이고, 실제 경계는 조직의 심의체계를 확인한 뒤 정하는 게 맞다고 봅니다 — 그 조정 자체가 제 첫 일이라고 생각합니다.**"

---

## 6. 자기 진단 — 내 PoC의 역할 분리는 어떤 상태인가

| 분리선 | 내 PoC 상태 |
|---|---|
| ① 만드는 쪽 ↔ 판정하는 쪽 | **혼재.** 내가 만들고 내가 E2E 테스트를 썼다. 다만 **테스트가 내 구현의 실패를 실제로 잡아냈다** — 154건 중 13건 |
| ② 판정하는 쪽 ↔ 수용하는 쪽 | **없음.** residual risk를 수용할 주체가 정의되지 않았다 |
| ③ 기준 만드는 쪽 ↔ 판정하는 쪽 | **없음.** 내가 기준을 쓰고 내가 그 기준으로 판정했다 |

**말할 것 (먼저 꺼낸다)**
> "제 PoC는 1인 프로젝트라 세 분리선이 다 없습니다. **특히 ③이 없습니다** — 제가 기준을 쓰고 제가 그 기준으로 판정했습니다.
>
> 다만 **분리선 ①의 대용으로 테스트를 썼고, 그게 실제로 제 구현의 실패를 잡아냈습니다.** 혼자 하면서도 '내가 만든 걸 내가 판정하지 않는다'를 구조로 흉내낼 수 있는 방법이 테스트라고 생각합니다.
>
> ②와 ③은 **조직이 있어야 성립하는 것이고, 이 역할에서 하고 싶은 일이 그것입니다.**"

---

## 7. 물으면 답할 것

### "이 역할과 Assurance팀의 경계는 어디입니까?"

> 저는 **기준을 만들고, 그 기준이 SW 구조에 들어갈 수 있게 개발팀을 가이드하고, 그 구조에서 Assurance가 쓸 evidence가 나오게** 합니다.
> Assurance는 **그 기준으로 실행·모니터링·감사하고 승인**합니다. **Release Approver도 Assurance 쪽입니다.**
> **제가 판정까지 하면 기준 자체를 검증할 사람이 없어집니다.**

### "그러면 결정 권한이 없는 역할인가요?"

> **결정 권한이 아니라 결정 가능성을 만드는 역할이라고 봅니다.**
> Release Approver가 evidence를 근거로 Go/No-go를 하려면 **그 evidence가 애초에 나오는 구조**여야 합니다. Internal Audit이 독립 보증을 하려면 **audit 가능한 형태로 남아 있어야** 합니다. 그게 안 되어 있으면 승인은 서명이 되고 감사는 인터뷰가 됩니다.
> 그리고 escalation 경로는 제 Accountability입니다 — **미해결 중요 위험을 올리는 것까지가 제 책임**입니다.

### "residual risk는 누가 받습니까?"

> **Risk Owner와 Business Sponsor입니다. 제가 아닙니다.** 조직이 감수할 위험의 크기는 사업 책임자가 결정하는 것이고, 저는 그 판단에 필요한 근거 — **무엇이 남았고 무엇으로 확인했는지** — 를 만드는 쪽입니다.

### "AI GRC가 개발을 막는 조직이 되지 않겠습니까?"

> **저는 게이트에 서지 않습니다.** §5의 여섯 가지만 escalation 대상이고 나머지는 팀 백로그에서 끝냅니다.
> 그리고 게이트를 걸 때 **무엇을 제출하면 통과인지를 먼저 정해 두는 것**이 제 일입니다. **통과 조건이 없는 게이트가 개발을 막습니다.**

### "그 역할들이 우리 조직에 없으면요?"

> **§4가 그 경우의 배정입니다.** Control Owner·Risk Owner·Release Approver는 애자일 조직에 없는 직책입니다. 그래서 Product Owner가 risk와 control requirement를 backlog로 갖고, 팀 권한을 넘는 것만 관리계층으로 올립니다.
> **역할표를 조직에 강요하는 게 아니라 조직 구조에 책임을 배정하는 순서가 맞다고 봅니다.**
