HTTP_STATUS_OK = 200


def get_standard_notation(word: str) -> str | None:
    """word의 외래어 표준 표기를 조회한다. 등재 없거나 실패 시 None."""
    response = call_loanword_api(word)
    if response.status_code == HTTP_STATUS_OK:
        return response.json().get("notation")
    return None
