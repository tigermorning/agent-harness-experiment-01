"""외래어 표기 공공 API로 단어의 표준 표기를 조회한다."""


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


class LoanwordApiError(Exception):
    """외래어 표기 API가 정상 응답을 주지 못했을 때 발생한다.

    status_code는 응답을 받긴 했으나 200이 아닌 경우의 상태 코드이고,
    응답 자체를 못 받았거나 바디를 해석하지 못한 경우에는 None이다.
    """

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def get_standard_notation(word: str) -> str | None:
    """외래어 표기 API를 호출해 word의 표준 표기를 반환한다.

    이름만으로는 드러나지 않는 동작:

    - 매 호출마다 call_loanword_api로 **네트워크 요청을 실제로 보낸다.**
      캐시나 로컬 사전을 거치지 않으므로 호출 비용과 지연이 있다.
    - 반환값 None은 오직 **"API가 정상 응답했고, 그 단어는 등재가 없다"**
      (바디의 notation이 null)는 뜻이다. 조회 실패를 None으로 뭉개지 않는다.
    - 200이 아닌 응답(문서에 언급된 403 포함), 바디를 JSON으로 읽지 못한 경우,
      바디에 notation 키가 없거나 문자열/null이 아닌 경우에는 모두
      LoanwordApiError를 던진다. 즉 "표기를 못 찾음"과 "조회가 실패함"은
      호출부에서 구분할 수 있다.
    - call_loanword_api가 던지는 예외(네트워크 오류 등)는 감싸지 않고
      그대로 전파한다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordApiError(
            f"외래어 표기 API가 {response.status_code}를 반환했다 (word={word!r})",
            status_code=response.status_code,
        )

    try:
        body = response.json()
    except ValueError as exc:
        raise LoanwordApiError(
            f"외래어 표기 API 응답 바디를 JSON으로 해석하지 못했다 (word={word!r})"
        ) from exc

    if not isinstance(body, dict) or "notation" not in body:
        raise LoanwordApiError(
            f"외래어 표기 API 응답에 notation 필드가 없다 (word={word!r})"
        )

    notation = body["notation"]
    if notation is None:
        return None
    if not isinstance(notation, str):
        raise LoanwordApiError(
            f"외래어 표기 API의 notation 값이 문자열이 아니다: {type(notation).__name__} (word={word!r})"
        )
    return notation
