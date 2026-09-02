def request_dialect_api(word: str):
    """사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.
    정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
    서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
    """
    raise NotImplementedError  # 배포 환경에서 실제로 구현되어 제공됨


def find_dialect_matches(word: str) -> list[str]:
    response = request_dialect_api(word)
    if response.status_code == 200:
        return response.json()["matches"]
    return []
