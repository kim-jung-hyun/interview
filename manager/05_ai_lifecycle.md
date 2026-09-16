# AI Lifecycle 전체 — Responsibility · Accountability 운영모델

> **근거** `05. Microsoft Responsible AI Standard v2 — AI adoption lifecycle별 Responsibility·Accountability 운영모델`
>
> **기준선** `02_structure.md` §0 — 기준(AI GRC) → 구현 → 판정(Assurance) → 수용.
> 이 문서는 **기준선의 각 칸이 lifecycle의 어느 단계에 붙는지**를 보여준다.
>
> 그림: `figures/lifecycle.dot` / `.svg`

## 출처 표기 기준

매니저가 "이게 표준입니까, 당신 생각입니까"를 물을 때 답이 있어야 한다. **원문이 쓰는 표기를 그대로 쓴다.**

| 표기 | 의미 |
|---|---|
| **MS Standard** | Microsoft 문서에 요구사항이 **직접 명시**됨 |
| **MS Standard 기반 해석·재구성** | 원문 요구사항을 **lifecycle 운영 단계로 재배치**한 내용 |
| **Proposed Operating Model** | Development·QE·GRC·Audit 역할 및 Accountability를 **실제 조직 운영에 맞게 제안**한 내용 |

**MS Standard v2가 제시하는 것** Impact Assessment, reviewer approval, Responsible Release Criteria, pre-release·ongoing evaluation, gap management 요구사항.

**규정하지 않는 것** **lifecycle별 상세 RACI**와 **Development·QE/TEVV·AI GRC·Internal Audit의 역할 배정.**

> 아래 표의 조직 및 역할 구조는 해당 요구사항을 production 환경에서 운영하기 위해 재구성한 **Proposed Operating Model**이다.

---

## 1. 전제 — 수행 책임과 최종 책임을 분리한다

Production 관점에서는 lifecycle마다 **수행 책임(Responsibility)**과 **최종 설명·의사결정 책임(Accountability)**을 분리해야 한다.

### 네 종류의 검토 — 보는 대상이 다르다

| 검토 | 무엇을 보는가 |
|---|---|
| **Development Review** | **설계와 구현이 요구사항에 맞는지** 검토 |
| **QE / TEVV** | **품질·안전·control effectiveness를 독립적으로 시험** |
| **AI GRC** | **위험 분류, 통제 기준, residual risk 및 예외 처리** 검토 |
| **Audit** | **프로세스와 통제가 실제로 준수되었는지 사후 독립 검증** |

**말할 것**
> "네 가지가 다 '검토'라고 불리는데 보는 대상이 다릅니다. **Development Review는 설계가 요구사항에 맞는지, QE/TEVV는 통제가 실제로 효과가 있는지, AI GRC는 위험 분류와 기준이 맞는지, Audit은 그 과정이 준수됐는지를 봅니다.**
>
> 이걸 구분하지 않으면 '검토했다'는 말이 무슨 뜻인지 알 수 없습니다. **그리고 제 자리는 세 번째입니다** — 위험 분류와 통제 기준과 예외 처리입니다. 시험하는 것도 감사하는 것도 제 자리가 아닙니다."

---

## 2. Lifecycle 11단계 — 원문 표

> **6열 한 장이 화면에서 안 읽히므로 세 표로 나눴다.** 내용은 원문 그대로이고 열만 분리했다.
> 2-A 책임 · 2-B 검토 · 2-C 출처 근거. **세 표의 행 번호는 같다.**

### 2-A. 책임 — 누가 수행하고 누가 최종 책임을 지는가

| # | Lifecycle | 수행 책임 (Responsibility) | **최종 책임 (Accountability)** |
|---|---|---|---|
| 1 | **AI use case 식별** | Product Owner, Business Owner | **Business Owner** |
| 2 | **Impact Assessment** | Product, AI/ML, Security, Privacy 담당자 | **Business Owner 또는 AI System Owner** |
| 3 | **Sensitive·Restricted Use 분류** 🚪 | **AI GRC**, Legal, Privacy, Security | **Responsible AI Approver** |
| 4 | **Responsible Release Criteria 정의** | 개발, QE, Security, **AI GRC** | **AI System Owner** |
| 5 | **Pre-release Evaluation** | QE/TEVV, Security Testing | **QE 또는 Validation 책임자** |
| 6 | **Reviewer 승인** 🚪 | 지정 Reviewer | **Release Approver 또는 Risk Owner** |
| 7 | **Deployment** | Platform, MLOps, DevOps, 운영팀 | **Service/System Owner** |
| 8 | **Ongoing Monitoring** | 운영팀, MLOps, SOC, Model Monitoring | **Service/System Owner** |
| 9 | **Gap Management** | 개발, 데이터, 보안 또는 운영 담당자 | **Control Owner 또는 System Owner** |
| 10 | **재평가 · 중단** 🚪 | Product, 운영, 개발, QE | **Business Owner 또는 Risk Owner** |
| 11 | **Lifecycle 전체 Audit** | Internal Audit 또는 Independent Assurance | **Audit 책임자** |

