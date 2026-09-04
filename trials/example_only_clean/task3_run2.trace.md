# trace — example_only_clean / task3 (get_standard_notation), run2

## 격리 확인

확인 완료(헤드리스 `claude -p` 세션의 첫 질문에 대한 답). 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 자동 메모리 없음. cwd는 `Documents` 바깥의 빈 임시 폴더(세션 스크래치패드 아래 `example_only_run3`)라 `fixtures/`·`trials/`·`README.md`가 애초에 시야에 없음. 이전 재실행과 다른 점: caveman 훅(응답 문체 압축)이 함께 로드됨 — 코드 판정에는 영향 없고 자기보고 문체만 짧아짐(§4-4 참고).

세션 ID: `3d030d00-0134-4381-83d1-ac46731b3d59` (헤드리스, `--model sonnet`, 2턴: 격리 질문 → 과제 프롬프트 `--resume`)

에이전트의 격리 답변 원문:

> Loaded 컨텍스트, 새로 검색 안 함:
>
> **CLAUDE.md (전역, ~/.claude/CLAUDE.md)** — oh-my-claudecode(OMC) 멀티에이전트 오케스트레이션 지침. 위임 규칙, 모델 라우팅, 스킬 목록, 검증 절차, 훅 패턴, 취소 명령, worktree 경로 등.
>
> **AGENTS.md** — 로드 안 됨.
>
> **자동 메모리(memory 디렉토리)** — MEMORY.md 인덱스나 개별 메모리 파일 로드 안 됨. 컨텍스트에 없음.
>
> **추가 시스템 리마인더:**
> - userEmail: tigermorning0@gmail.com (attribution용)
> - CAVEMAN MODE ultra 활성 (SessionStart hook)
> - 프로젝트: git repo 아님, Windows 11, PowerShell/Bash 둘 다 사용 가능
> - 이용 가능 스킬 목록, 에이전트 카탈로그, deferred tools 목록
>
> 프로젝트별 CLAUDE.md/AGENTS.md는 컨텍스트에 안 보임 — 이 디렉토리(scratchpad run)엔 없는 듯.

## 서브에이전트 자기보고 (원문)

> task3.py 작성 완료.
>
> 설명: `call_loanword_api` 호출해 `status_code == 200` 아니면 `LoanwordAPIError` 예외 던짐 — 403 같은 실패를 `None`으로 뭉개지 않게. 200이면 JSON `notation` 값 그대로 반환, 이때 `None`은 "정상 조회했지만 등재 없음"만 뜻함. 예시 스니펫과 같은 원칙: 정상적 부재(None)와 장애(예외) 구분. `notation` 키는 항상 존재한다는 독스트링 전제라 `.get()` 대신 `[...]` 사용, KeyError 나면 API 계약 위반이라 그대로 터지는 게 맞음.

## 판정: PASS

비-200은 `LoanwordAPIError`, 200이면 `["notation"]`. 독스트링에 "None은 정상 조회했지만 등재 없음만 뜻한다"를 계약으로 명시. `.get` 대신 `[]`를 써 키 누락도 조용히 `None`이 되지 않게 함(control_clean run2와 같은 선택). 예시 스니펫 인용.

## 누적 (example_only_clean, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
| 2 | PASS |
