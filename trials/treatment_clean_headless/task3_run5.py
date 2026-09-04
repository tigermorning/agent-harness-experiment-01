def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


class LoanwordApiError(Exception):
    """조회 자체가 실패했을 때(비-200 응답, 응답 형식 오류) 발생시킨다."""


def get_standard_notation(word: str) -> str | None:
    """word의 표준 외래어 표기를 반환한다. 등재가 없으면 None.

    조회 실패(비-200, 형식 오류)는 None이 아니라 LoanwordApiError로 구분한다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordApiError(
            f"'{word}' 조회 실패: status_code={response.status_code}"
        )

    try:
        body = response.json()
        notation = body["notation"]
    except (ValueError, KeyError) as exc:
        raise LoanwordApiError(
            f"'{word}' 응답 형식 오류: {response.text!r}"
        ) from exc

    return notation