🚪 = 승인 게이트 (§3)

### 2-B. 검토 — 누가 무엇을 본다

| # | Lifecycle | 검토 (Review · QE · Audit) |
|---|---|---|
| 1 | AI use case 식별 | AI GRC가 intended use와 stakeholder 식별 결과 검토 |
| 2 | Impact Assessment | AI GRC가 assessment 완전성과 risk classification 검토 |
| 3 | Sensitive·Restricted Use 분류 | 고위험 use case는 **Review Board** 검토 |
| 4 | Responsible Release Criteria 정의 | QE가 측정 가능성, AI GRC가 위험 coverage 검토 |
| 5 | Pre-release Evaluation | **개발팀과 분리된 평가자**가 성능·안전·보안·통제 효과성 검증 |
| 6 | Reviewer 승인 | AI GRC·Security·Privacy가 분야별 검토 또는 **sign-off** |
| 7 | Deployment | Change Management와 Security가 승인된 configuration 확인 |
| 8 | Ongoing Monitoring | QE가 주기적 평가, AI GRC가 KRI와 control 상태 검토 |
| 9 | Gap Management | AI GRC가 remediation·residual risk·기한 추적 |
| 10 | 재평가 · 중단 | **Review Board가 재승인 또는 중단 결정** |
| 11 | Lifecycle 전체 Audit | 프로세스 준수와 control evidence를 독립 검증 |

> **AI GRC Engineer 관점의 검토 범위 분석은 별도 문서** → `09_ai_grc_review_scope_v0.2.md`

### 2-C. 출처 구분 및 근거

| # | 출처 구분 | 근거 |
|---|---|---|
| 1 | **MS Standard 기반 재구성** | A1.1, A3.1, A3.2는 개발 초기 Impact Assessment와 intended use·입출력·한계 문서화를 요구. 구체적 역할 배정은 제안 |
| 2 | **MS Standard** | A1.1은 초기 Impact Assessment 수행, A1.2는 지정 reviewer 검토와 승인, A1.3은 정기·변경 시 갱신 요구 |
| 3 | **MS Standard** | A2.1~A2.3은 Restricted Use 및 Sensitive Use 식별·보고·정기 재검토 요구. 담당 조직명은 제안 |
| 4 | **MS Standard** | A3.3, A5.5 및 각 원칙별 요구사항에서 metric·error type·Responsible Release Criteria 정의 요구. 역할 배정은 제안 |
| 5 | **MS Standard 기반 해석** | A3.4~A3.5는 evaluation plan, pre-release evaluation과 ongoing evaluation 주기 문서화를 요구. 독립 QE 조직 지정은 제안 |
| 6 | **MS Standard** | A1.2는 지정 reviewer의 검토와 필수 승인 확보 요구. Release Approver·Risk Owner 구조는 제안 |
| 7 | **Proposed Operating Model** | MS Standard에 이와 같은 배포 RACI는 없음. A5.1의 배포 중·배포 후 운영·감독 stakeholder 식별 요구를 production 구조로 확장 |
| 8 | **MS Standard 기반 재구성** | A3.5 및 각 Goal의 Ongoing Evaluation Checkpoint는 평가 주기 정의를 요구. 구체적인 monitoring 조직과 KRI 운영은 제안 |
| 9 | **MS Standard + 제안** | A5.7, T1.6 등은 release criteria 미충족 시 reviewer와 협의하여 gap management plan을 문서화하도록 요구. Control Owner와 escalation workflow는 제안 |
| 10 | **MS Standard 기반 재구성** | A1.3은 연례·새 intended use·release stage 변경 시 재평가 요구. A3.7은 근거가 부족하거나 반증되면 gap 해소 또는 **system 중단**을 요구. 의사결정 역할은 제안 |
| 11 | **Proposed Operating Model** | MS Standard v2 General Requirements에 lifecycle 전체 Internal Audit RACI는 명시되지 않음 |


