"""지역어 사전 조회 래퍼.

`request_dialect_api`는 주어진 헬퍼이며 여기서 구현·수정하지 않는다.
아래 정의는 프롬프트에 주어진 시그니처와 독스트링을 그대로 옮긴 것이다.
"""


def request_dialect_api(word: str):
    """사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
    서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


class DialectLookupError(RuntimeError):
    """지역어 사전에 '물어보지 못했다'는 사실을 알린다.

    '물어봤더니 없더라'(정상 응답, matches 빈 리스트)와 구별하기 위해 존재한다.
    후자는 빈 리스트로 돌아오고, 전자는 이 예외로 터진다.
    """

    def __init__(self, word: str, status_code: int):
        super().__init__(
            f"지역어 사전 조회 실패: word={word!r}, status_code={status_code} "
            f"(등재 여부를 알 수 없음)"
        )
        self.word = word
        self.status_code = status_code


def find_dialect_matches(word: str) -> list[str]:
    """`word`의 지역어 대응 표기 목록을 반환한다.

    정상 응답(200)이면 바디의 `matches` 리스트를 그대로 돌려준다.
    등재된 표기가 없으면 빈 리스트가 된다 — 이는 조회에 성공한 결과다.

    Raises:
        DialectLookupError: 200이 아닌 응답(예: 5xx). 조회 자체가 실패했으므로
            등재 여부를 단정할 수 없다.
        KeyError: 200인데 바디에 `matches`가 없는 경우. 응답 형식이 계약과
            다르다는 뜻이므로 빈 리스트로 뭉개지 않고 그대로 드러낸다.
    """
    response = request_dialect_api(word)

    if response.status_code != 200:
        raise DialectLookupError(word, response.status_code)

    return response.json()["matches"]
