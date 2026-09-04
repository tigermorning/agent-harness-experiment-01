class LoanwordApiError(Exception):
    """외래어 표기 API 조회 실패(서버 장애, 인증 오류 등)를 나타낸다."""


def get_standard_notation(word: str) -> str | None:
    """단어의 표준 외래어 표기를 조회한다.

    반환값 None은 "조회는 성공했지만 등재된 표기가 없음"만 의미한다.
    조회 자체가 실패한 경우(인증 오류, 서버 장애, 응답 형식 오류)는
    None으로 뭉개지 않고 LoanwordApiError를 발생시켜 구분한다.
    """
    response = call_loanword_api(word)

    if response.status_code == 403:
        raise LoanwordApiError(f"인증 실패(403): '{word}' 조회 거부됨")

    if response.status_code != 200:
        raise LoanwordApiError(
            f"API 조회 실패(status_code={response.status_code}): '{word}'"
        )

    try:
        body = response.json()
    except ValueError as e:
        raise LoanwordApiError(f"응답 JSON 파싱 실패: '{word}'") from e

    if "notation" not in body:
        raise LoanwordApiError(f"응답 형식 오류(notation 필드 없음): '{word}'")

    return body["notation"]
