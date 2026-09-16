# AI GRC Engineer의 검토 범위 — v0.2

> **무엇을 하는 문서인가** `05_ai_lifecycle.md` §2-B의 「검토」 열을 **지원 포지션 관점에서 다시 읽은 것**이다.
> lifecycle 11단계 중 **내가 검토하는 곳이 어디이고, 없는 곳이 왜 없는가**를 정리한다.
>
> **지원 포지션** `Staff AI Security **Governance** **Engineer** (AI GRC)`
>
> **근거** `05_ai_lifecycle.md` §2-A·§2-B (MS Standard 원문 표) / `06_ai_responsibility.md` §1 (역할별 Accountability) / `02_structure.md` §0 (기준선)
>
> **버전** v0.2 — **조직 확인 반영: `Security Architecture`가 별도 팀이다.** 7단계 확정, 산출물 수신자 정정.
> v0.1은 `09_ai_grc_review_scope_v0.1.md`에 남겨 둔다(폐기).

---

## 요약 — 네 가지

| # | 발견 | 성격 |
|---|---|---|
| ① | **내 검토 6곳이 AI GRC의 Accountability 문구와 그대로 맞는다** | 확인 |
| ② | **내가 없는 4곳은 「빠진 것」이 아니라 분리선이다** | 해석 |
| ③ | **「AI GRC」와 「Security Architecture」는 별도 팀이다** → 7단계에 내가 없는 것이 **확정** | **확인 완료** |
| ④ | **Engineer이므로 「검토」에서 끝나지 않는다** | 해석 |
| ⑤ | **내 기준의 1차 수신자는 Security Architecture 팀이다** | v0.2 신규 |

---

## ① 내 검토는 6곳이고, 성격이 두 종류로 갈린다

`05` §2-B의 검토 열에서 AI GRC가 나오는 단계는 **1 · 2 · 4 · 6 · 8 · 9**다.

| 성격 | 단계 | 무엇을 보는가 (원문) |
|---|---|---|
| **분류·기준 정의** (전단계) | **1** AI use case 식별 | intended use와 stakeholder 식별 결과 |
| | **2** Impact Assessment | assessment 완전성과 risk classification |
| | **4** Responsible Release Criteria 정의 | 위험 coverage |
| **운영 추적·escalation** (후단계) | **6** Reviewer 승인 | 분야별 검토 또는 sign-off |
| | **8** Ongoing Monitoring | KRI와 control 상태 |
| | **9** Gap Management | remediation · residual risk · 기한 추적 |

**AI GRC의 Accountability 문구와 그대로 맞는다**

    기준 · 분류 · oversight · gap escalation 체계의 운영
    └──────┬──────┘   └────────┬─────────┘
       1 · 2 · 4          6 · 8 · 9

앞 세 곳이 **기준·분류**, 뒤 세 곳이 **oversight·gap escalation**이다. 원문 표가 스스로 맞아떨어진다.

**말할 것**
> "제 검토가 여섯 단계에 걸쳐 있는데 **성격이 두 종류입니다.** 앞의 1·2·4단계는 **분류와 기준 정의**이고, 뒤의 6·8·9단계는 **운영 추적과 escalation**입니다.
>
> 이게 AI GRC의 Accountability 문구 그대로입니다 — **기준·분류·oversight·gap escalation 체계의 운영.**"

---

## ② 내가 없는 4곳은 「빠진 것」이 아니라 분리선이다

검토 열에 AI GRC가 **없는** 단계는 **5 · 7 · 10 · 11**이다. 각각 이유가 있다.

| 단계 | 검토 주체 (원문) | 내가 없는 이유 |
|---|---|---|
| **5** Pre-release Evaluation | **개발팀과 분리된 평가자**가 성능·안전·보안·통제 효과성 검증 | **분리선 ①** — 시험은 QE/TEVV가 한다. **내가 기준을 만들고 내가 시험하면 기준과 판정이 한 사람에게 모인다** |
| **7** Deployment | Change Management와 **Security**가 승인된 configuration 확인 | **확정 — 내 자리가 아니다.** `Security Architecture`가 **별도 팀**이므로 이 Security는 그 팀이다 (③) |
| **10** 재평가 · 중단 | **Review Board**가 재승인 또는 중단 결정 | **분리선 ②** — 재승인·중단은 **결정**이고 내 자리가 아니다. **분류를 다시 하는 것은 3단계로 되돌아가는 것**이고 그때 내가 수행한다 |
| **11** Lifecycle 전체 Audit | 프로세스 준수와 control evidence를 독립 검증 | **분리선 ③의 최종 보장 장치** — 감사는 위임되지 않는다 |

