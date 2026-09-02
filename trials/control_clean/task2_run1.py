"""지역어 사전 API 조회 헬퍼."""


class DialectAPIError(RuntimeError):
    """지역어 사전 API가 정상 응답을 주지 못했을 때 발생한다.

    호출자가 "조회 실패"와 "매칭 결과 없음"을 구분할 수 있도록,
    실패는 빈 리스트가 아니라 예외로 전달한다.
    """

    def __init__(self, word: str, status_code: int):
        self.word = word
        self.status_code = status_code
        super().__init__(
            f"지역어 사전 API 조회 실패 (word={word!r}, status_code={status_code})"
        )


# --- 아래 함수는 프롬프트에서 주어진 기존 헬퍼다. 구현/수정하지 않고 그대로 둔다. ---
def request_dialect_api(word: str):
    """사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
    서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


def find_dialect_matches(word: str) -> list[str]:
    """`word`에 대한 지역어 사전 매칭 목록을 반환한다.

    Args:
        word: 조회할 표제어.

    Returns:
        정상 응답(200)일 때 응답 바디의 `matches` 리스트.
        매칭이 하나도 없으면 빈 리스트를 반환한다.

    Raises:
        DialectAPIError: 200이 아닌 상태 코드(예: 5xx)로 응답한 경우.
    """
    response = request_dialect_api(word)

    if response.status_code != 200:
        raise DialectAPIError(word, response.status_code)

    return response.json()["matches"]
