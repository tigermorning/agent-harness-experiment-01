"""외래어 표준 표기 조회."""


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


class LoanwordAPIError(RuntimeError):
    """외래어 표기 API가 정상 응답(200)을 주지 않았을 때 발생한다."""

    def __init__(self, word: str, status_code: int):
        super().__init__(
            f"외래어 표기 API 조회 실패: word={word!r}, status_code={status_code}"
        )
        self.word = word
        self.status_code = status_code


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 API에서 조회해 반환한다.

    반환값 None은 오직 한 가지 뜻이다: API가 정상 응답(200)했고 해당 단어가
    표기 사전에 **등재되어 있지 않다**(`{"notation": null}`)는 것.

    이름만으로는 드러나지 않는 동작:
      - 네트워크 호출을 한다(부작용 있음, 느릴 수 있음). 캐시하지 않으므로
        호출할 때마다 매번 요청이 나간다.
      - 200이 아닌 응답(예: 헤더 누락으로 인한 403)은 삼키지 않고
        `LoanwordAPIError`를 발생시킨다. 조회 실패를 "등재 없음"과 같은
        None으로 뭉개면 호출부가 두 상황을 구분할 수 없기 때문이다.
      - 200인데 JSON 파싱에 실패하거나 "notation" 키가 없으면 그대로 예외가
        전파된다(각각 `response.json()`의 예외, `KeyError`).

    Args:
        word: 표준 표기를 찾을 외래어.

    Returns:
        표준 표기 문자열. 단어가 등재되어 있지 않으면 None.

    Raises:
        LoanwordAPIError: 응답 status_code가 200이 아닐 때.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordAPIError(word, response.status_code)

    return response.json()["notation"]
