"""외래어 표준 표기 조회."""


class LoanwordApiError(RuntimeError):
    """외래어 표기 API가 정상 응답(200)을 주지 않았거나 응답 본문이 규약과 다를 때."""


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 API에서 조회해 반환한다.

    반환값 None은 오직 한 가지 의미다: API가 정상(200)으로 응답했고, 그 단어가
    외래어 표기 용례에 **등재되어 있지 않다**({"notation": null})는 뜻이다.
    "조회에 실패했다"는 None으로 표현하지 않는다.

    이름만으로는 드러나지 않는 동작:
      - 조회에 실패하면 `LoanwordApiError`를 올린다. 200이 아닌 응답(문서에
        언급된 403 포함)과, 200이지만 "notation" 키가 없는 본문이 여기 해당한다.
        실패를 None으로 흡수하면 호출부가 "등재 없음"과 구별할 수 없게 되므로
        일부러 삼키지 않는다.
      - 본문이 JSON이 아니면 `response.json()`이 올리는 예외가 그대로 전파된다.
      - 캐시·재시도·보정을 하지 않는다. 호출 한 번이 곧 결과다.

    Raises:
        LoanwordApiError: 위에 적은 조회 실패 상황.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordApiError(
            f"외래어 표기 API 조회 실패: word={word!r}, status={response.status_code}"
        )

    body = response.json()
    if "notation" not in body:
        raise LoanwordApiError(
            f"외래어 표기 API 응답에 'notation' 키가 없음: word={word!r}, body={body!r}"
        )

    return body["notation"]
