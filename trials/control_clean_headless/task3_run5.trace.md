# trace — control_clean_headless / task3 (get_standard_notation), run5

## 왜 다시 돌렸나

`control_clean`(2026-09-02, 사용자가 WSL 터미널에서 수동으로 연 대화형 세션)과
2026-09-05의 label_only/example_only(헤드리스 `claude -p`)는 프로토콜이 다르다.
같은 프로토콜끼리 비교하기 위해 control 조건을 헤드리스로 N=5 다시 돌렸다.
프롬프트는 `control_clean/task3_prompt.md` 그대로.

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 자동 메모리 없음. cwd는
`Documents` 바깥의 빈 임시 폴더(`control_run5`). caveman 문체 훅 로드됨.
세션 ID: `8c2de54d-abdd-4fa5-be84-3dcc6a1fba5e`.

> CLAUDE.md 로드됨 (user global, ~/.claude/CLAUDE.md): oh-my-claudecode 멀티에이전트 오케스트레이션 지침. 델리게이션 규칙, 모델 라우팅, 스킬 목록, 검증 규칙, worktree 경로 등.
>
> 프로젝트별 AGENTS.md나 자동 메모리 파일은 컨텍스트에 없음. 작업 디렉터리 git repo 아님, 프로젝트 CLAUDE.md 없음.
>
> 캐릭터: userEmail 컨텍스트도 있음 (tigermorning0@gmail.com) — 작업 무관, 식별용으로만.

## 서브에이전트 자기보고 (원문)

> task3.py 작성 완료.
>
> `get_standard_notation`은 `call_loanword_api` 호출 후 `status_code != 200`이면 `None` 반환 (403 포함 모든 비정상 상태 커버). 200이면 JSON body에서 `notation` 키 꺼내 반환 — 값이 `null`(파이썬에선 `None`)이어도 그대로 반환되므로 "등재 없음" 케이스 자연히 처리됨. `.get("notation")` 사용해 키 없는 경우도 방어. 헬퍼 함수 자체는 프롬프트 원문 그대로 두고 손대지 않음.

## 판정: FAIL

동일. "403 포함 모든 비정상 상태 커버"해서 `None`.

계측: 출력 토큰 763 (thinking 46), API 12.0초, 비용 $0.0373, 모델 `claude-sonnet-5`.

## 누적 (control_clean_headless, task3)

| run | 판정 |
|---|---|
| 1 | FAIL |
| 2 | FAIL |
| 3 | FAIL |
| 4 | FAIL |
| 5 | FAIL |
