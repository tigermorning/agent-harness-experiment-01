# control_clean 진행 상황 — 목표 N=5/과제

각 run은 반드시 **새 터미널 + 새 `claude` 세션**으로 시작한다. 순서:
1. `wsl bash -lc "cd /mnt/c/Users/user/Documents/agent-harness-experiment-01 && pwd && claude"`
2. 오염 확인 질문 먼저: "지금 너한테 자동으로 로드된 프로젝트별 규칙이나 문서가 있어?
   자동 메모리에 korean-subtitle-corrector 관련 항목도 있는지 같이 알려줘."
3. 문제없으면 해당 `taskN_prompt.md` 내용을 열어서 복사 → 그대로 붙여넣기
4. 응답(자기보고 포함) 받으면 대화창에 그대로 붙여넣기 — 파일 정리·판정은 이쪽에서 처리

## task1 (get_corrections, §78)
- [x] run1 — PASS (`task1_run1.py`/`task1_run1.trace.md`)
- [x] run2 — PASS (`task1_run2.py`/`task1_run2.trace.md`)
- [x] run3 — PASS (`task1_run3.py`/`task1_run3.trace.md`)
- [x] run4 — PASS (`task1_run4.py`/`task1_run4.trace.md`)
- [x] run5 — PASS (`task1_run5.py`/`task1_run5.trace.md`) — **task1 완료: 5/5 PASS**

## task2 (find_dialect_matches, search_dialect 동형)
- [x] run1(1차 시도, 폐기 — `task2_contaminated_attempt1.*`, 사유: 이전 시행 파일 자발적 탐색)
- [x] run1(2차 시도, 유효) — PASS (`task2_run1.py`/`task2_run1.trace.md`)
- [x] run2 — PASS (`task2_run2.py`/`task2_run2.trace.md`)
- [x] run3 — PASS (`task2_run3.py`/`task2_run3.trace.md`, 자기보고 유실 — 코드만으로 판정)
- [x] run4 — PASS (`task2_run4.py`/`task2_run4.trace.md`)
- [x] run5(1차 시도, 폐기 — `task2_contaminated_attempt2_readme_leak.*`, 사유: 오염 확인 단계에서 README.md 직접 읽음)
- [x] run5(재시도, 유효) — PASS (`task2_run5.py`/`task2_run5.trace.md`) — **task2 완료: 5/5 PASS**

## 중요: 이제 `fixtures/`와 `trials/`가 저장소 밖(`Documents/_experiment01_backup_during_trials/`)으로 옮겨졌다

남은 시행 동안 `agent-harness-experiment-01/`에는 `.git`·`.omc`·`.gitignore`만
있다. 프롬프트는 파일 경로 대신 대화창에서 직접 복사해서 쓸 것 — 저장소를
비워 뒀어도 사람이 실수로 다시 파일을 넣지 않도록 주의.

## task3 (get_standard_notation, §79)
- [x] run1 — FAIL (`task3_run1.py`/`task3_run1.trace.md`)
- [x] run2 — PASS (`task3_run2.py`/`task3_run2.trace.md`)
- [x] run3 — PASS (`task3_run3.py`/`task3_run3.trace.md`)
- [x] run4 — PASS (`task3_run4.py`/`task3_run4.trace.md`)
- [x] run5 — PASS (`task3_run5.py`/`task3_run5.trace.md`) — **task3 완료: 4/5 PASS**

## 전체 데이터 수집 완료 (2026-09-02)

| 과제 | N=5 결과 | 기존 오염 control (N=1, 참고용) |
|---|---|---|
| task1 (§78) | 5/5 PASS | FAIL |
| task2 (search_dialect 동형) | 5/5 PASS | FAIL |
| task3 (§79) | 4/5 PASS | PASS |

다음 단계: 저장소 원상복구(`fixtures/`·`trials/`·`README.md` 되돌리기) 후
README.md §4·§5·§6·§7·§8 갱신.
- [ ] run3
- [ ] run4
- [ ] run5

## 진행 순서

과제 하나를 N=5까지 채우고 다음 과제로 넘어간다 (task1 run2~5 → task2 run2~5 →
task3 run2~5). 지금은 **task1 run2**부터 시작.
