from typing import Optional


def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.
    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    ...  # 실제 구현은 배포 환경에서 제공됨 (이 파일에서는 시그니처만 참고)


def get_standard_notation(word: str) -> Optional[str]:
    """외래어 word의 표준 표기를 API로 조회해 돌려준다. 등재가 없으면 None을 돌려준다."""
    response = call_loanword_api(word)
    if response.status_code != 200:
        return None
    return response.json().get("notation")
