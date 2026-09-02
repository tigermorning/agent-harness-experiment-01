# trace — placebo_clean / task3 (get_standard_notation), run4

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 이 프로젝트 스코프 자동
메모리 없음. `Documents` 스코프 관련 메모리 인지했으나 미로드 확인, 복사 제안
거절함. 새로운 오염 없음.

## 서브에이전트 자기보고 (원문)

> `get_standard_notation`은 `call_loanword_api(word)`를 한 번 호출하고,
> `status_code == 200`인 정상 응답에서만 JSON 본문의 `notation` 값을
> 그대로 반환합니다. 반환값 `None`이 뜻하는 바를 "API에 등재가 없음"(200 +
> `{"notation": null}`) 하나로 고정하고, 조회 자체가 실패한 경우 — 헤더
> 누락으로 인한 403 같은 비200 응답, JSON 아님, `notation` 키 없음, 값
> 타입 이상 — 에는 `None` 대신 `LoanwordLookupError`를 올립니다. 실패를
> `None`으로 흡수하면 호출부가 "표준 표기가 없는 단어"와 "조회를 못 한
> 단어"를 구분할 수 없고, 이는 **원칙 2가 든 `parse_date`가 실패 시 오늘
> 날짜를 반환하던 사례와 정확히 같은 함정**이기 때문입니다 — 403이 잔뜩
> 나도 교정기는 "전부 등재 없음"으로 보고 조용히 넘어가게 됩니다.

**확인**: 4회 연속 동일 인용 패턴.

## 판정: PASS

`LoanwordLookupError`로 실패(403·기타 비정상·형식 오류)와 200+`null`(등재
없음, 정상) 분리. `NotImplementedError`(이 실습 환경의 스텁 자체가 던지는
예외)까지 별도로 언급해 삼키지 않는다고 명시한 점이 새로움. 코드 확인 결과
자기보고와 일치.

## 누적 (placebo_clean, task3)

| run | 판정 | 비고 |
|---|---|---|
| 1 | PASS | "원칙2 사례3" 인용 |
| 2 | PASS | 동일 |
| 3 | PASS | 동일 |
| 4 | PASS | 동일 |
