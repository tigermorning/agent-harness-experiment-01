class LoanwordApiError(Exception):
    """call_loanword_api 호출이 실패했을 때(예: 403 등 비정상 응답) 발생시키는 예외."""


def get_standard_notation(word: str) -> str | None:
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordApiError(
            f"외래어 표기 API 호출 실패: status_code={response.status_code}"
        )

    return response.json().get("notation")
