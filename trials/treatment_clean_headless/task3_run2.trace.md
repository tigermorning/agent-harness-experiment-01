# trace — treatment_clean_headless / task3 (get_standard_notation), run2

## 왜 다시 돌렸나

`treatment_clean`(2026-09-02, 사용자가 WSL 터미널에서 수동으로 연 대화형 세션)과
2026-09-05의 label_only/example_only(헤드리스 `claude -p`)는 프로토콜이 다르다.
같은 프로토콜끼리 비교하기 위해 treatment 조건을 헤드리스로 N=5 다시 돌렸다.
프롬프트는 `treatment_clean/task3_prompt.md` 그대로.

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 자동 메모리 없음. cwd는
`Documents` 바깥의 빈 임시 폴더(`treatment_run2`). caveman 문체 훅 로드됨.
세션 ID: `c61c82cc-1837-41a8-8c84-b8af72ed0a28`.

> 로드된 것: 글로벌 `~/.claude/CLAUDE.md` 하나뿐.
>
> 내용 요약: oh-my-claudecode(OMC) 멀티에이전트 오케스트레이션 규칙. 전문 작업은 서브에이전트(executor, explore, planner 등)에 위임, 모델 라우팅(haiku/sonnet/opus), 스킬 트리거 키워드(autopilot/ralph/ultrawork 등), 완료 전 검증 필수, 작성과 리뷰 패스 분리, 훅 패턴(`<system-reminder>`, MAGIC KEYWORD 등), 상태 저장 경로 `.omc/**` 규칙.
>
> 프로젝트별 `CLAUDE.md`, `AGENTS.md`, 자동 메모리(MEMORY.md) — 컨텍스트에 없음. (현재 디렉터리도 git repo 아님.)

## 서브에이전트 자기보고 (원문)

> `task3.py` 작성 끝.
>
> 구현: 반환 타입은 `str | None` 유지하되, None은 "notation 필드 자체가 null"인 정상-빈-결과 케이스에만 씀. status_code != 200(서버 장애, 403 등)이나 JSON 파싱/키 누락 같은 형식 오류는 전부 `LoanwordApiError` 예외로 별도 구분. 이렇게 하면 "조회 실패"와 "조회 성공+결과 없음"이 반환값 수준에서 섞이지 않음 — 원칙 5에서 지적한 4개 사고 패턴(서버 장애, 인증 403, 형식 오류가 전부 "없음"으로 뭉개지는 것) 그대로 재현 안 되게 막음. `call_loanword_api` 자체는 시그니처·독스트링만 그대로 신뢰해서 호출, 수정 안 함.

## 판정: PASS

동일 구조. 독스트링에 구분 계약 명시. 원칙5 사례 4개를 인용.

계측: 출력 토큰 1022 (thinking 166), API 14.5초, 비용 $0.044, 모델 `claude-sonnet-5`.

## 누적 (treatment_clean_headless, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
| 2 | PASS |
