"""외래어 표준 표기 조회.

반환값 규약 (원칙 5):
    조회 실패와 "조회 성공 · 등재 없음"을 절대 같은 값으로 뭉개지 않는다.

    - 정상 응답 + 등재 있음  -> 표기 문자열 (str)
    - 정상 응답 + 등재 없음  -> None
    - 그 밖의 모든 경우      -> LoanwordLookupError 하위 예외

    즉 None은 오직 "서버가 200으로 정상 응답했고, 그 단어는 사전에 없다"는
    확정된 사실일 때만 나온다. 403(인증 헤더 누락), 5xx(서버 장애), 형식이
    깨진 응답은 전부 예외로 나가므로 호출부가 '없음'으로 오해할 수 없다.
"""

from __future__ import annotations

from typing import Optional


# --- 제공된 헬퍼 (프롬프트에 주어진 그대로. 구현하거나 수정하지 않는다) ---
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
    """외래어 표기 조회가 실패했다. '등재 없음'과는 다른 사건이다."""


class LoanwordTransportError(LoanwordLookupError):
    """API 호출 자체가 성립하지 않았다 (네트워크 오류, 타임아웃 등)."""


class LoanwordHTTPError(LoanwordLookupError):
    """서버가 응답했지만 200이 아니다. 조회 결과에 대해 아무것도 알 수 없다."""

    def __init__(self, status_code: Optional[int], word: str) -> None:
        self.status_code = status_code
        self.word = word
        super().__init__(
            f"외래어 표기 API가 비정상 상태 코드를 반환했다 "
            f"(word={word!r}, status_code={status_code!r})"
        )


class LoanwordAuthError(LoanwordHTTPError):
    """403 — 요청 헤더/인증 문제. 사전에 없는 것이 아니라 물어보지 못한 것이다."""


class LoanwordResponseFormatError(LoanwordLookupError):
    """200이지만 바디가 약속된 {"notation": ...} 형태가 아니다."""


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 반환한다.

    Args:
        word: 표준 표기를 찾을 단어.

    Returns:
        표준 표기 문자열. 서버가 정상 응답했으나 등재된 항목이 없으면 None.

    Raises:
        LoanwordTransportError: 호출 자체가 실패했다.
        LoanwordAuthError: 403 — 인증/헤더 문제로 조회하지 못했다.
        LoanwordHTTPError: 그 밖의 비정상 상태 코드로 조회하지 못했다.
        LoanwordResponseFormatError: 200이지만 응답 형식이 약속과 다르다.
    """
    try:
        response = call_loanword_api(word)
    except LoanwordLookupError:
        raise
    except Exception as exc:  # 호출 실패는 '없음'이 아니다 — 삼키지 않는다
        raise LoanwordTransportError(
            f"외래어 표기 API 호출에 실패했다 (word={word!r})"
        ) from exc

    status_code = getattr(response, "status_code", None)
    if status_code != 200:
        error_type = LoanwordAuthError if status_code == 403 else LoanwordHTTPError
        raise error_type(status_code, word)

    try:
        body = response.json()
    except Exception as exc:
        raise LoanwordResponseFormatError(
            f"외래어 표기 API 응답 바디를 JSON으로 읽지 못했다 (word={word!r})"
        ) from exc

    if not isinstance(body, dict) or "notation" not in body:
        raise LoanwordResponseFormatError(
            f"외래어 표기 API 응답에 'notation' 키가 없다 "
            f"(word={word!r}, body={body!r})"
        )

    notation = body["notation"]
    if notation is None:
        # 여기서만 None이 나온다: 서버가 "그런 표제어는 없다"고 확인해 준 경우.
        return None
    if not isinstance(notation, str):
        raise LoanwordResponseFormatError(
            f"'notation' 값이 문자열도 null도 아니다 "
            f"(word={word!r}, notation={notation!r})"
        )
    return notation
