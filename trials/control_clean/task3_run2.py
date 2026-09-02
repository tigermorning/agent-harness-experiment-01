"""외래어 표준 표기 조회.

`call_loanword_api`는 이미 존재하는 헬퍼다. 아래 정의는 프롬프트에 주어진 것을
그대로 옮겨 둔 것이며, 구현하거나 수정하지 않는다.
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


class LoanwordAPIError(RuntimeError):
    """외래어 표기 API가 정상 응답(200)을 주지 못했을 때 발생한다.

    반환값 None은 "조회에 성공했고 등재가 없다"는 뜻으로만 쓰므로, 조회 자체가
    실패한 경우는 값으로 뭉개지 않고 이 예외로 구분해 올린다.
    """

    def __init__(self, word: str, status_code: int):
        self.word = word
        self.status_code = status_code
        super().__init__(
            f"외래어 표기 API 조회 실패: word={word!r}, status_code={status_code}"
        )


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 반환한다.

    Returns:
        표준 표기 문자열. 조회는 됐지만 등재가 없으면 None.

    Raises:
        LoanwordAPIError: 응답 status_code가 200이 아닐 때(예: 헤더 누락으로 인한
            403). 등재 없음(None)과 구분하기 위해 예외로 올린다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordAPIError(word, response.status_code)

    return response.json()["notation"]