**10단계의 논리를 한 번 더** 원문 A2.1~A2.3이 Sensitive·Restricted Use의 **정기 재검토**를 요구하고, 그 분류의 수행 책임이 3단계의 AI GRC다. 따라서 **재평가 시 분류를 다시 하는 것은 3단계로 되돌아가는 경로**이고, 10단계 자체의 검토 주체가 Review Board인 것과 모순되지 않는다.

**말할 것**
> "검토 열에서 제가 없는 곳이 네 군데인데, **빠진 게 아니라 의도된 것**입니다.
>
> 5단계 시험은 QE가 해야 합니다 — **제가 기준을 만들고 제가 시험하면 분리선이 무너집니다.** 대신 4단계에서 **무엇을 시험해야 하는지를 기준으로 못박는 것**이 제 일입니다.
>
> 10단계 재승인·중단은 결정이고, 11단계 감사는 독립성이 핵심입니다. **제가 들어가면 안 되는 자리입니다.**"

→ **이 답이 「오너십이 좁은 게 아니냐」는 질문을 선점한다.** 좁은 게 아니라 **경계가 설계된 것**이다.

---

## ③ 「AI GRC」와 「Security Architecture」는 별도 팀이다 — **확인 완료**

**조직 확인 결과** Cross-functional 조직에 **`Security Architecture` 팀이 별도로 존재한다.**

따라서 원문 검토 열의 배치가 **그대로 맞다.**

| 단계 | 원문 검토 열 | 확정된 해석 |
|---|---|---|
| **6** Reviewer 승인 | **AI GRC · Security · Privacy**가 분야별 검토 또는 sign-off | **세 자리가 실제로 분리되어 있다.** 나는 AI GRC 몫의 sign-off만 한다 |
| **7** Deployment | Change Management와 **Security**가 승인된 configuration 확인 | 이 Security는 **Security Architecture 팀**이다. **내 검토 범위가 아니다** |

**v0.1에서 열어 두었던 가정은 기각됐다** — AI GRC가 Security를 겸하지 않는다.

### 그래서 경계가 하나 더 생긴다 — 기준 vs 설계

| 자리 | 답하는 질문 | 산출물 |
|---|---|---|
| **AI GRC (나)** | **무엇을 충족해야 하는가** | 기준 · 분류 · 통제 요건 |
| **Security Architecture (별도 팀)** | **그것을 어떻게 만들 것인가** | 보안 설계 · 구조 |
| Development | 그 설계를 구현 | 코드 |

**말할 것 — 이 구분이 중요하다**
> "**Security Architecture가 별도 팀이라고 이해했습니다.** 그러면 경계가 분명합니다 — **저는 「무엇을 충족해야 하는가」를 정하고, Security Architecture는 「그것을 어떻게 만들 것인가」를 설계합니다.**
>
> 제가 설계까지 하면 그 팀의 자리를 침범하고, **제 기준이 특정 설계에 묶여 버립니다.** 기준은 설계 선택지를 열어 두는 쪽이 맞다고 봅니다."

→ **역질문** "Security Architecture 팀과 AI GRC의 산출물 경계를 어디로 보고 계십니까?"

## ④ Engineer이므로 「검토」에서 끝나지 않는다

4단계를 보면 AI GRC가 **수행 책임에도 있고 검토에도 있다.**

| 4단계 Responsible Release Criteria 정의 | 원문 |
|---|---|
| **수행 책임** | 개발, QE, Security, **AI GRC** |
| **검토** | QE가 측정 가능성, **AI GRC가 위험 coverage** |

3단계도 같다 — **수행 책임에 AI GRC**가 있다(최종 책임은 Responsible AI Approver).

| AI GRC가 수행 책임인 단계 | 하는 일 |
|---|---|
| **3** Sensitive·Restricted Use 분류 | 분류안을 만든다 |
| **4** Responsible Release Criteria 정의 | 기준을 만든다 |

**이게 `Engineer` 직함의 의미다.** 위험 coverage를 검토만 하는 게 아니라 **기준을 기계가 읽는 형태로 만드는 것**(policy-as-code)까지 한다. 그게 JD 1.1의 `Architect policy-as-code rule sets`다.

