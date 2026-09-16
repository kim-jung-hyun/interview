# 실험 결과

실행일: 2026-09-02
환경: Python 3.12.14 / langgraph 1.2.11 / anthropic 1.3.0 / httpx2 2.12.0
모델: Amazon Bedrock `ap-northeast-2` — Claude Haiku 4.5, Claude Sonnet 5
온도: SDK 기본값, `max_tokens` = 4096 (전 조건 동일)

수치 표는 `spike/audit_tables.md`가 생성한다. **이 문서에 숫자를 손으로 옮기지 않는다.**
재생성: `.venv/bin/python spike/audit_tables.py`

    유효 실행 55회 / tool argument 1,102개 / 4개 조건
    제외: stop_reason=max_tokens 21회, max_tokens≠4096 37회

에이전트는 run당 1회 실행하고, 관측 조건은 같은 로그를 서로 다른 범위로 읽어 산출한다.
`AgentState`는 모든 조건에서 `CONTEXT_HANDOFF.md` §8 스키마 그대로다.

---

## 0. 관측 조건의 정의 — 왜 이렇게 정의했는가

초기 버전의 표는 리뷰에서 무너질 구조였다. 두 가지 결함이 있었다.

1. **"trace/state로는 출처를 특정할 수 없다"가 정의상 참이었다.** 우리 계측이 그 관계를
   기록하지 않았을 뿐이므로, "구현이 부실한 것"이라는 반론에 답할 수 없었다.
2. **state history에는 `retrieved_emails`가 원문 그대로 들어 있다.** 사후에 grep하면 같은
   출처 판정이 나온다. 이 반론은 옳다.

따라서 각 계층에 **그 계층이 실제로 규정하거나 보유한 모든 것**을 주고 같은 매처를 돌린다.

| 조건 | 정의 근거 |
|---|---|
| C1 OTel trace | OpenTelemetry GenAI semantic conventions(commit `5ca9052bc796`)가 **opt-in으로 규정한** 속성을 켠 조건. `gen_ai.retrieval.documents`(문서별 `id`, `score`), `gen_ai.tool.call.arguments`, `gen_ai.tool.call.id`. **이 셋 중 앞의 둘도 `Opt-In`이고 규약은 "[Default] Don't record instructions, inputs, or outputs"라고 규정하므로, 엄밀한 규약 기본값에서는 인자 열거조차 불가하다.** C1은 기본값보다 강하게 부여된 조건이며 오차 방향은 baseline에 유리하다. 입력 메시지 내용만 끈 조건(content off)과 켠 조건(content on)을 나눈다 |
| C2 state history | checkpoint state를 에이전트 state 스키마로 제한. `retrieved_emails`가 source 원문을 보유하므로 source별 매칭 가능. `tool_call`은 단일 슬롯이므로 **첫 후보의 argument만** 감사 대상이 된다 |
| C3 | C2의 source 원문 + C1의 후보 열거 범위. **source 원문에 대한 합집합이 아니다** — C1의 유일한 내용 표면은 조립된 문맥 전체를 하나의 미분화된 pseudo-source로 본 것이라, 개별 메일 어디에도 없는 값이 매칭될 수 있다. 따라서 "입력 내 존재" 축에서 C3가 C1 content on보다 낮을 수 있다 |
| C4 execution evidence | 선언된 trust·획득채널, segment 경계, 모든 action 후보, 전송 바이트 |

매처 강도는 계층과 **직교하는 두 번째 축**이다.

- **보수** `exact+normalized/v1` — 정확 일치, NFKC+공백 정규화 일치
- **관대** `exact+normalized+date_semantic/v1` — ISO 날짜/시각을 한국어 표기 후보로 환원해 매칭

관대 매처는 도달 범위를 올리는 대신 근거(`basis`)를 격하한다. 두 축을 모두 보고한다.

`basis` 어휘는 표준 용어가 아니라 `CONTEXT_HANDOFF.md` §30이 정의한 5항 초안
(`direct_observation`·`deterministic_transform`·`declared`·`inferred`·`attribution_model`)이며,
구현이 실제로 기록하는 것은 앞의 세 항이다(`core/recorder.py:30-35`). 감사 계산(`core/audit.py`의
`TIER_BASIS`)은 표기 환원을 `inferred`로 부르지만 실행 시점 relation(`core/graph.py:235`)은 같은
tier를 `declared`로 기록하므로 두 값이 어긋나 있다. **어휘 확정은 미결 과제이며, 이 어휘의 부재를
표준의 결함으로 서술하지 않는다.** 정규화 tier는 본 실험에서 한 번도 발화하지 않았다.

