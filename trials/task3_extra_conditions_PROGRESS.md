# task3 추가 재실행 — treatment_clean / placebo_clean, 목표 N=5씩

control_clean의 task3가 4/5(유보)로 나와서, 같은 격리 프로토콜로 treatment·
placebo도 재실행한다. 절차는 control_clean과 동일 — 새 터미널 + 새 `claude`
세션, 오염 확인 질문 먼저, 저장소는 시행 동안 비워 둔 상태(`fixtures/`·
`trials/`·`README.md`를 저장소 밖으로 옮김), 프롬프트는 대화창에서 직접
전달.

## treatment_clean (task3, 원리5를 작업 지시와 같은 자리에 명시)
- [x] run1 — PASS (`task3_run1.py`/`task3_run1.trace.md`)
- [x] run2 — PASS (`task3_run2.py`/`task3_run2.trace.md`)
- [x] run3 — PASS (`task3_run3.py`/`task3_run3.trace.md`)
- [x] run4 — PASS (`task3_run4.py`/`task3_run4.trace.md`)
- [x] run5 — PASS (`task3_run5.py`/`task3_run5.trace.md`) — **treatment_clean 완료: 5/5 PASS**
- [ ] run3
- [ ] run4
- [ ] run5

## placebo_clean (task3, 무관한 원칙 — 함수 이름/독스트링 관례)
- [x] run1 — PASS (`task3_run1.py`/`task3_run1.trace.md`, 흥미로운 점: 네이밍 원칙 사례에서 원리5 논리를 스스로 유추함)
- [x] run2 — PASS (`task3_run2.py`/`task3_run2.trace.md`, run1과 동일하게 "원칙2 사례3"을 근거로 명시 인용)
- [x] run3 — PASS (`task3_run3.py`/`task3_run3.trace.md`, 3회 연속 동일 인용)
- [x] run4 — PASS (`task3_run4.py`/`task3_run4.trace.md`, 4회 연속 동일 인용)
- [x] run5 — PASS (`task3_run5.py`/`task3_run5.trace.md`, 5회 연속 동일 인용) — **placebo_clean 완료: 5/5 PASS**

## 전체 완료 (2026-09-02)

| 조건 | task3 N=5 결과 |
|---|---|
| control_clean | 4/5 PASS |
| placebo_clean | 5/5 PASS (단, 매번 "원칙2 사례3"을 근거로 인용 — placebo 설계 순도 문제) |
| treatment_clean | 5/5 PASS |

다음 단계: README §6·§7 갱신, placebo 설계 결함(사례3이 원리5와 구조 공유)을
한계로 기록.
- [ ] run2
- [ ] run3
- [ ] run4
- [ ] run5

## 참고
- 프롬프트 원문: `trials/treatment_clean/task3_prompt.md`,
  `trials/placebo_clean/task3_prompt.md` (지금은 저장소 밖으로 옮겨진 백업
  위치에 있음 — 시행이 끝나면 다시 이 경로로 복구).
- 비교 대상: `trials/control_clean/task3_run{1..5}.trace.md` (4/5 PASS).
