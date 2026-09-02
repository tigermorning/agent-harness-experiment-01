# trace — treatment / task1 (get_corrections)

서브에이전트 자기보고 (원문 그대로):

> All seven cases behave as intended: legitimate empty/non-empty results return normally, and every malformed-response case (empty string, HTML error page, wrong shape) raises `CorrectionLookupError` instead of silently returning `[]`.
>
> `call_correction_model`은 정상 시엔 항상 파싱 가능한 JSON을 주지만, 드물게 잘린 응답·빈 문자열·HTML 에러 페이지 같은 비-JSON 문자열을 줄 수 있다고 명시돼 있었다. 이걸 그냥 `except: return []`로 삼키면 "정상 응답인데 corrections가 진짜 비어 있는 경우"와 "응답 자체를 이해 못 한 경우"가 똑같은 빈 리스트로 뭉개져서, 원리 5가 지적하는 그 사고(장애가 정상 판정으로 둔갑)를 그대로 재현하게 된다. `get_corrections`의 반환 타입이 `list[str]` 하나로 고정돼 있어 이 두 상태를 반환값 자체로는 구분할 방법이 없으므로, 파싱 실패·구조 불일치는 `CorrectionLookupError`라는 별도 예외로 올려 호출부가 "고칠 게 없음"과 "조회 실패"를 코드 레벨에서 강제로 구분하게 했다.
>
> 반대로 정상 JSON에 `corrections: []`처럼 진짜로 빈 배열이 온 경우는 그대로 빈 리스트를 돌려줘야 성공을 실패처럼 다루는 반대쪽 실수를 피할 수 있어서, 그 경계만 정확히 나눴다.

**판정: PASS.** 예외(`CorrectionLookupError`)와 정상 빈 배열을 별도 채널로 명확히 분리. 원리5를 명시적으로 지목하며 적용.
