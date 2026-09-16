"""manager/*.md 를 읽는 순서대로 이어붙여 rendered/_all.md 를 만든다."""
import re, pathlib
ROOT = pathlib.Path(__file__).parent
ORDER = [("00_note.md","말하기 노트"),("02_structure.md","기본 구조와 개념"),
         ("05_ai_lifecycle.md","AI Lifecycle"),("06_ai_responsibility.md","AI Responsibility"),
         ("07_system_architecture.md","AI System 구조"),("08_ai_rmf_profile.md","AI RMF Profile"),
         ("09_ai_grc_review_scope_v0.2.md","내 검토 범위 (v0.2)"),
         ("04_adoption_gate.md","도입 심사 게이트"),("03_demo.md","데모 시나리오")]
FIG = {"05_ai_lifecycle.md":"lifecycle","06_ai_responsibility.md":"responsibility",
       "07_system_architecture.md":"architecture","08_ai_rmf_profile.md":"rmf_cycle"}
HEAD = """# 거버넌스 매니저 인터뷰 — 전체 자료

**기준선**

    기준 (AI GRC · 내 자리)  →  구현 (Development)  →  판정 (Assurance)  →  수용 (Risk / Business)

| 분리선 | 내용 |
|---|---|
| ① | 만든 사람이 판정하지 않는다 (구현 ↔ Assurance) |
| ② | 판정한 사람이 위험을 수용하지 않는다 (Assurance ↔ 수용) |
| ③ | **기준을 만든 사람이 그 기준으로 판정하지 않는다** (내 자리 ↔ Assurance) |

> **"저는 승인하지 않습니다. 승인이 가능하도록 만듭니다."**

![기준선](../manager/figures/baseline.svg)

---
"""
parts = [HEAD]
for fn, title in ORDER:
    s = (ROOT/"manager"/fn).read_text(encoding="utf-8")
    s = re.sub(r"^# .*$", f"# {title}", s, count=1, flags=re.M)
    if fn in FIG:
        s += f"\n\n---\n\n## 그림\n\n![{title}](../manager/figures/{FIG[fn]}.svg)\n"
    parts += [s, "\n\n---\n\n"]
(ROOT/"rendered"/"_all.md").write_text("\n".join(parts), encoding="utf-8")
print("  _all.md 생성")
