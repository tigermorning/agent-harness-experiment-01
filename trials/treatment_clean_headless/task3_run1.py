class LoanwordApiError(Exception):
    """call_loanword_api 조회 실패(비-200 응답, 예상치 못한 JSON 형식 등)를 나타낸다."""


def get_standard_notation(word: str) -> str | None:
    """외래어 표준 표기를 조회한다.

    반환값:
        str: 표준 표기가 등재되어 있는 경우.
        None: 조회는 성공했지만 등재된 표기가 없는 경우 (notation == null).

    예외:
        LoanwordApiError: 조회 자체가 실패한 경우
            (예: 인증 헤더 누락으로 인한 403, 서버 5xx 장애,
            응답 JSON에 "notation" 키가 없는 등 형식 오류).
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordApiError(
            f"외래어 표기 조회 실패: word={word!r}, status_code={response.status_code}"
        )

    try:
        body = response.json()
        notation = body["notation"]
    except (ValueError, KeyError) as exc:
        raise LoanwordApiError(
            f"외래어 표기 조회 응답 형식 오류: word={word!r}"
        ) from exc

    return notation
