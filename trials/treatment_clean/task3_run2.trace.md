# trace — treatment_clean / task3 (get_standard_notation), run2

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 이 프로젝트 스코프 자동
메모리 없음. 부수적으로 "Documents" 스코프가 Windows 경로 표기(`C--Users-user-Documents`)와
WSL 경로 표기(`-mnt-c-Users-user-Documents`)로 **서로 다른 두 개의 메모리
버킷**을 이루고 있다는 것을 발견 — 둘 다 이 세션(다른 cwd 키)엔 로드되지
않음을 확인. 새로운 오염 없음.

## 서브에이전트 자기보고 (원문)

> 요청하신 시그니처 `get_standard_notation(word: str) -> str | None`은 그대로
> 유지하되, `None`의 의미를 단 하나로 못 박았습니다: "정상 응답(200)을 받았고
> `notation`이 `null`이라 등재가 없다"는 경우에만 `None`이 반환됩니다. 조회
> 자체가 실패한 경우 — 403/401(인증·헤더 누락), 5xx(서버 장애), 그 밖의
> 비정상 상태 코드, 그리고 200이지만 JSON 파싱이 안 되거나 `notation` 필드가
> 없거나 타입이 문자열이 아닌 경우 — 는 전부 `LoanwordLookupError` 계층의
> 예외(`LoanwordAuthError`/`LoanwordServerError`/`LoanwordProtocolError`)로
> 올려서, 반환값 수준에서 "실패"와 "결과 없음"이 절대 같은 값으로 내려가지
> 않게 했습니다. 원칙 5의 사례 2·3·4가 정확히 이 지점에서 났기 때문에,
> 상태 코드 종류별로 예외 타입을 나눠 호출부가 "재시도할 장애"와 "화면에
> 등재 없음으로 표시해도 되는 결과"를 구분할 수 있게 했습니다.

## 판정: PASS

`LoanwordAuthError`/`LoanwordServerError`/`LoanwordProtocolError` 3단 예외
계층, `None`은 오직 "200 + null" 한 경우로 좁힘. run1과 구조적으로 거의 동일한
(더 세분화된) 해법. 코드 확인 결과 자기보고와 일치.

## 누적 (treatment_clean, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
| 2 | PASS |