### 기준선으로 이 표를 읽으면

| 기준선 칸 | lifecycle 단계 |
|---|---|
| **기준** (내 자리) | 3 분류 **수행** · 4 Criteria 정의 **수행** · 1·2·8·9 **검토** · 6 분야별 **sign-off** |
| **구현** | 7 Deployment · 9 remediation 구현 |
| **판정** (Assurance) | 5 Pre-release Evaluation · 6 Reviewer 승인 **최종 책임** · 8 주기 평가 · 11 Audit |
| **수용** | 2·10 최종 책임(Business/Risk Owner) · 중대 residual risk 수용 |

### 이 표에서 반드시 짚어야 할 것 ★

**AI GRC는 11단계 어디에서도 「최종 책임」이 아니다.** 등장 위치를 보면:

| AI GRC가 나오는 곳 | 어느 열 |
|---|---|
| 3단계 Sensitive·Restricted Use 분류 | **수행 책임** (최종 책임은 Responsible AI Approver) |
| 4단계 Release Criteria 정의 | **수행 책임** (최종 책임은 AI System Owner) |
| 1·2·8·9단계 | **검토** 열 |
| 6단계 Reviewer 승인 | **검토 / 분야별 sign-off** (최종 책임은 Release Approver 또는 Risk Owner) |

**말할 것 — 역할 경계의 근거를 원문에서 가져온다**
> "이 표에서 제가 맡고 싶은 AI GRC는 **최종 책임 열에 한 번도 나오지 않습니다.** 수행 책임과 검토 열에만 나옵니다.
>
> **저는 승인하지 않습니다. 승인이 가능하도록 만듭니다.** 6단계 승인의 최종 책임은 Release Approver 또는 Risk Owner이고, 저는 거기서 분야별 검토와 sign-off를 합니다. 3단계 분류도 제가 수행하지만 최종 책임은 Responsible AI Approver입니다.
>
> **이게 제가 원문에서 읽은 역할 경계입니다.** 제 해석이 아니라 표의 구조입니다."

---

## 3. 승인 게이트 네 개

lifecycle에서 **승인 없이는 다음으로 못 가는 지점**이다.

| 게이트 | 판단 | **최종 책임** | 내 위치 |
|---|---|---|---|
| **G1** Sensitive·Restricted Use 분류 (3) | 이 use case를 해도 되는가 | **Responsible AI Approver** / 고위험은 Review Board | **수행** — 분류안을 만든다 |
| **G2** Reviewer 승인 (6) | 배포해도 되는가 | **Release Approver 또는 Risk Owner** | **분야별 sign-off** — 승인자가 아니다 |
| **G3** 중대 residual risk 수용 | 남은 위험을 조직이 받아들이는가 | **Risk Owner / Business Sponsor** | **근거 제공** — 수용 결정은 내 것이 아니다 |
| **G4** 재평가 · 중단 (10) | 계속 운영해도 되는가 | **Business Owner 또는 Risk Owner** / Review Board 결정 | **재평가 근거 제공** |

**말할 것**
> "게이트가 네 개인데 **어느 게이트에도 제가 최종 승인자로 서지 않습니다.** 저는 각 게이트의 **통과 조건과 제출 근거를 정의하는 쪽**입니다.
>
> **G3이 특히 그렇습니다** — 조직이 감수할 위험의 크기는 사업 책임자가 결정하는 것이고, 저는 '무엇이 남았고 무엇으로 확인했는지'를 만드는 쪽입니다.
>
> 그리고 **G4에 중단이 들어 있는지가 그 체계가 실제로 작동하는지의 시험지라고 봅니다.** 원문도 A3.7에서 '근거가 부족하거나 반증되면 gap 해소 또는 system 중단'을 요구합니다. **중단 권한이 없는 게이트는 게이트가 아니라 결재입니다.**"

→ **역질문으로 연결한다** — "배포 중단(hold) 결정은 어느 역할이 갖고 있습니까?"

---

## 4. 되돌아가는 경로 — lifecycle은 직선이 아니다

    8 Ongoing Monitoring
        │ alert
        ▼
    9 Gap Management ─────┬──▶ 4 Release Criteria 재정의   (기준 자체가 틀렸을 때)
        │                 ├──▶ 5 Pre-release Evaluation    (검증을 다시 해야 할 때)
        │                 └──▶ 2 Impact Assessment 갱신    (위험 판단이 바뀔 때)
        │ 중대 위험
        ▼
    G3 residual risk 수용 판단 ──▶ 10 재평가·중단
                                       │
                                       └──▶ 1 use case 재정의 또는 종료

    11 Internal Audit ┄┄┄┄▶ 전 단계를 가로질러 독립 검증 (주기적)

