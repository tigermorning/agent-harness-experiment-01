"""
외래어 표준 표기 조회.

아래는 이미 존재하는 헬퍼 함수 시그니처다 (구현체는 배포 환경에만 있음, 여기서는
그대로 호출만 한다):

    def call_loanword_api(word: str):
        \"\"\"외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.
        정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
        등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
        반환할 수도 있다.
        \"\"\"
"""

from typing import Optional


def get_standard_notation(word: str) -> Optional[str]:
    """외래어 word의 표준 표기를 돌려준다.

    - 정상 응답(200)이고 등재가 있으면: 표준 표기 문자열을 돌려준다.
    - 정상 응답(200)이고 등재가 없으면(notation: null): None을 돌려준다.
      이 None은 "물어봤더니 없더라"를 뜻하므로 안전한 값이다.
    - 정상 응답이 아니면(403 등 200이 아닌 상태 코드): None을 돌려주지 않고
      예외를 던진다. "못 물어봤다"를 "없더라"와 같은 값(None)으로 합쳐버리면
      호출부가 API 장애(예: 헤더 누락으로 인한 403)를 "표준 표기 미등재"로
      오인해, 근거 없는 결론을 근거처럼 사용자에게 전달하게 된다.
    """
    response = call_loanword_api(word)

    if response.status_code != 200:
        raise RuntimeError(
            f"외래어 표기 API 조회 실패: word={word!r}, "
            f"status_code={response.status_code}"
        )

    data = response.json()
    return data.get("notation")
