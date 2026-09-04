class LoanwordApiError(Exception):
    """외래어 표기 API 호출이 실패했을 때 발생하는 예외."""


def get_standard_notation(word: str) -> str | None:
    """word의 표준 외래어 표기를 조회한다.

    반환값 None은 "API가 정상 응답했지만 등재된 표기가 없음"만을 뜻한다.
    API 호출 자체가 실패한 경우(예: 헤더 누락으로 인한 403 등 비정상
    status_code)는 None을 반환하지 않고 LoanwordApiError를 발생시켜,
    호출부가 "등재 없음"과 "조회 실패"를 구분할 수 있게 한다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordApiError(
            f"외래어 표기 API 호출 실패: status_code={response.status_code}"
        )

    return response.json().get("notation")