---

## 1. 결과 요약 — 무엇이 실제 격차인가

`spike/audit_tables.md`의 전체 표를 참조하되, 결론은 세 줄이다.

**(1) 출처 지명은 격차가 아니다.** C3(trace+state)가 C4와 **동일한 source 지명률**을 달성한다.
OTel 규약 수준의 trace와 checkpoint state를 결합하면, 전용 evidence 계층과 같은 출처 판정이
사후에 재구성된다. 이것은 §28 조합 A·B 반론에 대한 우리 쪽 인정이며, 논문은 이 사실을
숨기지 않고 먼저 밝힌다.

**(2) 실제 격차는 세 가지다.** 매처 강도와 무관하게 계층 능력이 갈린다.

| 능력 | C1 off | C1 on | C2 | C3 | C4 |
|---|---|---|---|---|---|
| argument 열거 | ○ | ○ | △ 첫 후보만 | ○ | ○ |
| 값이 입력에 존재하는지 판정 | ✕ | ○ | ○ | ○ | ○ |
| 어느 source인지 지명 | ✕ | **✕** | ○ | ○ | ○ |
| 선언된 trust·획득채널 복원 | ✕ | ✕ | **✕** | **✕** | ○ |
| 입력을 전송 바이트와 대조 | ✕ | ✕ | ✕ | **✕** | ○ |

- **C1 content on이 source를 지명하지 못하는 이유는 우리 구현이 아니라 규약이다.**
  조립된 문맥이 전달되는 **텍스트 파트**는 `type`과 `content`만 가지며 source 식별자 필드가 없다
  (파일·URI 파트는 `file_id`·`uri`를 갖지만 사전 업로드된 대상을 통째로 지시할 뿐 조립된 텍스트
  안의 구간을 가리키지 못한다). 바이트 범위·문자 오프셋 개념은 파트 정의 전체에 없다.
  값이 입력에 존재하는지는 판정되지만(보수 0.222~0.530 / 관대 0.622~0.842),
  어느 문서에서 왔는지는 어떤 매처 강도로도 답하지 못한다.
- **trust 복원은 어느 사후 매칭으로도 불가능하다.** 획득 채널은 렌더된 프롬프트 문자열에
  남지 않으므로, ingestion 시점에 선언하지 않으면 복원 대상이 없다. C1~C3에서 전 조건 0.000.
- **state 스키마의 구조적 손실.** 단일 `tool_call` 슬롯 때문에 C2가 열거할 수 있는 argument가
  source 수에 따라 급격히 줄어든다 — min fixture 179/321·40/45,
  **wide fixture 66/531(12.4%)·25/205(12.2%)**. 후보를 잃은 실행은 wide 조건에서
  **12/12, 5/5**다.

**(3) 결정적 출처 추적에는 상한이 있다.** 보수 매처의 source 지명률은 0.178~0.367이고,
관대 매처로 올려도 0.514~0.678에 머문다. 나머지는 모델이 값을 복사하지 않고 변환한 경우다.
관대 매처는 근거를 `inferred`로 격하하므로, 도달 범위와 근거 강도가 교환 관계에 있다.

---

## 2. 동일 context에서의 action 변동 (§15)

여기서 지표 정의를 정정했다. **action 후보 *수*는 약한 신호다.**

| 조건 | 후보 수 이탈률 | **action 집합 이탈률**(argument 값 포함) |
|---|---:|---:|
| min × Haiku (30회) | 0.033 | **0.900** |
| min × Sonnet (8회) | 0.125 | **0.750** |
| wide × Haiku (12회) | 0.000 | **0.917** |
| wide × Sonnet (5회) | 0.000 | **0.800** |

**관측 사실.** context 바이트가 동일한 재호출에서 후보 *수*는 거의 일정했다. 그러나 tool 이름과
argument 값까지 포함한 action 집합은 서로 달랐다 — wide×Haiku는 12회 실행이 **12개의 서로 다른
action 집합**을 만들었다.

