"""지역어 사전 API 조회 헬퍼."""


class DialectApiError(RuntimeError):
    """지역어 사전 API가 정상 응답(200)을 주지 못했을 때 발생한다."""

    def __init__(self, word: str, status_code: int):
        super().__init__(
            f"지역어 사전 API 조회 실패: word={word!r}, status_code={status_code}"
        )
        self.word = word
        self.status_code = status_code


def request_dialect_api(word: str):
    """사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
    서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


def find_dialect_matches(word: str) -> list[str]:
    """`word`의 지역어 표제어 목록을 반환한다.

    정상 응답(200)이면 바디의 `matches` 리스트를 그대로 돌려준다.
    그 밖의 상태 코드(5xx 등)는 `DialectApiError`로 올린다 — 조회 실패와
    "일치 항목 없음"은 다른 사실이라 빈 리스트로 뭉뚱그리지 않는다.
    """
    response = request_dialect_api(word)

    if response.status_code != 200:
        raise DialectApiError(word, response.status_code)

    return response.json()["matches"]
