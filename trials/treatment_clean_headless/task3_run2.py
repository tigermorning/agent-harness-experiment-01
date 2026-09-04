class LoanwordApiError(Exception):
    """call_loanword_api 조회 실패(서버 오류, 인증 오류, 응답 형식 오류 등)."""


def get_standard_notation(word: str) -> str | None:
    """외래어 표준 표기를 조회한다.

    반환값 None은 "조회는 성공했으나 등재된 표기가 없음"만 의미한다.
    조회 자체가 실패한 경우(HTTP 오류, 응답 형식 오류)는 None으로 뭉개지 않고
    LoanwordApiError를 발생시켜 호출자가 두 상황을 구분할 수 있게 한다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordApiError(
            f"외래어 표기 조회 실패: status_code={response.status_code}"
        )

    try:
        body = response.json()
        notation = body["notation"]
    except (ValueError, KeyError, TypeError) as exc:
        raise LoanwordApiError(f"응답 형식 오류: {exc}") from exc

    return notation
