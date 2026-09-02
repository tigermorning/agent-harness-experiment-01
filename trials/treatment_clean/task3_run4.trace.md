# trace — treatment_clean / task3 (get_standard_notation), run4

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 이 프로젝트 스코프 자동
메모리 없음. `Documents` 스코프 관련 메모리 인지했으나 미로드 확인, 복사 제안
거절함. 새로운 오염 없음.

## 서브에이전트 자기보고 (원문)

> 요청받은 시그니처 `get_standard_notation(word) -> str | None`을 그대로
> 유지하되, `None`이 뜻하는 바를 한 가지로 못 박았다: "서버가 200으로 정상
> 응답했고 그 단어는 등재돼 있지 않다"(`{"notation": null}`)는 확정된
> 사실일 때만 `None`이 나온다. 조회 자체가 실패한 경우 — 403(헤더/인증
> 누락), 그 밖의 비정상 상태 코드, JSON 파싱 실패, `notation` 키가 없거나
> 문자열도 `null`도 아닌 응답, 호출 단계의 네트워크 오류 — 는 전부
> `LoanwordLookupError` 하위 예외로 나가게 했다. 원칙 5가 지적한 네 건의
> 장애가 전부 "실패를 정상 반환값에 섞어 넣은" 설계에서 나왔고, 특히
> 4번(403을 "등재된 항목 없음"으로 단정 표시)은 이 API가 헤더 누락 시 403을
> 준다는 독스트링과 정확히 겹치는 시나리오라서, 그 경로만은
> `LoanwordAuthError`로 따로 떼어 호출부가 상태 코드까지 보고 처리할 수
> 있게 했다.

## 판정: PASS

`LoanwordTransportError`/`LoanwordAuthError`/`LoanwordHTTPError`/
`LoanwordResponseFormatError` 4단 예외 계층, `None`은 오직 "200 + null" 한
경우로 좁힘. 지금까지 중 가장 세분화된 구현. 코드 확인 결과 자기보고와 일치.

## 누적 (treatment_clean, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
| 2 | PASS |
| 3 | PASS |
| 4 | PASS |
