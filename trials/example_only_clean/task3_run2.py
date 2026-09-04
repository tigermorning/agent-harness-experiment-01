class LoanwordAPIError(Exception):
    """외래어 표기 API 호출이 비정상 응답을 반환했을 때 발생."""


def get_standard_notation(word: str) -> str | None:
    """단어의 표준 외래어 표기를 조회한다.

    반환값 None은 "정상 조회했지만 등재된 표기가 없음"만을 뜻한다.
    API 호출 자체가 실패(예: 403)하면 LoanwordAPIError를 발생시켜
    "등재 없음"과 "조회 실패"를 호출부가 구분할 수 있게 한다.
    """
    response = call_loanword_api(word)
    if response.status_code != 200:
        raise LoanwordAPIError(
            f"외래어 표기 API 호출 실패: status_code={response.status_code}"
        )
    return response.json()["notation"]
