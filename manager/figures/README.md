# figures/ — 그림 4종

| 파일 | 대응 문서 | 상태 |
|---|---|---|
| **`baseline.{dot,png,svg}`** | **`../02_structure.md` §0 — 기준선** | **정본 확정 · 배치 양호. 가장 먼저 띄우는 한 장** |
| `lifecycle.{dot,png,svg}` | `../05_ai_lifecycle.md` §2·§3·§4 | **정본 확정** — 배치 개선은 AI |
| `responsibility.{dot,png,svg}` | `../06_ai_responsibility.md` §1·§3 | **정본 확정 · 배치 양호** — 역할 경계 정정 반영본 |
| `architecture.{dot,png,svg}` | `../07_system_architecture.md` §2·§3 | **정본 확정** — 배치 개선은 AI |
| `rmf_cycle.{dot,png,svg}` | `../08_ai_rmf_profile.md` §1 | **정본 확정 · 배치도 양호** — 그대로 써도 된다 |

**DOT이 정본이다.** PNG·SVG는 파생물이다. 내용을 고칠 때는 `.dot`을 고치고 다시 렌더한다.

```bash
cd interview/manager/figures
for f in baseline lifecycle responsibility architecture rmf_cycle; do
  dot -Tpng -Gdpi=110 $f.dot -o $f.png
  dot -Tsvg $f.dot -o $f.svg
done
```

**SVG를 쓰는 게 좋다.** 벡터라 HWP·PPT에 넣어도 깨지지 않고 확대해도 글자가 유지된다.

---

## 렌더 환경 (실측)

| | |
|---|---|
| Graphviz `dot` | 있음. **한글 렌더 정상** |
| 한글 폰트 | Noto Sans / Serif CJK (80종) |
| Mermaid CLI (`mmdc`) | **없음** — Mermaid는 렌더 불가 |
| `pandoc`, `libreoffice` | 있음 — 문서·PDF 변환 가능 |

DOT에서 쓰는 폰트는 `fontname="Noto Sans CJK KR"`이다. 다른 환경에서 렌더할 때 이 폰트가 없으면 한글이 □로 나온다.

---

## 그림별 남은 배치 문제 (Claude AI로 넘길 것)

### `lifecycle.png`
- **되돌아가는 점선 4개가 중앙에서 교차**해 읽기 어렵다
- `use case 재정의 / 종료` 라벨이 **왼쪽 끝에서 잘린다**
- 게이트 4개(G1~G4)가 흐름 중간중간에 있어 **게이트라는 성격이 한눈에 안 보인다** — 별도 열로 빼는 게 낫다
- Internal Audit(11)의 점선 3개가 다른 선과 겹친다

### `architecture.png`
- 왼쪽에 **빈 공간이 크다.** 흐름이 오른쪽에 몰려 있다
- `TEST`와 `E2E TEST`가 우상단에서 **긴 점선으로 내려와** 다른 선과 교차한다
- Evidence로 내려가는 점선 6개가 **아래쪽에서 뭉친다**
- 네 방향 축(가로 흐름 / 세로 계층 / 아래 Evidence / 위 Test)을 **Graphviz가 못 푼다** — 이 그림이 AI로 넘길 1순위다

### `baseline.png`
기준선 전용 한 장. 네 진영 + 분리선 3개 + 내 산출물 두 갈래.
- 남은 문제 — **가로 배치라 「구현」과 「수용」이 대각으로 떨어져 있다.** 일직선으로 놓는 게 낫다
- **이 그림이 인터뷰의 첫 장이다.** AI 마감 우선순위로는 A·B 다음 세 번째지만, 실제 사용 빈도는 가장 높다

### `responsibility.png`
배치가 의도대로 나왔다. 네 진영(기준 / 구현 / Assurance / 수용)과 AI GRC의 두 산출물 화살표가 살아 있다.
- 남은 문제 하나 — **분리선 ③ 라벨이 오른쪽 끝에서 잘린다**
- **역할 경계 정정 반영본이다.** 이전 버전은 Release Approver를 내 자리로 표시했었다. Release Approver는 **Assurance**다

