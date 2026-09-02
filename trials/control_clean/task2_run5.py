"""지역어 사전 API로 단어의 방언 대응형을 조회한다."""


class DialectAPIError(RuntimeError):
    """지역어 사전 API가 정상 응답(200)을 주지 못했을 때 발생한다."""

    def __init__(self, word: str, status_code: int):
        super().__init__(
            f"지역어 사전 API 조회 실패: word={word!r}, status_code={status_code}"
        )
        self.word = word
        self.status_code = status_code


# --- 아래 헬퍼는 주어진 것을 그대로 옮긴 것이다. 구현·수정하지 않는다. ---
# (배포 환경에서는 이 정의 대신 실제 모듈에서 import 해서 쓴다.)
def request_dialect_api(word: str):
    """사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
    서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


def find_dialect_matches(word: str) -> list[str]:
    """`word`에 대응하는 지역어 목록을 반환한다.

    정상 응답이면 JSON 바디의 "matches" 리스트를 그대로 돌려준다.
    200이 아닌 응답(예: 서버 쪽 5xx)은 DialectAPIError로 올린다 — 조회에
    실패한 것과 대응형이 하나도 없는 것은 다른 상황이므로 빈 리스트로
    뭉뚱그리지 않는다.
    """
    response = request_dialect_api(word)

    if response.status_code != 200:
        raise DialectAPIError(word, response.status_code)

    return response.json()["matches"]
