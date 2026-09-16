# 작업 분담 — Claude Code vs Claude AI

필요 산출물 4종:
1. **AI lifecycle 전체**
2. **AI Responsibility** (책임 체계)
3. **2를 위한 AI System 구조** (model · harness · policy · evidence · test · e2e test)
4. **AI RMF Profile**

---

## 0. 이 호스트에서 실측한 도구 (분담의 근거)

| 도구 | 상태 | 의미 |
|---|---|---|
| `dot` (Graphviz) | **OK** | **한글 렌더 확인됨.** 실제 PNG/SVG 생성 가능 |
| 한글 폰트 | **OK** (Noto Sans/Serif CJK 80종) | 다이어그램 안 한글이 깨지지 않는다 |
| 생성 PNG 읽기 | **OK** | Claude Code가 **자기가 만든 그림을 다시 보고 검증**할 수 있다 |
| `pandoc` | OK | md → docx/html 변환 |
| `libreoffice` | OK | docx/pptx → PDF, 포맷 변환 |
| `mmdc` (Mermaid CLI) | **없음** | Mermaid는 소스만 쓸 수 있고 렌더 불가 |
| `python-docx` / `python-pptx` | **없음** | 필요하면 `uv pip install`로 설치 가능 (pypi 허용됨) |

`claude-lab/present/build.py`와 `claude-lab/papers/present/build.py`에 **docx·hwpx·pptx 빌더가 이미 있다.** 재사용 가능하지만 python-docx/pptx 설치가 선행된다.

---

## 1. 분담 기준 — 한 줄

| | 판단 기준 |
|---|---|
| **Claude Code** | **답이 근거 파일에 있는 것.** 정확성·일관성·교차검증·구조가 중요한 것 |
| **Claude AI** | **답이 눈에 있는 것.** 보기 좋은지, 읽히는지, 배치가 맞는지를 사람이 즉시 판단해야 하는 것 |

Claude Code는 그림을 **그릴 수 있지만** Graphviz 자동 배치에 갇힌다. 복잡한 lifecycle 스윔레인이나 발표용 레이아웃은 배치 엔진과 싸우게 된다.
Claude AI는 **아티팩트로 즉시 보면서 초 단위로 고칠 수 있다.** 색·여백·글자 크기·아이콘 같은 판단이 여기서 빠르다.

---

## 2. Claude Code가 효과적인 task

### ✅ 지금 바로 하는 것 (근거 파일이 있다)

| # | 산출물 | 왜 Code인가 | 근거 파일 |
|---|---|---|---|
| **1** | **AI lifecycle 11단계 정의표** — 단계별 수행 책임·최종 책임·검토 주체·출처 구분 | MS 문서 원문 명시 / 해석·재구성 / 제안을 **구분해서 표기**해야 한다. 이 구분이 거버넌스 문서의 신뢰성이고, 원문 대조는 Code 작업이다 | `05. MS RAI v2 운영모델` |
| **2** | **Responsibility 역할 9종 + lifecycle×역할 RACI + 애자일 대안 운영모델** | 표가 산출물의 본질이다. 그림이 아니다 | 같은 문서 |
| **3** | **System 구조 6요소 정의** (model·harness·policy·evidence·test·e2e test) + 요청 흐름 + 결정 지점 | NIST Profile §6 Target Control Architecture + 특허 구성요소 + 내 PoC를 **대조**해야 한다. 세 출처를 맞추는 작업 | `03. NIST Profile`, `06. 특허`, `tmac-poc/` |
| **4** | **AI RMF Profile 4 function 표** — GOVERN/MAP/MEASURE/MANAGE × Core ID × 적용 목표 × 필요 증적 | **원본 PDF에 깨진 텍스트와 오타가 있다** (`MANAGE 4. verlie` → 문서 자신이 `MANAGE 4.1`로 정정). 전사·정정·구조화가 필요하다 | `03. NIST Profile` §5 |
| **5** | **DOT 소스 4종 + PNG 렌더** | 한글 렌더 확인됨. 논리 구조 그림(흐름·계층·순환)은 Graphviz가 잘 한다. **만든 뒤 내가 다시 읽어 검증**한다 | — |
| **6** | **용어·수치 일관성 검증** | 4개 산출물 + 기존 manager/tech 문서 사이에 용어가 어긋나는지 검사. `claude-lab/spike/verify_numbers.py`와 같은 방식 | 전체 |

### ✅ 요청하면 추가로 할 수 있는 것

