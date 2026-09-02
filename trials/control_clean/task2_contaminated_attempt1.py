"""지역어 사전 API 응답을 읽어 matches 리스트를 돌려준다."""


class DialectAPIError(RuntimeError):
    """지역어 사전 API 조회 자체가 실패한 경우.

    호출부가 '일치하는 지역어가 없었다'와 '사전을 조회하지 못했다'를 구분할 수
    있도록, 빈 리스트로 뭉개지 않고 이 예외를 쓴다.
    """

    def __init__(self, reason: str, *, word: str, status_code: int | None = None) -> None:
        detail = f"[{status_code}] " if status_code is not None else ""
        super().__init__(f"{detail}{word!r} 조회 실패: {reason}")
        self.reason = reason
        self.word = word
        self.status_code = status_code


# --- 아래 함수는 주어진 것 그대로다. 구현하거나 수정하지 않는다. ---
def request_dialect_api(word: str):
    """사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
    서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")
# --- 주어진 함수 끝 ---


def find_dialect_matches(word: str) -> list[str]:
    """`word`에 대응하는 지역어 목록을 반환한다.

    정상 응답(200)이면 `matches` 리스트를 그대로 돌려준다. 대응하는 지역어가
    없으면 빈 리스트가 나온다 — 이것은 정상적인 조회 결과다.

    Raises:
        DialectAPIError: 200이 아닌 응답(독스트링이 예고한 5xx 포함), 바디가
            JSON이 아닌 경우, 또는 JSON이지만 기대한 모양(`matches` 문자열
            리스트)이 아닌 경우. 이때 빈 리스트를 돌려주면 '지역어 없음'과
            구별되지 않으므로 조용히 삼키지 않는다.
    """
    response = request_dialect_api(word)

    if response.status_code != 200:
        raise DialectAPIError(
            "정상 응답이 아님", word=word, status_code=response.status_code
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise DialectAPIError(
            f"JSON 파싱 실패: {exc}", word=word, status_code=response.status_code
        ) from exc

    if not isinstance(payload, dict):
        raise DialectAPIError(
            f"최상위가 객체가 아님: {type(payload).__name__}",
            word=word,
            status_code=response.status_code,
        )

    if "matches" not in payload:
        raise DialectAPIError(
            "'matches' 키가 없음", word=word, status_code=response.status_code
        )

    matches = payload["matches"]
    if not isinstance(matches, list):
        raise DialectAPIError(
            f"'matches'가 리스트가 아님: {type(matches).__name__}",
            word=word,
            status_code=response.status_code,
        )

    if not all(isinstance(item, str) for item in matches):
        raise DialectAPIError(
            "'matches' 원소 중 문자열이 아닌 것이 있음",
            word=word,
            status_code=response.status_code,
        )

    return matches
