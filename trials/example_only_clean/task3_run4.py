class LoanwordLookupError(Exception):
    """외래어 표기 API 조회 실패(장애/비정상 응답)를 나타낸다."""


def get_standard_notation(word: str) -> str | None:
    """word의 외래어 표준 표기를 조회한다.

    반환값 None은 "정상적으로 조회했지만 등재된 표기가 없음"만을 의미한다.
    API 호출 자체가 실패(403 등 200이 아닌 응답)한 경우는 None이 아니라
    LoanwordLookupError를 발생시켜, 호출부가 "미등재"와 "조회 실패"를
    구분할 수 있게 한다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordLookupError(
            f"외래어 표기 API 호출 실패: status_code={response.status_code}"
        )

    return response.json().get("notation")