### `rmf_cycle.png`
배치가 의도대로 나왔다. **발표용으로도 그대로 쓸 수 있다.** 색·글꼴만 조직 템플릿에 맞추면 된다.

---

## Claude AI에 넘길 때 — 프롬프트

**공통 규칙 — 프롬프트 맨 앞에 반드시 붙인다**

> 내용을 바꾸지 마. 단계 이름·역할 이름·라벨·게이트 위치는 첨부한 정본 문서가 기준이야.
> **배치와 가독성만 개선해줘.** 줄이거나 합치거나 생략하지 말 것 — 거버넌스 문서라서 항목이 빠지면 사실이 바뀐다.

### A — lifecycle 전체도 (1순위)

```
첨부: manager/figures/lifecycle.dot + manager/05_ai_lifecycle.md

AI adoption lifecycle 전체도를 단일 SVG 아티팩트로 만들어줘.

[내용을 바꾸지 마. 11단계와 게이트 4개는 05_ai_lifecycle.md §2·§3이 정본이야.]

요건:
- 11단계를 주 흐름으로 세로 배치
- 승인 게이트 4개(G1 Sensitive·Restricted Use 분류 / G2 Reviewer 승인 /
  G3 중대 residual risk 수용 / G4 재평가·중단)를 주 흐름과 시각적으로 구분.
  별도 열이나 다른 모양으로 빼는 것을 검토해줘
- 각 게이트에 승인자를 반드시 표기
  (Responsible AI Approver / Release Approver·Risk Owner /
   Business Sponsor·Management / Review Board)
- Gap Management(9)에서 4·5·2단계로 되돌아가는 화살표 3개를 겹치지 않게.
  라벨은 "기준이 틀렸을 때" / "검증 재수행" / "위험 판단 변경"
- G4에서 1단계로 가는 "use case 재정의 / 종료" 경로 (지금 잘려 있음)
- Internal Audit(11)이 전체를 가로질러 독립 검증하는 관계를 점선으로
- A4 가로 1장에서 읽히게. 글자 10pt 상당 이상
- 색 3색 이내. 흑백 인쇄에서도 게이트가 구분되게 (채움 패턴이나 선 종류 병행)
- 한국어 라벨, 영문 용어는 그대로 (Release Approver 등은 번역하지 말 것)
```

### B — System 구조도 (1순위)

```
첨부: manager/figures/architecture.dot + manager/07_system_architecture.md

AI System 구조도를 단일 SVG 아티팩트로 만들어줘.

[내용을 바꾸지 마. 6요소와 결정 3분기는 07_system_architecture.md §2·§3이 정본이야.]

축이 네 개라서 배치가 핵심이야:
- 가로 또는 세로 주 흐름: Identity → 외부데이터 수집 → Context Builder →
  1 Model → 2 Harness → 3 Policy(PDP) → 4 Guardrail(PEP) → Tool 실행
- Policy의 출력이 3개다: ALLOW / DENY / REQUIRE_APPROVAL
  · DENY → 거부 + 기록
  · REQUIRE_APPROVAL → 사람 승인(approver 신원·승인 기록) → Guardrail로 합류
  · 이 3분기가 그림에서 가장 눈에 띄어야 한다 (규제 요건이 걸린 지점)
- 아래: 5 Evidence — 모든 단계에서 점선으로 기록이 내려온다.
  "입력·context·정책버전·결정·승인·실행결과를 연결해 기록"
  특히 Policy → Evidence 선에는 "정책 버전" 라벨
- 위 또는 옆: 6 Test와 6 E2E Test를 구분.
  · Test = 요소별 명세 준수 (Harness 등 개별 요소를 가리킨다)
  · E2E Test = Model에 입력 주입 → Tool 실행 관측.
    "선언된 통제가 실제로 집행되는가 = 정의·집행 불일치(drift) 검출"
- "외부 데이터 수집" 박스에 "◆ 신뢰 등급을 여기서 선언" 유지
- A4 가로 1장. 한국어 라벨. 왼쪽 빈 공간을 없애고 균형 있게
```

### C — RACI 매트릭스 (Graphviz로 안 만들었다)

