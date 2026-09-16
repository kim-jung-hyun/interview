# AI GRC Engineer의 검토 범위 — v0.1  ⚠️ 폐기

> **이 문서는 `09_ai_grc_review_scope_v0.2.md`로 대체되었다.**
> v0.1은 ③에서 「AI GRC와 Security가 같은 자리일 수 있다」를 **미해결 가정**으로 두었다.
> 조직 확인 결과 **`Security Architecture`가 별도 팀**이어서 그 가정은 기각됐다. **v0.2를 보라.**

> **무엇을 하는 문서인가** `05_ai_lifecycle.md` §2-B의 「검토」 열을 **지원 포지션 관점에서 다시 읽은 것**이다.
> lifecycle 11단계 중 **내가 검토하는 곳이 어디이고, 없는 곳이 왜 없는가**를 정리한다.
>
> **지원 포지션** `Staff AI Security **Governance** **Engineer** (AI GRC)`
>
> **근거** `05_ai_lifecycle.md` §2-A·§2-B (MS Standard 원문 표) / `06_ai_responsibility.md` §1 (역할별 Accountability) / `02_structure.md` §0 (기준선)
>
> **버전** v0.1 — 최초 작성. 조직 확인(D-1) 후 v0.2로 갱신 예정

---

## 요약 — 네 가지

| # | 발견 | 성격 |
|---|---|---|
| ① | **내 검토 6곳이 AI GRC의 Accountability 문구와 그대로 맞는다** | 확인 |
| ② | **내가 없는 4곳은 「빠진 것」이 아니라 분리선이다** | 해석 |
| ③ | **이 JD에서는 「AI GRC」와 「Security」가 같은 자리일 수 있다** | **확인 필요** |
| ④ | **Engineer이므로 「검토」에서 끝나지 않는다** | 해석 |

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
| **7** Deployment | Change Management와 **Security**가 승인된 configuration 확인 | 배포 구성 확인은 운영 통제다 → **단, ③ 참고** |
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

## ③ 이 JD에서는 「AI GRC」와 「Security」가 같은 자리일 수 있다 ★ 확인 필요

원문 검토 열이 두 곳에서 **다르게** 쓴다.

| 단계 | 원문 검토 열 | 함의 |
|---|---|---|
| **6** Reviewer 승인 | **AI GRC · Security · Privacy**가 분야별 검토 또는 sign-off | 세 자리가 **분리된 조직** 전제 |
| **7** Deployment | Change Management와 **Security**가 승인된 configuration 확인 | **AI GRC는 없고 Security만** 있다 |

그런데 지원 직함이 **`AI Security Governance Engineer`**다. **AI GRC와 Security가 한 자리라면 7단계 배포 구성 확인도 내 검토 범위에 들어온다.**

| 가정 | 7단계에서 내 위치 |
|---|---|
| AI GRC ≠ Security (별도 조직) | **검토 없음** — 원문 그대로 |
| **AI GRC = Security** (이 자리가 겸함) | **승인된 configuration 확인이 내 검토** |

**말할 것 — 역질문으로 쓴다**
> "원문 운영모델은 AI GRC와 Security를 별도 검토 주체로 씁니다. **그런데 이 포지션은 AI Security Governance라서 두 역할이 한 자리일 수 있습니다.**
>
> 그러면 **7단계 배포 시 승인된 configuration 확인도 제 범위에 들어옵니다.** 조직에서 두 역할이 분리되어 있는지, 아니면 이 자리가 둘을 겸하는지 확인이 필요합니다."

→ **역질문** "AI 보안 검토와 AI 거버넌스 검토가 같은 조직입니까, 분리되어 있습니까?"

⚠️ **이 문서 v0.2의 전제가 이것이다.** 답을 받으면 7단계 행을 확정한다.

---

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

## 정리 — 한 장으로

    lifecycle 11단계에서 AI GRC Engineer의 위치

    수행 (R)   : 3 분류안 작성 · 4 기준 작성            ← Engineer, 산출물 ①
    검토 (C)   : 1 · 2 · 4 (분류·기준)                  ← 기준·분류
                 6 · 8 · 9 (sign-off·KRI·gap 추적)      ← oversight·escalation
    최종책임(A) : **없음**                               ← 기준 제공자, 승인하지 않는다
    부재       : 5 시험 · 10 결정 · 11 감사              ← 분리선 ①②③
                 7 배포 구성 확인                        ← ③ 확인 필요

**한 문장**
> "저는 **3·4단계에서 만들고, 여섯 단계에서 검토하고, 어디에서도 최종 승인하지 않습니다.** 5·10·11단계에 제가 없는 것은 분리선이고, 7단계는 조직 구조에 따라 갈립니다."

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| **v0.1** | 2026-09-16 | 최초 작성. `05` §2-B를 JD 관점으로 재검토 — 발견 4건 |
| v0.2 (예정) | — | **D-1 답변 반영** — AI GRC와 Security의 조직 분리 여부에 따라 7단계 행 확정 |