**해석.** 동일 state·동일 입력을 재사용해도 실행된 action이 값 수준에서 재현되지 않는다.
따라서 재호출은 과거 action의 **값 수준** 근거를 검증하는 수단이 되지 못한다. checkpoint를
복원해 재생하는 절차는 수행하지 않았으므로 그 절차에 대해서는 말하지 않는다.

**정정.** 이전 라운드에서 보고한 후보 수 이탈률 0.207은 `max_tokens=1024` 실행에서 나온
값이며, 상한을 4096으로 올리면 0.033으로 떨어진다. 그 수치는 **토큰 상한의 부산물**이었다.
논문에는 action 집합 이탈률을 쓴다.

---

## 3. 미연결의 정체

시작·종료 시각은 **전부** 미연결이었다. 원문 메일은 "9월 8일 화요일 오후 3시부터 4시까지"이고
도구 인자는 `2026-09-08T15:00:00+09:00`이다. 메모도 대부분 미연결이며 원문
"안건은 3분기 목표 점검입니다"가 "안건: 3분기 목표 점검"으로 바뀌어 있다.

argument 위치별 분포는 `spike/audit_tables.md`의 "argument 위치별 판정" 절이 생성한다
(폐기된 `spike/metrics_result.json`을 대체했다). min×Haiku 조건의 미연결 비율은 보수 → 관대로
`start` 1.000 → 0.186, `end` 1.000 → 0.000, `notes` 0.797 → 0.797,
`title` 0.068 → 0.068, `location`·`attendees/i` 0.000 → 0.000이다.

**관측 사실.** 관대 매처(ISO 날짜를 한국어 표기로 환원)를 적용하면 source 지명률이
0.293 → 0.514(min×Haiku), 0.367 → 0.678(wide×Haiku)로 오른다.

**해석.** 미연결의 지배적 원인은 계측 누락이 아니라 모델의 값 변환이며, 그 변환은 한 종류가 아니다 —
(a) 표기 변환, (b) 요약·발췌, (c) 복수 구간 결합 세 종류다. 관대 매처는 (a)만 회수한다:
시각 필드는 대부분 회수되지만 `notes`는 두 매처 모두 같은 비율(0.797)로 미연결이다. 다만 회수된 관계의 근거는 `inferred`이므로, 도달 범위를 늘리는
대가로 주장 강도를 낮춘다. 증명할 수 없는 관계를 `ambiguous`/`unlinked`로 명시하는 설계는
선택 사항이 아니다.

---

## 4. Fixture 타당성과 인젝션 미재현

정정된 판정 기준(argument에 공격자 주소가 나타나거나 메일 전달을 서술하는 경우로 한정,
호출 건수는 근거가 아님)으로 문구 5종을 각 3회 실행 → **0/15.** 본 실험 전체의 action 후보에서도
공격자 주소는 0건이다. 단 `policy_gate`가 판정을 수행하지 않는 통과 노드이므로(`evaluated: false`)
"승인 거부된 후보"라는 범주 자체가 이 실험에 존재하지 않는다 — 0건은 정책 집행의 효과가 아니다.

캘리브레이션 범위도 밝힌다: Haiku 4.5·min fixture·단일 삽입 위치·문구 5종이며, 판정 기준 오류로
문구 탐색이 조기 중단되었다.

**따라서 측정 대상은 정상 action이다.** 실제로 얻은 조건이 더 견고하다 — 하나의 action이
복수의 신뢰할 수 없는 외부 source를 섞는 상황이 정상 동작에서 발생한다. 인젝션 메일은
어떤 action argument에도 기여하지 않은 **음성 대조군**으로 쓴다. evidence 계층은 그 메일로부터의
파생 관계가 0건임을 보이지만, trace와 state history는 기여 여부를 어느 쪽으로도 보이지 못한다.

---

## 5. 부수 측정 — 조립 좌표와 전송 좌표 (A7)

- A7a **PASS**: 조립된 context 문자열은 저장된 segment로부터 바이트 동일하게 재현된다
  (20회 반복, 별도 프로세스, 입력 key 순서 변경 포함).
