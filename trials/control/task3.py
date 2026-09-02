"""외래어 표준 표기 조회.

call_loanword_api()는 별도 배포 환경에 구현되어 있으며, 이 파일에서는
그 시그니처만 그대로 가져다 쓴다 (직접 구현하지 않음).
"""

from typing import Optional


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.
    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 여기서는 시그니처만 사용")


def get_standard_notation(word: str) -> Optional[str]:
    """word의 외래어 표준 표기를 돌려준다. 등재가 없으면 None.

    status_code == 200 인 정상 응답만 "물어봤다"로 취급하고, 그 JSON의
    notation 필드(값이 있으면 표준 표기, null이면 등재 없음 → None)를 그대로
    돌려준다. 200이 아닌 응답(예: 헤더 누락으로 인한 403)은 "등재가 없다"가
    아니라 "물어보지 못했다"이므로, 여기서 None으로 뭉개지 않고 예외로
    올린다 — 조회 실패와 조회 결과 '없음'을 같은 값(None)으로 합치면
    호출부가 두 경우를 구분할 수 없게 된다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise RuntimeError(
            f"외래어 표기 API 조회 실패: word={word!r}, "
            f"status_code={response.status_code}"
        )

    return response.json().get("notation")
