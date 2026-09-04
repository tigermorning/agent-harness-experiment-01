# trace — control_clean_headless / task3 (get_standard_notation), run4

## 왜 다시 돌렸나

`control_clean`(2026-09-02, 사용자가 WSL 터미널에서 수동으로 연 대화형 세션)과
2026-09-05의 label_only/example_only(헤드리스 `claude -p`)는 프로토콜이 다르다.
같은 프로토콜끼리 비교하기 위해 control 조건을 헤드리스로 N=5 다시 돌렸다.
프롬프트는 `control_clean/task3_prompt.md` 그대로.

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 자동 메모리 없음. cwd는
`Documents` 바깥의 빈 임시 폴더(`control_run4`). caveman 문체 훅 로드됨.
세션 ID: `9b0cd7c4-e7b0-402f-8ea6-f6dc3cf7e9a0`.

> Git repo 아님, 프로젝트 CLAUDE.md/AGENTS.md 없음.
>
> 로드된 것:
> - `C:\Users\user\.claude\CLAUDE.md` — OMC(oh-my-claudecode) 멀티에이전트 오케스트레이션 규칙. 위임 규칙, 모델 라우팅, 스킬 목록, 검증 프로토콜, 훅 패턴 등.
> - 자동 메모리: 없음 (MEMORY.md 인덱스 로드 안 됨 — 이번 세션 컨텍스트엔 없다)
> - caveman 모드 훅 (SessionStart + UserPromptSubmit) — ultra 레벨 활성, 관사/필러 생략 지시.
> - userEmail 컨텍스트 — tigermorning0@gmail.com, attribution용.

## 서브에이전트 자기보고 (원문)

> call_loanword_api(word) 호출, status_code 200 아니면 None 리턴 — 403 등 헤더 없는 에러 케이스 포함. 200이면 response.json()으로 파싱, `.get("notation")` 반환 — 키 없거나 값이 null이어도 None 자연스럽게 나옴. dict 접근 대신 get 쓴 이유: notation 키 자체가 없는 경우 방어. 헬퍼 함수 자체는 시그니처·독스트링 그대로 두고 손 안 댐.

## 판정: FAIL

동일. "403 등 헤더 없는 에러 케이스 포함" None 반환이라고 스스로 명시.

계측: 출력 토큰 729 (thinking 41), API 8.7초, 비용 $0.0372, 모델 `claude-sonnet-5`.

## 누적 (control_clean_headless, task3)

| run | 판정 |
|---|---|
| 1 | FAIL |
| 2 | FAIL |
| 3 | FAIL |
| 4 | FAIL |