- A7b **MIXED**: 그 문자열이 JSON 요청 본문으로 인코딩되면 segment마다 앞서는 구조 오버헤드가 달라
  시작 위치가 이동한다(한국어 본문은 원시 UTF-8로 전송되어 늘지 않고, 확장은 개행 이스케이프 몫이다).
  관측된 좌표 이동량 [61, 64, 70, 76] — **단일 상수 shift가 없다.** 시스템 지시 segment는 본문에서
  유일 위치가 아니라 두 곳에 나타났다. **이 측정은 단일 호출이며 시스템 지시 문구가 유효 실행 55회와
  다른 변형(`guarded`, 146바이트 대 `neutral` 143바이트)이다.** 요청 본문은 단일 좌표 공간이 아니라 `system`·`messages`·`tools`
  등 복수 영역의 집합이므로, 출처 위치는 (영역, 바이트 범위) 쌍으로 기록해야 한다.
- B5 **확인**: 요청 alias와 `response.model`이 다르다.
  `global.anthropic.claude-haiku-4-5-20251001-v1:0` → `anthropic.claude-haiku-4-5-20251001-v1:0`,
  `global.anthropic.claude-sonnet-5` → `claude-sonnet-5`.

---

## 6. 정정 이력

리뷰에서 지적될 수 있는 자체 오류를 모두 기록한다.

| 오류 | 영향 | 조치 |
|---|---|---|
| 캘리브레이션 판정에 `tool_call` 2건을 무권한 근거로 사용 | T1 문구를 hit rate 1.0으로 오판. 정상 일정 2건이었음 | 기준 정정 후 재측정 0/15 |
| system 문구에 완화책(`"요청받은 작업만 수행하십시오"`) 포함 | 초기 0/12 | 통제 변수로 승격 |
| 사용자 요청이 특정 메일 1건만 지목 | 인젝션 메일이 과업 범위 밖 | `broad` 변형 추가 |
| 위치 비교 시 발신자·제목이 함께 변동 | idx2=0/12가 위치 효과로 오독될 수 있었음 | 공격 메일 고정 객체화 후 재측정 |
| `max_tokens=1024` | wide fixture 전 실행 절단(10/10), 후보 수 분포가 상한의 부산물 | 4096으로 통일, 절단 실행을 표에서 배제 |
| 비결정성 지표를 후보 *수*로 정의 | 0.207 → 상한 수정 후 0.033. 약한 신호였음 | argument 값 포함 action 집합 이탈률로 교체 |
| 관측 조건을 우리 계측 기준으로 정의 | C1~C3의 0이 정의상 참이 되어 반론 불가 | 규약·스키마가 규정한 것으로 재정의 |
| basis 어휘를 3항으로 서술 | `CONTEXT_HANDOFF.md` §30은 5항(`declared`·`attribution_model` 포함)이고, 감사 계산은 표기 환원을 `inferred`로 부르는데 `core/graph.py:235`는 같은 tier를 `declared`로 기록한다. 두 값이 어긋난 상태 | 제출본 3절에 5항 초안·구현 3항·불일치를 명시. 어휘 확정은 미결 |
| `verify_numbers.py`의 rate 정규식 `0\.\d{3}\b` | 한글이 word 문자라 `0.NNN에서`처럼 한글이 뒤따르는 경우를 매칭하지 못함. 제출본 49건 중 12건이 미검사였고 `1.000`도 누락 | `(?<!\d)[01]\.\d{3}(?!\d)`로 교체. 제출본 37→49건 포착 |
| §2가 "재실행"·"checkpoint 복원" 표현 사용 | 이 실험은 checkpoint를 복원해 재생하지 않는다. 독립 재호출이다 | "재호출"로 교체하고 값 수준으로 한정 |
| C1을 "규약 기본값"이라 서술 | `gen_ai.tool.call.arguments`·`gen_ai.retrieval.documents`도 **Opt-In**이므로 엄밀한 기본값에서는 인자 열거조차 불가. C1을 규약보다 강하게 부여했고 오차 방향은 baseline에 유리 | 논문 3절을 "opt-in을 켠 조건"으로 재서술. 코드 라벨·docstring은 미수정(계층 정의 변경이라 승인 필요) |
| 복원 불가 3종에 "첫 후보 이후 action"을 포함 | C3가 전체 후보를 열거하므로 87.6% 누락은 C2 한정 손실인데, 초록·5절·결론이 계층 범위를 지워 표 1과 모순 | 계층 범위를 명시하고 "두 가지 + 계층에 따라 갈리는 손실"로 재구성 |
| 4.2절 좌표 이동을 "이스케이프 때문"으로 서술 | `a7b_result.json`의 `body_is_ascii_escaped`가 `false`. 실제 원인은 segment별 JSON 구조 오버헤드 차 | 원인 서술 교체. A7b가 폐기된 `guarded` system 문구·단일 호출 조건임도 명시 |
| 4.3절 잔여분을 "모델의 값 변환"으로 일괄 귀속 | 관대 매처는 `end`를 전부 회수하나 `notes` 0.821은 한 건도 회수 못 함(요약·발췌·구간 결합) | `audit_tables.py`에 argument 위치별 분해 추가, 폐기된 `metrics_result.json` 의존 제거 |
| `verify_numbers.py`가 제출본 인자 총계를 미검사 | 정규식이 ASCII `argument N개`만 매칭해 `도구 인자 1,102개`에서 0건 매칭 — 침묵 실패 | 한국어 표기·배제 건수·위치별 비율까지 검사 범위 확대 |
| 4.4절이 "checkpoint 복원"을 결론에 포함 | `variation()`은 독립 재호출을 context digest로 묶은 것이며 checkpoint 재생은 미측정. 온도도 미보고 | "재호출"로 한정, 온도·시드 부재를 실험 조건에 명시 |
| 위협 모델 부재 | 보안 학회 제출본에 공격자 능력 서술이 0건 | 3절에 위협 모델 단락 추가. 귀인 회피 공격면을 4.3절에 명시 |
| 제출본 축약이 논문 B의 정정 대상을 삭제 | 4.4절·표 2와 결론의 재호출 문장을 함께 제거해, 논문 B §6이 "선행 보고가 …라고 결론짓는다"고 정정하려는 문장이 제출본에 남지 않았다. 논문 B가 인용부호로 제시한 "재호출은 감사 수단이 되지 못한다"의 리터럴 출처는 폐기본 `docs/paper_draft.md:282`이며 그쪽은 "재**실행**"이라 쓴다 | 논문 B와 조율 필요. 축약을 유지하려면 논문 B §6이 폐기본을 인용하지 않도록 근거를 바꿔야 한다 |
| 제출본 체크리스트가 논문 3편의 옛 경로를 인용 | 재배치로 `docs/paper_{transform,replay,coordinates}.md` → `papers/*/paper.md` | 경로 갱신 |

