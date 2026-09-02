"""지역어 사전 API 조회 래퍼.

`request_dialect_api`는 이 저장소에 이미 존재하는 헬퍼다. 여기서 구현하거나
수정하지 않으며, 이 모듈 스코프에서 호출 가능하다고 가정한다.
실제 배치 시 아래 주석 자리에 해당 모듈의 import 한 줄을 넣으면 된다.
"""

# from <기존_모듈> import request_dialect_api


class DialectAPIError(RuntimeError):
    """지역어 사전 API가 정상 응답(200)을 주지 못했을 때 발생한다."""

    def __init__(self, word: str, status_code: int):
        super().__init__(
            f"지역어 사전 API 조회 실패: word={word!r}, status_code={status_code}"
        )
        self.word = word
        self.status_code = status_code


def find_dialect_matches(word: str) -> list[str]:
    """`word`에 대한 지역어 사전 매치 목록을 반환한다.

    Args:
        word: 조회할 단어.

    Returns:
        매치된 표제어 리스트. 조회는 성공했지만 매치가 없으면 빈 리스트.

    Raises:
        DialectAPIError: 응답 상태 코드가 200이 아닐 때(예: 서버 5xx).
    """
    response = request_dialect_api(word)

    if response.status_code != 200:
        raise DialectAPIError(word, response.status_code)

    return response.json()["matches"]
