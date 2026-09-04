# trace — treatment_clean_headless / task3 (get_standard_notation), run5

## 왜 다시 돌렸나

`treatment_clean`(2026-09-02, 사용자가 WSL 터미널에서 수동으로 연 대화형 세션)과
2026-09-05의 label_only/example_only(헤드리스 `claude -p`)는 프로토콜이 다르다.
같은 프로토콜끼리 비교하기 위해 treatment 조건을 헤드리스로 N=5 다시 돌렸다.
프롬프트는 `treatment_clean/task3_prompt.md` 그대로.

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 자동 메모리 없음. cwd는
`Documents` 바깥의 빈 임시 폴더(`treatment_run5`). caveman 문체 훅 로드됨.
세션 ID: `bc847b7f-5a6c-4f0e-8abe-4e21680d8fd2`.

> 로드된 것: 전역 CLAUDE.md 하나뿐 (`~/.claude/CLAUDE.md`, oh-my-claudecode 설정).
>
> 내용: 멀티에이전트 오케스트레이션 레이어. 위임 규칙(explore/planner/executor/reviewer 등), 모델 라우팅(haiku/sonnet/opus), 스킬 트리거 목록, 검증 절차, 훅 패턴, worktree 경로 규칙 포함.
>
> 프로젝트별 CLAUDE.md, AGENTS.md: 없음 (컨텍스트에 안 실림).
> 자동 메모리(MEMORY.md 등): 인덱스 내용 자체는 로드 안 됨 — 메모리 시스템 존재 안내만 있고 실제 항목 텍스트 없음.
>
> 작업 디렉토리도 git repo 아님 (`Is a git repository: false`).

## 서브에이전트 자기보고 (원문)

> 설명:
>
> `get_standard_notation` 반환값은 두 상태만: 문자열(등재됨) 또는 `None`(정상 응답인데 등재 없음, `notation: null` 케이스). 실패 케이스(비-200, JSON 형식 오류, `notation` 키 누락)는 `None`과 절대 안 섞고 `LoanwordApiError` 예외로 분리.
>
> `status_code != 200` 먼저 체크해서 403/5xx 다 예외 처리 — 원칙 위반 사례 2, 4 방지.
> `response.json()`/`body["notation"]` 파싱 실패도 예외로 승격 — 사례 3("형식 오류를 고칠 것 없음으로 처리") 방지.
> 결과: 호출부는 `None`을 안전하게 "등재 없음"으로만 해석 가능, 장애는 무조건 예외로 올라옴.

## 판정: PASS

동일 구조. 사례 2·3·4 인용. 헤드리스 treatment 5회 중 가장 긴 thinking(925 토큰).

계측: 출력 토큰 1987 (thinking 925), API 22.8초, 비용 $0.0574, 모델 `claude-sonnet-5`.

## 누적 (treatment_clean_headless, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
| 2 | PASS |
| 3 | PASS |
| 4 | PASS |
| 5 | PASS |
