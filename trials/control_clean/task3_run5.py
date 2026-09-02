"""외래어 표준 표기 조회.

`call_loanword_api`는 이미 존재하는 헬퍼로 가정하고 그대로 호출한다.
"""


class LoanwordAPIError(RuntimeError):
    """외래어 표기 API 호출이 정상 응답을 주지 못했을 때 발생한다."""

    def __init__(self, word: str, status_code: int, detail: str = ""):
        self.word = word
        self.status_code = status_code
        message = f"외래어 표기 API 조회 실패 (word={word!r}, status={status_code})"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)


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

    반환값의 None은 오직 "API가 정상 응답했고, 그 단어가 등재되어 있지 않다"는
    뜻이다. 호출 자체가 실패한 경우(예: 헤더 누락으로 인한 403)는 None으로
    뭉개지 않고 LoanwordAPIError를 올린다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        detail = "요청 헤더 누락으로 거부되었을 수 있음" if response.status_code == 403 else ""
        raise LoanwordAPIError(word, response.status_code, detail)

    try:
        body = response.json()
    except ValueError as exc:
        raise LoanwordAPIError(word, response.status_code, f"JSON 파싱 실패: {exc}") from exc

    return body["notation"]
