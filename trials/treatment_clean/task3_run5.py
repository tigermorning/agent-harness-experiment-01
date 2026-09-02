"""외래어 표준 표기 조회.

조회 실패(네트워크/인증/서버 장애/응답 형식 오류)와 조회 성공하되 등재가 없는
경우를 반환값 수준에서 구분한다:

    - 성공 & 등재 있음  -> str
    - 성공 & 등재 없음  -> None
    - 실패             -> LoanwordLookupError 예외

None은 오직 "서버가 정상 응답했고, 그 안에서 표제어가 없다고 말한 경우"에만 쓴다.
"""


class LoanwordLookupError(Exception):
    """외래어 표기 조회 자체가 실패했음을 알린다 (결과 없음과는 다르다).

    Attributes:
        word: 조회하려던 단어.
        status_code: HTTP 상태 코드를 알 수 있으면 그 값, 아니면 None.
    """

    def __init__(self, message: str, *, word: str, status_code: int | None = None):
        super().__init__(message)
        self.word = word
        self.status_code = status_code


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
    """`word`의 외래어 표준 표기를 돌려준다.

    Returns:
        표준 표기 문자열. 조회는 성공했으나 등재된 표기가 없으면 None.

    Raises:
        LoanwordLookupError: 조회를 끝내지 못한 모든 경우 — 호출 자체가 터졌거나,
            200이 아닌 응답(403 인증 누락, 5xx 서버 장애 등)이거나, 바디를 JSON으로
            읽을 수 없거나, 바디 형식이 계약과 다른 경우.
    """
    try:
        response = call_loanword_api(word)
    except Exception as exc:  # 네트워크 오류, 타임아웃, 미구현 등 호출 실패 전부
        raise LoanwordLookupError(
            f"외래어 API 호출 실패: {word!r} ({exc.__class__.__name__}: {exc})",
            word=word,
        ) from exc

    status_code = getattr(response, "status_code", None)
    if status_code != 200:
        # 403(헤더 누락)도 5xx(서버 장애)도 "등재 없음"이 아니다. 결과를 모르는 것이다.
        raise LoanwordLookupError(
            f"외래어 API가 비정상 상태로 응답: {word!r} (status={status_code})",
            word=word,
            status_code=status_code if isinstance(status_code, int) else None,
        )

    try:
        body = response.json()
    except Exception as exc:
        raise LoanwordLookupError(
            f"외래어 API 응답을 JSON으로 읽지 못함: {word!r} ({exc.__class__.__name__}: {exc})",
            word=word,
            status_code=status_code,
        ) from exc

    if not isinstance(body, dict) or "notation" not in body:
        # 형식이 깨진 응답을 "고칠 것 없음"으로 읽지 않는다.
        raise LoanwordLookupError(
            f"외래어 API 응답 형식이 계약과 다름: {word!r} (body={body!r})",
            word=word,
            status_code=status_code,
        )

    notation = body["notation"]
    if notation is None:
        return None  # 정상 응답, 등재된 표기가 없음
    if not isinstance(notation, str):
        raise LoanwordLookupError(
            f"외래어 API의 notation 타입이 예상과 다름: {word!r} "
            f"(type={type(notation).__name__}, value={notation!r})",
            word=word,
            status_code=status_code,
        )
    return notation
