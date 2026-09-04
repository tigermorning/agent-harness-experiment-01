def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


class LoanwordLookupError(Exception):
    """조회 자체가 실패했을 때(비정상 status_code, 파싱 불가 등) 발생시킨다."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def get_standard_notation(word: str) -> str | None:
    """표준 표기를 조회한다.

    반환값은 조회 성공(등재 없음 포함)일 때만 쓴다.
    - "표기값" : 등재됨
    - None     : 조회는 성공했지만 등재된 표기가 없음 (notation == null)

    조회 자체가 실패한 경우(403 등 비정상 status_code, JSON 파싱 실패,
    응답 형식 오류)는 LoanwordLookupError를 발생시킨다. None을 실패 신호로
    같이 쓰지 않는다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise LoanwordLookupError(
            f"외래어 표기 조회 실패: status_code={response.status_code}",
            status_code=response.status_code,
        )

    try:
        body = response.json()
    except ValueError as e:
        raise LoanwordLookupError(f"응답 JSON 파싱 실패: {e}") from e

    if not isinstance(body, dict) or "notation" not in body:
        raise LoanwordLookupError(f"예상치 못한 응답 형식: {body!r}")

    return body["notation"]
