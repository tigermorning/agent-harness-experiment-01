"""외래어 표준 표기 조회.

주어진 헬퍼 `call_loanword_api`를 그대로 호출해 표준 표기를 얻는다.
헬퍼는 프롬프트에 주어진 형태 그대로이며 수정하지 않는다.
"""


class LoanwordAPIError(RuntimeError):
    """외래어 표기 API 호출이 정상 응답을 주지 못했음을 나타낸다.

    "등재된 표기가 없음"(정상 응답 + notation null)과 구분하기 위한 예외다.
    """

    def __init__(self, word: str, status_code: int):
        self.word = word
        self.status_code = status_code
        super().__init__(
            f"외래어 표기 API가 {word!r}에 대해 status {status_code}를 반환했다 "
            f"(정상 응답이 아니므로 표준 표기 유무를 판단할 수 없다)"
        )


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 반환한다.

    Returns:
        표준 표기 문자열. 정상 응답이지만 등재된 표기가 없으면 None.

    Raises:
        LoanwordAPIError: 응답이 200이 아닐 때(예: 헤더 누락으로 인한 403).
            호출 실패를 "표기 없음"(None)으로 뭉개지 않기 위해 예외로 올린다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordAPIError(word, response.status_code)

    notation = response.json().get("notation")
    return notation if notation else None