```
첨부: manager/06_ai_responsibility.md §2

lifecycle 11단계 × 역할 9종 RACI 표를 한 장짜리 매트릭스 SVG로 만들어줘.

[표 내용을 바꾸지 마. §2가 정본이야. 셀을 비우거나 추가하지 말 것.]

요건:
- R(수행 책임)과 A(최종 책임)를 색과 기호로 구분. 같은 셀에 둘 다 있는 경우 표현
- C(검토·협의)는 약하게
- 승인 게이트 행 4개(3단계 / 6단계 / 중대 residual risk 수용 / 10단계)를 강조
- 행 12개 × 열 9개가 A4 가로 1장에 들어가야 한다.
  역할명은 2줄로 줄바꿈해도 됨 (Development / Owner)
- 표 아래에 "이 RACI는 제안이다 — MS Standard v2는 lifecycle별 상세 RACI를
  규정하지 않는다" 각주 유지
```

### D — RMF 4 Function 순환도 (선택)

```
첨부: manager/figures/rmf_cycle.dot + manager/08_ai_rmf_profile.md §1

현재 DOT도 쓸 만하지만, 원형 순환 배치를 원하면 만들어줘.

[4 function의 핵심 질문과 use case 적용 내용은 08_ai_rmf_profile.md §1이 정본.]

요건:
- GOVERN이 MAP·MEASURE·MANAGE를 감싸는 구조 (NIST 원 구조)
- MAP → MEASURE → MANAGE 순환, MANAGE → MAP "새 위험 발견" 되돌림
- 측정·처리 결과가 GOVERN의 판단 기준으로 되돌아가는 관계
- 각 function에 핵심 질문 한 줄 + 이 use case 적용 내용 한 줄
- 원형이 억지스러우면 현재 중첩 사각형 구조를 유지하고 다듬기만 해줘
```

---

## 넘기는 순서

```
[완료] Code — DOT 정본 + 렌더 + 눈으로 검증
   ↓
[다음] AI  — A·B 먼저 (배치가 실제로 문제인 것), 그다음 C, D는 선택
   ↓
[필요시] Code — SVG를 문서에 삽입, docx/PDF 변환, 용어 일관성 재검증
```

**AI가 만든 SVG를 받으면 이 폴더에 `*_final.svg`로 넣고, DOT은 남겨 둔다.** 내용이 바뀌었는지 대조할 기준이 필요하기 때문이다.

### E — 기준선 한 장 (사용 빈도 1위)

```
첨부: manager/figures/baseline.dot + manager/02_structure.md §0

거버넌스 역할 경계를 보여주는 기준선 도해를 단일 SVG 아티팩트로 만들어줘.

[내용을 바꾸지 마. 진영 이름·역할·분리선 문구는 02_structure.md §0이 정본이야.]

요건:
- 주 사슬 4칸을 일직선으로: 기준(AI GRC) → 구현(Development) → 판정(Assurance) → 수용(Risk/Business)
- 「기준」 칸에 ★ 내 자리 표시. 시각적으로 가장 강조
- 「판정 = Assurance」 칸 안에 4개 역할을 나열:
  Control Owner(실행·모니터링) / QE·TEVV(시험) / Release Approver(승인) / Internal Audit(감사)
  → Release Approver가 이 칸 안에 있다는 것이 그림의 핵심 메시지다
- 분리선 3개를 칸 사이에 명확히:
  ① 만든 사람이 판정하지 않는다        (구현 ↔ Assurance)
  ② 판정한 사람이 위험을 수용하지 않는다 (Assurance ↔ 수용)
  ③ 기준을 만든 사람이 그 기준으로 판정하지 않는다 (기준 ↔ Assurance) ← 가장 중요
- 기준에서 나가는 화살표 두 개:
  ① 개발팀용 기준·가이드 (규제 requirement → SW 구조)  → 구현
  ② evidence·audit 가능 구조 요건                      → 판정
- 한 장에 5초 안에 읽히게. 이 그림은 인터뷰에서 가장 먼저 띄운다
- A4 가로. 한국어 라벨, 역할명은 영문 그대로
```
