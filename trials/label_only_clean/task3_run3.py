HTTP_STATUS_OK = 200


def get_standard_notation(word: str) -> str | None:
    """외래어 표준 표기를 조회한다. 정상 응답이 아니면 None을 반환한다."""
    response = call_loanword_api(word)

    if response.status_code != HTTP_STATUS_OK:
        return None

    return response.json().get("notation")
