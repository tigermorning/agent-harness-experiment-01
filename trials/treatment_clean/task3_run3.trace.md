# trace — treatment_clean / task3 (get_standard_notation), run3

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 이 프로젝트 스코프 자동
메모리 없음. `Documents` 스코프 관련 메모리 인지했으나 미로드 확인, 복사 제안
거절함. 작업 트리가 비어 있음을 스스로 확인. 새로운 오염 없음.

## 서브에이전트 자기보고 (원문)

> 요청한 시그니처(`get_standard_notation(word: str) -> str | None`)는 그대로
> 유지하되, 원칙 5에 맞춰 `None`의 의미를 "조회 성공 + 등재 없음" 하나로만
> 좁혔다. 조회 자체가 실패한 경우는 반환값이 아니라 예외로 알린다: 200이
> 아닌 응답은 `LoanwordAPIStatusError`(`status_code` 속성 보존 — 403 인증
> 오류와 5xx 장애를 호출부에서 구분할 수 있게), 200이지만 바디를 해석할 수
> 없는 경우(JSON 파싱 실패, `notation` 키 없음, `notation`이 문자열/`null`이
> 아님)는 `LoanwordResponseFormatError`이고, 둘 다 공통 상위
> `LoanwordLookupError`를 상속해서 호출부가 "실패 전반"과 "등재 없음"을 한
> 줄로 갈라낼 수 있다. `call_loanword_api`가 올리는 네트워크 예외는 잡지
> 않고 그대로 전파시켰는데, 삼켜서 `None`으로 바꾸는 순간 사례 1·2와 똑같은
> 뭉개기가 되기 때문이다. 응답 바디 검증을 넣은 이유는 사례 3(형식 오류가
> "고칠 것 없음"으로 처리됨)이 정확히 200 응답 안에서 일어나는 실패라서,
> 상태 코드만 보면 걸러지지 않아서다.

## 판정: PASS

`LoanwordAPIStatusError`/`LoanwordResponseFormatError` 2단 예외 계층,
`None`은 오직 "200 + null" 한 경우로 좁힘. run1·run2와 구조적으로 동일한
해법. 코드 확인 결과 자기보고와 일치.

## 누적 (treatment_clean, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
| 2 | PASS |
| 3 | PASS |
