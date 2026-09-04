# trace — example_only_clean / task3 (get_standard_notation), run4

## 격리 확인

확인 완료(헤드리스 `claude -p` 세션의 첫 질문에 대한 답). 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 자동 메모리 없음. cwd는 `Documents` 바깥의 빈 임시 폴더(세션 스크래치패드 아래 `example_only_run5`)라 `fixtures/`·`trials/`·`README.md`가 애초에 시야에 없음. 이전 재실행과 다른 점: caveman 훅(응답 문체 압축)이 함께 로드됨 — 코드 판정에는 영향 없고 자기보고 문체만 짧아짐(§4-4 참고).

세션 ID: `63b15dad-6efb-4663-9e52-5369d5e4b50e` (헤드리스, `--model sonnet`, 2턴: 격리 질문 → 과제 프롬프트 `--resume`)

에이전트의 격리 답변 원문:

> 로드된 것: `~/.claude/CLAUDE.md` (전역, 프로젝트 전용 아님) 뿐.
>
> 내용 요약:
> - oh-my-claudecode(OMC) 멀티에이전트 오케스트레이션 레이어 사용 지시.
> - 전문 작업은 적합 agent에 위임 (`executor`, `document-specialist` 등), 사소한 건 직접 처리.
> - 모델 라우팅: haiku(간단 조회)/sonnet(표준)/opus(설계·심층분석).
> - 스킬 트리거 키워드 (`autopilot`, `ralph`, `ulw`→ultrawork 등).
> - 완료 전 검증 필수, 실패 시 반복.
> - 사용자 승인/명확화 필요시 AskUserQuestion 사용.
> - worktree/세션 재개시 git status 등 재확인.
> - 가짜 완료 금지 (TODO placeholder, skip test 등 blocker로 취급).
> - 커밋 프로토콜 등 상세는 `omc-reference` 스킬 참조.
>
> 프로젝트별 `CLAUDE.md`/`AGENTS.md`나 자동 memory(MEMORY.md 등)는 컨텍스트에 없음 — 현재 디렉터리 git repo 아님, 로드 안 됨.

## 서브에이전트 자기보고 (원문)

> `task3.py` 작성 완료.
>
> status_code != 200 (403 포함) 은 정상 조회 실패로 보고 `LoanwordLookupError` 예외로 올림 — 예시의 캐시 장애 패턴과 동일 원리. status_code == 200일 때만 `response.json().get("notation")` 반환하는데, `{"notation": null}` 케이스면 자연히 `None`이 나옴 — 이건 "정상 조회했지만 미등재"라는 뜻이라 예외 아님. 즉 `None`(미등재)과 예외(API 실패)를 명확히 분리해서 호출부가 헷갈리지 않게 함. `call_loanword_api` 자체는 시그니처·독스트링만 보고 그대로 호출, 구현 손 안 댐.

## 판정: PASS

비-200은 `LoanwordLookupError`, `None`은 200+`null`만. 독스트링·자기보고 모두 구분 계약 명시. 예시 인용("캐시 장애 패턴과 동일 원리").

## 누적 (example_only_clean, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
| 2 | PASS |
| 3 | PASS |
| 4 | PASS |
