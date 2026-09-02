# 아래는 배포 환경에서만 제공되는 기존 헬퍼 함수의 시그니처다.
# 여기서는 구현하지 않고 그대로 호출만 한다.
#
# def request_dialect_api(word: str):
#     """사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.
#     정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
#     서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
#     """


def find_dialect_matches(word: str) -> list[str]:
    """단어에 대한 사투리 매칭 목록을 지역어 사전 API에서 조회해 반환한다.

    응답이 200이면 JSON의 "matches" 배열을 그대로 리스트로 반환하고,
    매칭이 없으면 빈 리스트를 반환한다. 200이 아닌 응답(5xx 등)은 "매칭 없음"과
    구분해야 하므로 빈 리스트로 흡수하지 않고 예외를 일으킨다.
    """
    response = request_dialect_api(word)
    response.raise_for_status()
    return response.json().get("matches", [])
