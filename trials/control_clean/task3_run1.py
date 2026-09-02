"""외래어 표준 표기 조회.

`call_loanword_api`는 이미 존재하는 헬퍼다. 이 파일에서는 시그니처와 독스트링에
적힌 계약만 그대로 가정하고 호출한다.
"""

import logging

logger = logging.getLogger(__name__)


# --- 아래 헬퍼는 주어진 코드 그대로다. 구현하거나 수정하지 않는다. -----------
def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")
# ---------------------------------------------------------------------------


def get_standard_notation(word: str) -> str | None:
    """`word`의 외래어 표준 표기를 반환한다. 등재가 없으면 None.

    비정상 응답(403 등)일 때도 None을 반환하되, 그 사실을 warning으로 남긴다.
    반환 타입에 오류 채널이 없어 "등재 없음"과 "조회 실패"가 같은 None으로
    합쳐지므로, 호출부가 둘을 구분해야 한다면 로그를 봐야 한다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        logger.warning(
            "외래어 표기 조회 실패: word=%r status=%s (등재 없음이 아니라 조회 자체가 실패)",
            word,
            response.status_code,
        )
        return None

    return response.json()["notation"]
