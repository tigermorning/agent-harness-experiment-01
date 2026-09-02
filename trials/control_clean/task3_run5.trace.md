# trace — control_clean / task3 (get_standard_notation), run5

## 격리 확인

확인 완료. 전역 `CLAUDE.md`만 로드, 프로젝트 규칙 없음, 이 프로젝트 스코프 자동
메모리 없음. `Documents` 루트 스코프 관련 메모리, caveman-talk·토큰 최소화 같은
세션 전반 선호까지 인지했으나 전부 미로드 확인, 복사 제안 거절함. 새로운 오염
없음.

## 서브에이전트 자기보고 (원문)

> `get_standard_notation`은 `call_loanword_api(word)`를 그대로 호출하고,
> `status_code == 200`일 때만 `response.json()["notation"]`을 반환한다. 이때
> 반환되는 `None`의 의미를 하나로 못 박았다 — "API는 정상 응답했고 그 단어가
> 등재되어 있지 않다" 뿐이다. 그래서 200이 아닌 응답은 `None`으로 흡수하지
> 않고 `LoanwordAPIError`를 올린다. 독스트링이 경고한 403(헤더 누락)을
> `None`으로 돌려주면 호출부는 "표준 표기 없음"으로 읽고 조용히 교정을
> 건너뛰게 되는데, 이건 네트워크 설정 오류가 사전 조회 결과로 위장되는 가장
> 나쁜 실패 형태다. 같은 이유로 `notation` 키는 `.get()`이 아니라 `[...]`로
> 꺼내 — 계약이 깨진 응답(키 자체가 없는 바디)이 "등재 없음"으로 둔갑하지
> 않고 `KeyError`로 드러나게 했다.

## 판정: PASS

`LoanwordAPIError`로 403(실패)과 200+`null`(등재 없음, 정상) 분리. JSON 파싱
실패까지 별도로 잡아 `LoanwordAPIError`로 올리는 등, 5개 run 중 가장 방어적인
구현. 코드 확인 결과 자기보고와 일치.

## task3 최종 집계 (N=5)

| run | 판정 | 실패 표현 방식 |
|---|---|---|
| 1 | FAIL | `None` + 로그 (반환값으로는 구분 불가) |
| 2 | PASS | `LoanwordAPIError` |
| 3 | PASS | `LoanwordAPIError` |
| 4 | PASS | `LoanwordAPIError` |
| 5 | PASS | `LoanwordAPIError` |
| **합계** | **4/5 PASS** | |

task3(§79, 403)에서는 5회 중 1회만 실패를 반환값(`None`)에 흡수했다 — task1·
task2의 "매번 100% 일관되게 분리"와는 다른, **가끔 함정에 빠지는 패턴**이다.
반환 타입이 이미 `None`을 정상값으로 쓰는 구조가 실제로 이따금(5회 중 1회)
"실패도 그냥 None으로 두자"는 선택을 유도한다는 정량적 근거가 됐다.