**말할 것**
> "4단계에서 저는 수행과 검토 양쪽에 들어갑니다. **위험 coverage를 검토하는 것만이 아니라 기준 자체를 기계가 읽는 형태로 만드는 것**까지가 제 일이라고 봅니다.
>
> **직함이 Engineer인 이유가 그것이라고 이해했습니다** — 문서로 된 기준을 **개발팀이 SW 구조에 넣을 수 있는 형태로 바꾸는 자리**입니다."

→ 이것이 기준선의 **산출물 ①**(개발팀용 기준과 가이드)이 나오는 지점이다.

---

## ⑤ 내 기준의 1차 수신자는 Security Architecture 팀이다 — v0.2 신규

기준선의 **산출물 ①**(개발팀용 기준과 가이드)의 수신자가 v0.1에서는 `Development · AI System Owner`였다. **Security Architecture가 별도 팀이면 그 앞에 한 단계가 더 있다.**

    기준 (AI GRC · 나)
      │ ① 통제 요건 · 기준
      ▼
    설계 (Security Architecture)          ← 1차 수신자. 요건을 보안 설계로 옮긴다
      │ 설계
      ▼
    구현 (Development · AI System Owner)  ← 2차. 설계를 코드로
      │
      ▼
    판정 (Assurance)  →  수용 (Risk / Business)

**기준선의 네 칸은 그대로다.** 「구현」 칸 안에서 **설계와 구현이 갈리는 것**이고, 내 산출물 ①이 **먼저 도달하는 곳이 Security Architecture**다.

**실무상 차이 — 기준을 쓰는 방식이 달라진다**

| 수신자가 개발팀일 때 | 수신자가 Security Architecture일 때 |
|---|---|
| 구현 가능한 수준으로 구체화해야 한다 | **요건 수준으로 두고 설계 선택지를 열어 둔다** |
| "이 필드를 이렇게 쓰라" | "**이 통제를 충족하라. 방법은 설계에서 정하라**" |

**말할 것**
> "제 기준이 처음 도달하는 곳이 **Security Architecture 팀**이라고 보면, 기준을 쓰는 방식이 달라집니다. **구현 방법까지 지정하면 설계 팀의 자리를 침범하니까요.**
>
> **요건 수준으로 쓰고 설계 선택지를 열어 두되, 「충족했다고 인정할 조건」은 제가 명확히 못박습니다.** 그게 Assurance가 판정할 수 있는 형태가 되어야 하니까요."

→ 이것이 **산출물 ①과 ②가 한 쌍으로 나가는 이유**다. 요건(①)만 주면 판정할 수 없고, 판정 조건(②)까지 같이 줘야 한다.

---

## 정리 — 한 장으로

    lifecycle 11단계에서 AI GRC Engineer의 위치

    수행 (R)   : 3 분류안 작성 · 4 기준 작성            ← Engineer, 산출물 ①
    검토 (C)   : 1 · 2 · 4 (분류·기준)                  ← 기준·분류
                 6 · 8 · 9 (sign-off·KRI·gap 추적)      ← oversight·escalation
    최종책임(A) : **없음**                               ← 기준 제공자, 승인하지 않는다
    부재       : 5 시험 · 10 결정 · 11 감사              ← 분리선 ①②③
                 7 배포 구성 확인                        ← Security Architecture 팀 (확정)

**한 문장**
> "저는 **3·4단계에서 만들고, 여섯 단계에서 검토하고, 어디에서도 최종 승인하지 않습니다.**
> 5·10·11단계에 제가 없는 것은 **분리선**이고, 7단계는 **Security Architecture 팀의 자리**입니다."

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| v0.1 | 2026-09-16 | 최초 작성. `05` §2-B를 JD 관점으로 재검토 — 발견 4건. **7단계 미확정** |
| **v0.2** | 2026-09-16 | **조직 확인 반영** — `Security Architecture`가 별도 팀. ③ 확정(7단계는 내 자리 아님), **⑤ 신설**(내 기준의 1차 수신자는 Security Architecture), 기준 vs 설계 경계 추가 |

**v0.1 대비 바뀐 것**
- ③ 「같은 자리일 수 있다」(가정) → **「별도 팀이다」(확정)**
- 7단계 검토: 「조직에 따라 갈림」 → **「Security Architecture 팀의 자리, 내 범위 아님」**
- 산출물 ① 수신자: `Development` → **`Security Architecture` → `Development`** (한 단계 추가)
- **기준 vs 설계** 경계 신설 — 나는 「무엇을」, Security Architecture는 「어떻게」