| 무엇 | 비고 |
|---|---|
| md → docx / PDF 변환 | pandoc + libreoffice로 가능 |
| pptx 초안 골격 생성 | `uv pip install python-pptx` 후 `claude-lab/present/build.py` 패턴 재사용 |
| 그림을 SVG로 출력 | 벡터라 HWP·PPT에 넣어도 깨지지 않는다 |
| 4종을 하나의 참조 문서로 병합 | 절 번호 교차참조 포함 |

### ❌ Code가 잘 못하는 것

- **발표용 시각 마감.** 색 조합, 여백, 글자 크기 균형 — 렌더하고 읽어서 확인은 되지만 반복이 느리다
- **복잡한 스윔레인 배치.** lifecycle × 역할 × 게이트를 한 장에 넣는 배치는 Graphviz가 억지로 푼다
- **아이콘·이미지가 들어가는 도해**
- **한 장에 다 넣기.** "이 그림을 A4 한 장에 읽히게" 같은 요구는 눈으로 봐야 한다

---

## 3. Claude AI가 효율적인 task

### 넘길 것

| # | 무엇 | 왜 AI인가 | 넘길 재료 |
|---|---|---|---|
| **A** | **lifecycle 전체도 발표용 마감** | 11단계 + 게이트 + 되돌아가는 화살표를 한 장에 읽히게 배치하는 것은 **눈의 문제**다. 아티팩트로 즉시 보면서 고치는 게 10배 빠르다 | Code가 만든 DOT + 단계 정의표 |
| **B** | **System 구조도 발표용 마감** | 요청 흐름(가로) × 통제 계층(세로) × 증거 sink(아래) × 테스트 주입점(위)이 겹친다. **4방향 배치는 Graphviz가 못 푼다** | Code가 만든 DOT + 6요소 정의 |
| **C** | **RACI 표 시각화** | 표는 Code가 만들지만, **색으로 R/A를 구분하고 한 장에 읽히게** 만드는 건 AI가 빠르다 | Code의 RACI 표 (markdown) |
| **D** | **RMF 4 function 순환도** | 원형 배치 + 함수 간 되돌아가는 관계. **원형은 Graphviz의 약점이다** | Code의 4 function 표 |
| **E** | **슬라이드 세트** (필요 시) | 레이아웃·색·분량 조절. 인터뷰용 3~5장이면 아티팩트가 압도적으로 빠르다 | 4종 산출물 md 전체 |
| **F** | **인터랙티브 HTML 도해** (선택) | 계층을 클릭하면 해당 역할·증거가 강조되는 형태. 매니저에게 노트북으로 보여주기 좋다 | 4종 산출물 md 전체 |

### Claude AI에 넘길 때 붙일 프롬프트 (그대로 복사)

**A — lifecycle 전체도**
```
첨부한 DOT 소스와 단계 정의표를 근거로, AI adoption lifecycle 전체도를
단일 SVG 아티팩트로 만들어줘.

요건:
- 11단계를 흐름으로, 그 중 "승인이 필요한 게이트" 4개(Reviewer 승인 /
  Release Go-No-go / 중대 residual risk 수용 / 재평가·중단)를 시각적으로 구분
- Gap Management에서 앞 단계로 되돌아가는 화살표를 반드시 표현
- Internal Audit이 전체를 가로질러 독립 검증하는 관계를 점선으로
- A4 가로 1장에서 읽히게. 글자 최소 10pt 상당
- 색은 3색 이내, 흑백 인쇄에서도 게이트가 구분되게 (선 종류나 채움 패턴 병행)
- 한국어 라벨. 영문 용어는 괄호 병기
내용을 바꾸지 말고 배치만 개선해줘. 단계 이름과 게이트 위치는 정의표가 정본이야.
```

**B — System 구조도**
```
첨부한 DOT과 6요소 정의표로 AI System 구조도를 SVG 아티팩트로 만들어줘.

축이 네 개라 배치가 핵심이야:
- 가로: 요청 흐름 (사용자 → Model → Harness → Policy → Guardrail → Tool)
- 세로: 통제 계층 (제안 / 검증 / 결정 / 집행)
- 아래: Evidence sink (모든 단계에서 기록이 내려온다)
- 위: Test 주입점 (Test와 E2E Test가 어느 지점을 검증하는지)

요건:
- Policy Decision Point의 출력이 3개(ALLOW / DENY / REQUIRE_APPROVAL)임을 명시
- REQUIRE_APPROVAL이 사람으로 가는 경로를 별도 표시
- Evidence가 무엇을 연결하는지(입력·context·정책버전·결정·승인·실행결과) 라벨
- Test와 E2E Test의 차이가 그림에서 구분되게
- A4 가로 1장. 한국어 라벨
```