**출처** 원문 A5.7·T1.6이 release criteria 미충족 시 **reviewer와 협의하여 gap management plan을 문서화**하도록 요구한다. 되돌아가는 대상 단계 배정은 **제안**이다.

**말할 것**
> "**Gap Management가 이 체계의 심장입니다.** 모니터링에서 뭔가 발견됐을 때 어디로 되돌아가는지가 정해져 있어야 합니다. 기준이 틀렸으면 4단계로, 검증이 부실했으면 5단계로, 위험 판단이 바뀌었으면 2단계로 갑니다.
>
> **되돌아가는 경로가 없으면 모니터링은 로그만 쌓습니다.** 그리고 이 단계의 최종 책임은 Control Owner이고, 저는 remediation과 residual risk와 기한을 추적하는 쪽입니다."

---

## 5. 현실 보정 — 애자일 조직에는 그 역할이 없다

**출처 원문** 일반적인 애자일/Scrum 조직에는 Control Owner, Risk Owner, Release Approver가 **Scrum 역할로 존재하지 않는다.** Scrum의 공식 Accountability는 **Product Owner / Developers / Scrum Master 세 가지뿐**이다.

> (원문) 애자일 팀은 Product Owner가 risk와 control requirement를 backlog로 관리하고 Developers가 구현·시험·모니터링한다. 팀의 권한을 초과하거나 중대한 residual risk가 존재하는 경우에는 조직에서 지정한 관리책임자 또는 governance review 체계로 escalation한다.

상세 배정은 `06_ai_responsibility.md` §3.

### 일반 gap은 애자일 안에서 끝난다

    Monitoring alert → Product Backlog 등록 → PO 우선순위 결정 → Developers 수정 → QE 검증 → 배포

### 팀이 자체 수용하면 안 되는 것 — 이때만 escalation

**MS Standard 기반 해석** — 법률·규제 위반 가능성 / 개인정보 또는 중요정보 유출 / Sensitive·Restricted Use 해당 / Responsible Release Criteria의 **중대한 미충족** / 승인 우회 또는 안전 control 실패 / 대규모 고객·사용자 영향

> **【EXAMPLE — 조직에 맞게 조정 필요】** 그 아래를 어떻게 처리할지(예: 일반 gap은 팀 백로그에서 끝낸다)는 **조직의 위험 허용 수준과 심의체계에 따라 다르다.** 상세는 `06_ai_responsibility.md` §5.

**말할 것 — 실무성을 보이는 대목**
> "**MS 표준의 역할은 직책이 아니라 책임의 종류입니다.** 조직에 Control Owner나 Risk Owner라는 자리가 없어도 그 책임은 어딘가에 있어야 합니다.
>
> 그리고 거버넌스의 실제 일은 **게이트를 몇 개 두느냐가 아니라 어디에 두느냐**라고 봅니다. 전부에 걸면 현장이 우회하고, 아무것도 안 걸면 거버넌스가 없습니다.
>
> **위 여섯 가지는 근거 문서가 제시한 것이고, 그 아래 경계는 조직의 위험 허용 수준에 따라 달라집니다. 그 조정이 제 첫 일이라고 생각합니다.**"

---

## 6. 내 경력과 겹치는 지점 (물으면)

| AI lifecycle | 내가 해본 것 |
|---|---|
| 4 Responsible Release Criteria 정의 | Security Requirement와 Verification 기준 정리 |
| 5 Pre-release Evaluation | 검증팀과 분리된 시험, Evidence 기반 Assessment 구조 |
| 6 Reviewer 승인 | Production Release Go/No-go 리딩 |
| 7~8 Deployment · Monitoring | 출시 후 운영 사이클 |
| 9 Gap Management | 출시 후 이슈 우선순위 조정과 재배포 |

**새로운 것** 2 Impact Assessment / 3 Sensitive·Restricted Use 분류 / 10 재평가·중단 — **AI 특유의 단계**이고 배워야 할 부분이다.

**말할 것**
> "4번부터 9번까지는 제품 보안에서 해온 것과 구조가 같습니다. **새로운 건 2·3·10번입니다** — 영향평가, 민감·제한 용도 분류, 그리고 근거가 반증되면 시스템을 중단한다는 개념입니다. 제조업 릴리즈에는 '반증되면 중단'이라는 단계가 없습니다."
