"""외래어 표준 표기 조회.

조회 실패(네트워크/서버 장애, 인증 오류, 응답 형식 오류)와
조회 성공이지만 등재가 없는 경우를 반환값 수준에서 구분한다.
- 실패      -> LoanwordLookupError 계열 예외
- 등재 없음 -> None
- 등재 있음 -> 표준 표기 문자열
"""


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


class LoanwordLookupError(Exception):
    """외래어 표기 조회가 실패했다. '등재 없음'과는 다른 상태다."""


class LoanwordAPIStatusError(LoanwordLookupError):
    """API가 200이 아닌 상태 코드를 반환했다 (403 인증 오류, 5xx 장애 등)."""

    def __init__(self, word: str, status_code: int):
        super().__init__(
            f"외래어 표기 API 조회 실패: word={word!r}, status_code={status_code}"
        )
        self.word = word
        self.status_code = status_code


class LoanwordResponseFormatError(LoanwordLookupError):
    """200이지만 바디가 약속된 형식({'notation': str | None})이 아니다."""

    def __init__(self, word: str, reason: str):
        super().__init__(f"외래어 표기 API 응답 형식 오류: word={word!r}, {reason}")
        self.word = word
        self.reason = reason


def get_standard_notation(word: str) -> str | None:
    """`word`의 표준 외래어 표기를 반환한다.

    Returns:
        표준 표기 문자열. 조회는 성공했으나 사전에 등재가 없으면 None.

    Raises:
        LoanwordAPIStatusError: 200이 아닌 응답(403 인증 오류, 5xx 장애 등).
        LoanwordResponseFormatError: 200이지만 바디를 해석할 수 없는 경우.
        Exception: call_loanword_api가 올리는 네트워크 예외는 그대로 전파한다.

    None은 오직 "조회에 성공했고 등재가 없다"만 의미한다. 조회 자체가
    실패한 경우는 호출부가 '등재 없음'으로 단정하지 못하도록 예외로 알린다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordAPIStatusError(word, response.status_code)

    try:
        payload = response.json()
    except ValueError as exc:
        raise LoanwordResponseFormatError(word, "JSON 파싱 실패") from exc

    if not isinstance(payload, dict) or "notation" not in payload:
        raise LoanwordResponseFormatError(word, "'notation' 키가 없음")

    notation = payload["notation"]
    if notation is None:
        return None  # 조회 성공, 사전에 등재 없음
    if not isinstance(notation, str):
        raise LoanwordResponseFormatError(
            word, f"'notation'이 문자열/null이 아님: {type(notation).__name__}"
        )
    return notation
