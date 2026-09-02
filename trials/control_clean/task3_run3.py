"""외래어 표준 표기 조회."""


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


class LoanwordAPIError(RuntimeError):
    """API가 200이 아닌 상태 코드로 응답했을 때 발생한다."""

    def __init__(self, word: str, status_code: int):
        self.word = word
        self.status_code = status_code
        super().__init__(
            f"외래어 표기 API 호출 실패: word={word!r}, status_code={status_code}"
        )


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 반환한다.

    등재된 표기가 없으면 None을 반환한다. API가 200이 아닌 응답을 주면
    LoanwordAPIError를 발생시킨다 — 조회 실패와 "등재 없음"은 다른 결과이므로
    None으로 뭉뚱그리지 않는다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordAPIError(word, response.status_code)

    return response.json().get("notation")