**C — RACI 시각화**
```
첨부한 lifecycle × 역할 RACI 표를 한 장짜리 매트릭스 SVG로 만들어줘.
R(수행 책임)과 A(최종 책임)를 색과 기호로 구분하고, 같은 셀에 둘 다 있는 경우를
표현해줘. 행이 11개 열이 9개라 A4 가로 1장에 들어가야 해.
표의 내용은 바꾸지 말 것 — 근거 문서에서 전사한 것이야.
```

**D — RMF 4 function 순환도**
```
GOVERN / MAP / MEASURE / MANAGE를 순환도로 만들어줘.
- GOVERN이 판단 기준을 정하고, MAP이 그 기준으로 위험 위치를 찾고,
  MEASURE가 크기와 통제 효과를 검증하고, MANAGE가 처리·추적한다
- MEASURE와 MANAGE의 결과가 GOVERN으로 되돌아가는 관계를 표현
- 각 function에 이 use case의 핵심 질문 한 줄을 붙여줘 (첨부 표에 있음)
- GOVERN이 나머지를 감싸는 형태로 두는 것도 검토해줘 (NIST 원 구조가 그렇다)
```

---

## 4. 순서 — 왜 Code가 먼저인가

```
[Code]  내용 확정 (근거 파일 대조, 출처 구분 표기)
          ↓
[Code]  DOT 소스 + PNG 렌더 + 읽어서 검증
          ↓  ← 여기까지가 "정본". 내용은 더 이상 바뀌지 않는다
[AI]    발표용 시각 마감 (배치·색·한 장 맞춤)
          ↓
[Code]  (필요 시) docx/pptx 변환, 용어 일관성 재검증
```

**순서를 지켜야 하는 이유.** AI가 먼저 예쁜 그림을 만들면 **내용이 그림에 맞춰 바뀐다.** 단계 이름이 짧아지고 게이트가 생략된다. 거버넌스 문서에서 그건 사실이 바뀌는 것이다. 그래서 **Code가 정본을 고정한 뒤 AI에 넘긴다.**

반대로 Code가 시각 마감까지 하려 들면 렌더-확인 반복에 시간이 갈린다. 그 지점이 넘기는 선이다.

---

## 5. Code 작업 결과 — 완료

| 파일 | 내용 | 상태 |
|---|---|---|
| `manager/05_ai_lifecycle.md` | lifecycle 11단계 + 승인 게이트 4개 + 되돌아가는 경로 + 애자일 현실 보정 | ✅ |
| `manager/06_ai_responsibility.md` | 역할 9종 Accountability + **분리선 3개** + RACI + 애자일 대안 + escalation 6기준 | ✅ |
| `manager/07_system_architecture.md` | 6요소 정의 + 결정 3분기 + fail-safe + **내 PoC 대조(2개 없음/3개 어긋남)** | ✅ |
| `manager/08_ai_rmf_profile.md` | GOVERN 12 / MAP 14 / MEASURE 15 / MANAGE 12 전체 표 + residual risk 8종 | ✅ |
| `manager/figures/*.dot` | 그림 4종 소스 — **DOT이 정본** | ✅ |
| `manager/figures/*.png` `*.svg` | 렌더 결과. **4종 모두 눈으로 검증** | ✅ |
| `manager/figures/README.md` | 그림별 남은 배치 문제 + **AI 인계 프롬프트 4종** | ✅ |

**렌더 검증 결과**

| 그림 | 판정 |
|---|---|
| `responsibility` | **배치도 양호 — 그대로 발표용으로 쓸 수 있다** (`newrank=true`로 분리선 3개가 의도대로 쌓였다) |
| `rmf_cycle` | **배치도 양호** (GOVERN이 나머지 셋을 감싸는 NIST 원 구조) |
| `lifecycle` | 내용 정본 확정. 되돌아가는 점선 4개가 중앙에서 교차 → **AI로** |
| `architecture` | 내용 정본 확정. **네 방향 축을 Graphviz가 못 푼다 → AI 1순위** |

**출처 표기 규칙** — 4개 산출물 전체에 적용한다. `05. MS RAI v2` 문서의 방식을 그대로 쓴다.

| 표기 | 의미 |
|---|---|
| **원문 명시** | 참조 문서에 요구사항이 직접 적혀 있음 |
| **재구성** | 원문 요구사항을 lifecycle 운영 단계로 재배치한 것 |
| **제안** | 실제 조직 운영에 맞게 내가 제안한 것 |

이 구분이 없으면 매니저가 "이게 표준입니까, 당신 생각입니까"를 물었을 때 답이 없다.
