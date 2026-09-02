"""외래어 표기 표준형 조회.

`call_loanword_api`는 이미 존재하는 헬퍼로, 여기서는 호출만 한다.
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


class LoanwordLookupError(RuntimeError):
    """표기 조회 자체가 실패했을 때 올린다("등재 없음"과 구분되는 상황).

    Attributes:
        word: 조회하려던 단어.
        status_code: 응답 상태 코드. 응답을 받기 전 단계에서 실패했으면 None.
    """

    def __init__(self, message: str, *, word: str, status_code: int | None = None):
        super().__init__(message)
        self.word = word
        self.status_code = status_code


def get_standard_notation(word: str) -> str | None:
    """외래어 표기 공공 API를 호출해 `word`의 표준 표기를 반환한다.

    반환값 None은 **"API에 등재가 없음"이라는 한 가지 뜻뿐이다**(status 200 +
    본문 {"notation": null}). 조회 자체가 실패한 경우에는 None을 반환하지 않고
    LoanwordLookupError를 올린다. 실패를 None으로 흡수하면 호출부가 "표준 표기가
    없는 단어"와 "조회를 못 한 단어"를 구분할 수 없고, 교정기가 후자를 전자로
    오인해 조용히 넘어가기 때문이다.

    캐시·재시도·헤더 보정·표기 정규화는 하지 않는다. 이름 그대로 API 응답을
    한 번 읽어 그대로 돌려주는 것이 전부다.

    Args:
        word: 조회할 단어.

    Returns:
        표준 표기 문자열, 또는 등재가 없으면 None.

    Raises:
        LoanwordLookupError: status_code가 200이 아니거나(예: 헤더 누락으로 인한
            403), 본문이 JSON이 아니거나, 본문에 "notation" 키가 없거나, 그 값이
            문자열도 None도 아닌 경우.
        NotImplementedError: 이 실습 환경에서 call_loanword_api를 실제로 호출한
            경우(헬퍼가 그대로 올리는 것을 삼키지 않는다).
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordLookupError(
            f"외래어 표기 API가 {response.status_code}를 반환했다: {word!r}",
            word=word,
            status_code=response.status_code,
        )

    try:
        body = response.json()
    except ValueError as exc:
        raise LoanwordLookupError(
            f"외래어 표기 API 응답이 JSON이 아니다: {word!r}",
            word=word,
            status_code=response.status_code,
        ) from exc

    if not isinstance(body, dict) or "notation" not in body:
        raise LoanwordLookupError(
            f"외래어 표기 API 응답에 'notation' 키가 없다: {word!r}",
            word=word,
            status_code=response.status_code,
        )

    notation = body["notation"]
    if notation is not None and not isinstance(notation, str):
        raise LoanwordLookupError(
            f"'notation' 값의 타입이 예상과 다르다({type(notation).__name__}): {word!r}",
            word=word,
            status_code=response.status_code,
        )

    return notation