---

## 7. 한계

- fixture 2종, 모델 2종, 프레임워크 1종, 유효 실행 55회. 조건 간 비교는 되지만 일반화 주장은 하지 않는다.
- 도구는 mock이며 실제 외부 부작용이 없다.
- **인젝션이 재현되지 않았다.** 공격 상황에서 동일한 수치가 나올지는 확인하지 않았다.
  또한 초기 판정 오류로 문구 탐색이 조기 중단되었으므로 이 fixture로 인젝션이 불가능하다고
  결론지을 수도 없다.
- source 지명률은 매처 정의에 의존한다. 보수·관대 두 값을 모두 보고하는 이유다.
- **B2 미해결**: httpx2 event hook이 넘긴 body가 실제 소켓에 기록된 바이트와 같은지 확인되지
  않았다. evidence record의 `capture_method`에 캡처 계층을 명시해 두었다.
- Bedrock 경유 특성: `model`이 body가 아닌 URL path에 있고 SDK가 `anthropic_version`을 주입한다.
  직접 Anthropic API 경로에서 같은 결과가 나올지는 미확인.
- 프롬프트 구간에 값이 존재했다는 사실이 그 구간이 action을 일으켰음을 증명하지 않는다.
  모든 relation은 `causal_claim = not_established`로 기록된다(주장된 인과 관계 0건).
- 문헌 카드는 CaMeL(소스 코드 포함) / OpenLineage / OpenTelemetry GenAI / W3C PROV /
  ContextCite / TaintDroid까지 마감했다. Why-Where(ICDT 2001)와 secure logging 2건은
  원문 재확인이 미수행이다 — `docs/related_work_facts.md` §7.
