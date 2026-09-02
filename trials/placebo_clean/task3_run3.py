"""외래어 표준 표기 조회.

`get_standard_notation`은 외래어 표기 공공 API를 감싸는 얇은 조회 함수다.
"조회에 실패했다"와 "조회에 성공했고 등재가 없다"를 호출부가 반드시 구분할 수
있도록, 전자는 예외로 후자는 None으로 갈라서 돌려준다.
"""

from __future__ import annotations


# --- 이미 존재하는 헬퍼 (주어진 정의 그대로, 구현·수정하지 않음) ---------------

def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


# --- 여기서부터가 이번 과제의 구현 -------------------------------------------

class LoanwordAPIError(RuntimeError):
    """외래어 표기 API의 응답에서 표준 표기를 읽어내지 못했음을 나타낸다.

    "그 단어가 등재되어 있지 않다"(정상 응답)와는 다른 상황이다. 등재 없음은
    예외가 아니라 None으로 표현된다.
    """

    def __init__(self, message: str, *, word: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.word = word
        self.status_code = status_code


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 API에서 조회해 반환한다.

    이름만으로는 드러나지 않는 동작:

    - **호출마다 네트워크 요청이 1회 발생한다.** 캐시나 로컬 사전 폴백이 없으므로
      같은 단어를 N번 물으면 요청도 N번 나간다. 반복 조회를 한다면 호출부가
      직접 캐싱해야 한다.
    - **반환값 None은 뜻이 하나뿐이다:** "API가 정상 응답했고, 그 단어는 등재되어
      있지 않다". 조회 자체가 실패한 경우(헤더 누락으로 인한 403, 5xx, 깨진 본문
      등)는 None으로 뭉개지 않고 `LoanwordAPIError`를 raise한다.
    - **추측으로 값을 채우지 않는다.** 원문을 그대로 돌려주거나 빈 문자열로
      대체하는 폴백이 없다.
    - **입력을 정규화하지 않는다.** 공백 제거·대소문자 변환 없이 `word`를 그대로
      API에 넘긴다.

    Args:
        word: 조회할 외래어의 원어 표기.

    Returns:
        표준 표기 문자열. 정상 응답이지만 등재가 없으면 None.

    Raises:
        LoanwordAPIError: status_code가 200이 아니거나, 응답 본문이 JSON이 아니거나,
            본문이 {"notation": 문자열 | null} 형태가 아닌 경우.
    """
    response = call_loanword_api(word)

    status_code = response.status_code
    if status_code != 200:
        raise LoanwordAPIError(
            f"외래어 표기 API가 {word!r}에 대해 status_code={status_code}를 반환했다 "
            f"(403이면 요청 헤더 누락일 수 있다)",
            word=word,
            status_code=status_code,
        )

    try:
        body = response.json()
    except ValueError as exc:  # requests의 JSONDecodeError는 ValueError의 하위 클래스다
        raise LoanwordAPIError(
            f"외래어 표기 API가 {word!r}에 대해 JSON이 아닌 본문을 반환했다",
            word=word,
            status_code=status_code,
        ) from exc

    if not isinstance(body, dict) or "notation" not in body:
        raise LoanwordAPIError(
            f"외래어 표기 API 응답에 'notation' 키가 없다 (word={word!r}, body={body!r})",
            word=word,
            status_code=status_code,
        )

    notation = body["notation"]
    if notation is None:
        return None  # 정상 응답 + 미등재
    if not isinstance(notation, str):
        raise LoanwordAPIError(
            f"'notation' 값이 문자열도 null도 아니다 (word={word!r}, notation={notation!r})",
            word=word,
            status_code=status_code,
        )
    return notation
