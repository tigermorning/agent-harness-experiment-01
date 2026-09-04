HTTP_STATUS_OK = 200


def get_standard_notation(word: str) -> str | None:
    """word의 외래어 표준 표기를 조회한다.

    call_loanword_api를 호출해 정상 응답(status_code == HTTP_STATUS_OK)이면
    JSON 바디의 "notation" 값을 반환한다. 등재가 없으면 notation은 None이다.
    """
    response = call_loanword_api(word)
    if response.status_code != HTTP_STATUS_OK:
        return None
    return response.json()["notation"]
