"""외래어 표준 표기 조회.

반환값 규약 (원칙 5):
  - 조회 성공 · 등재 있음  -> 표기 문자열 (str)
  - 조회 성공 · 등재 없음  -> None
  - 조회 실패             -> LoanwordLookupError 계열 예외

"조회에 실패했다"와 "조회는 됐는데 결과가 없다"는 절대 같은 반환값을 쓰지
않는다. None은 오직 "서버가 200으로 정상 응답했고, 그 바디가 등재 없음을
명시했다"는 뜻으로만 쓴다. 403/5xx나 형식 오류는 None으로 내려오지 않으므로
호출부가 이를 "등재된 항목 없음"으로 단정 표시할 수 없다.
"""

from __future__ import annotations


# --- 주어진 헬퍼 (수정 금지 · 원문 그대로) ---------------------------------

def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


# --- 실패 타입 -------------------------------------------------------------

class LoanwordLookupError(Exception):
    """조회 자체가 성립하지 않았음을 뜻한다. '등재 없음'과 겹치지 않는다."""

    def __init__(self, word: str, message: str) -> None:
        self.word = word
        super().__init__(message)


class LoanwordTransportError(LoanwordLookupError):
    """API에 닿지 못했다 (네트워크 오류, 타임아웃 등)."""


class LoanwordStatusError(LoanwordLookupError):
    """API가 200이 아닌 상태 코드로 응답했다 (403 인증 누락, 5xx 장애 등)."""

    def __init__(self, word: str, status_code: object) -> None:
        self.status_code = status_code
        super().__init__(word, f"'{word}' 조회 실패: HTTP 상태 {status_code!r}")


class LoanwordFormatError(LoanwordLookupError):
    """200으로 응답했지만 바디가 약속된 형식이 아니다."""


# --- 조회 ------------------------------------------------------------------

def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 반환한다.

    Returns:
        표준 표기 문자열. 조회는 성공했으나 등재가 없으면 None.

    Raises:
        LoanwordTransportError: API 호출 자체가 실패했다.
        LoanwordStatusError: 200이 아닌 응답 (403, 5xx 등).
        LoanwordFormatError: 200이지만 바디가 약속된 형식이 아니다.
    """
    try:
        response = call_loanword_api(word)
    except LoanwordLookupError:
        raise
    except Exception as exc:  # 네트워크 계층 예외를 조회 실패로 승격시킨다
        raise LoanwordTransportError(
            word, f"'{word}' 조회 실패: API 호출 중 {type(exc).__name__}"
        ) from exc

    status_code = getattr(response, "status_code", None)
    if status_code != 200:
        # 403(헤더 누락)·5xx(서버 장애)가 여기로 온다. None으로 뭉개지 않는다.
        raise LoanwordStatusError(word, status_code)

    try:
        payload = response.json()
    except Exception as exc:
        raise LoanwordFormatError(
            word, f"'{word}' 조회 실패: 응답 바디를 JSON으로 읽지 못했다"
        ) from exc

    if not isinstance(payload, dict) or "notation" not in payload:
        raise LoanwordFormatError(
            word, f"'{word}' 조회 실패: 응답 바디에 'notation' 키가 없다"
        )

    notation = payload["notation"]
    if notation is None:
        return None  # 조회 성공 · 등재 없음 — 유일하게 None을 반환하는 지점
    if not isinstance(notation, str):
        raise LoanwordFormatError(
            word,
            f"'{word}' 조회 실패: 'notation'이 문자열도 null도 아니다 "
            f"({type(notation).__name__})",
        )
    return notation
