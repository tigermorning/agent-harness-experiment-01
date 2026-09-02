"""외래어 표기 조회 — 조회 실패와 "등재 없음"을 반환값 수준에서 구분한다."""

from __future__ import annotations


# --- 주어진 헬퍼 (그대로 사용, 구현·수정하지 않음) ---------------------------
def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


# --- 조회 실패를 나타내는 예외 ------------------------------------------------
class LoanwordLookupError(RuntimeError):
    """조회 자체가 실패했다. "조회는 됐지만 등재가 없다"(None)와 다른 상황이다."""

    def __init__(self, message: str, word: str, status_code: int | None = None):
        super().__init__(message)
        self.word = word
        self.status_code = status_code


class LoanwordAuthError(LoanwordLookupError):
    """401/403 — 인증·권한 문제로 조회하지 못했다 (등재 없음이 아니다)."""


class LoanwordServerError(LoanwordLookupError):
    """5xx — 서버 장애로 조회하지 못했다 (등재 없음이 아니다)."""


class LoanwordProtocolError(LoanwordLookupError):
    """200이지만 바디가 약속된 형식이 아니다 — 결과를 신뢰할 수 없다."""


# --- 조회 -------------------------------------------------------------------
def get_standard_notation(word: str) -> str | None:
    """`word`의 표준 외래어 표기를 돌려준다.

    반환:
        str:  조회 성공 + 등재된 표준 표기가 있음.
        None: 조회 성공 + 해당 단어의 등재가 없음(정상 응답, notation == null).

    예외:
        LoanwordAuthError:     인증·권한 오류(401/403)로 조회 실패.
        LoanwordServerError:   서버 5xx 장애로 조회 실패.
        LoanwordProtocolError: 200이나 바디 형식이 약속과 달라 판정 불가.
        LoanwordLookupError:   그 밖의 비정상 상태 코드로 조회 실패.
        그 외 call_loanword_api가 올리는 네트워크 예외는 그대로 전파된다.

    None은 오직 "정상적으로 조회했고 등재가 없었다"만 뜻한다. 조회에 실패한
    경우는 절대 None으로 내려가지 않으므로, 호출부가 장애를 "등재 없음"으로
    화면에 단정 표시할 수 없다.
    """
    response = call_loanword_api(word)
    status = response.status_code

    if status != 200:
        if status in (401, 403):
            raise LoanwordAuthError(
                f"외래어 표기 조회 인증 실패({status}): {word!r} — 등재 여부는 알 수 없음",
                word=word,
                status_code=status,
            )
        if 500 <= status < 600:
            raise LoanwordServerError(
                f"외래어 표기 API 서버 장애({status}): {word!r} — 등재 여부는 알 수 없음",
                word=word,
                status_code=status,
            )
        raise LoanwordLookupError(
            f"외래어 표기 조회 실패(HTTP {status}): {word!r} — 등재 여부는 알 수 없음",
            word=word,
            status_code=status,
        )

    try:
        body = response.json()
    except Exception as exc:  # JSON 파싱 불가 = 조회 실패이지 "등재 없음"이 아니다
        raise LoanwordProtocolError(
            f"외래어 표기 응답을 JSON으로 해석하지 못함: {word!r}",
            word=word,
            status_code=status,
        ) from exc

    if not isinstance(body, dict) or "notation" not in body:
        raise LoanwordProtocolError(
            f"외래어 표기 응답에 'notation' 필드가 없음: {word!r}",
            word=word,
            status_code=status,
        )

    notation = body["notation"]
    if notation is None:
        return None  # 조회 성공, 등재된 표기 없음
    if not isinstance(notation, str):
        raise LoanwordProtocolError(
            f"외래어 표기 'notation' 타입이 문자열이 아님({type(notation).__name__}): {word!r}",
            word=word,
            status_code=status,
        )
    return notation
