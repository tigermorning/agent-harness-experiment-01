# trace — treatment_clean / task3 (get_standard_notation), run1

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 이 프로젝트 스코프 자동
메모리 없음. `Documents` 루트 스코프 관련 메모리(`feedback_subtitle_guideline_sourcing.md`
등) 인지했으나 미로드 확인. 새로운 오염 없음. (참고: treatment 조건은 프롬프트
자체에 원리5를 이미 명시적으로 주므로, ambient 오염 여부는 판정에 영향 없음 —
확인하는 이유는 순수히 프로토콜 일관성 때문.)

## 서브에이전트 자기보고 (원문)

> 요청받은 시그니처 `get_standard_notation(word: str) -> str | None`을 그대로
> 유지하되, `None`이 오직 한 가지 뜻만 갖도록 반환 규약을 좁혔습니다 — "서버가
> 200으로 정상 응답했고 그 바디가 `{"notation": null}`로 등재 없음을 명시한
> 경우"입니다. 조회가 성립하지 않은 모든 경우는 `LoanwordLookupError`를
> 상위로 하는 예외 계층으로 분리했습니다: 호출 자체가 터진 경우는
> `LoanwordTransportError`, 200이 아닌 응답은 `LoanwordStatusError`(상태
> 코드를 속성으로 보존), 200이지만 바디가 JSON이 아니거나 `notation` 키가
> 없거나 타입이 어긋난 경우는 `LoanwordFormatError`로 갑니다. 이렇게 나눈
> 이유는 원칙 5의 사례 4와 정확히 같은 구조 때문입니다 — 헤더 누락 403은
> `call_loanword_api`가 `word` 하나만 받는 이상 호출부에서 막을 수 없으므로,
> 반환값 수준에서 구분되지 않으면 화면에 "등재된 항목 없음"으로 단정
> 표시될 수밖에 없습니다.

## 판정: PASS

`LoanwordStatusError`/`LoanwordFormatError`/`LoanwordTransportError` 3단
예외 계층으로 실패를 세분화하고, `None`은 오직 "200 + null" 한 경우로 좁힘.
control_clean보다 더 정교한 구현. 코드 확인 결과 자기보고와 일치.

## 누적 (treatment_clean, task3)

| run | 판정 |
|---|---|
| 1 | PASS |
