"""사투리 매칭 조회.

아래 헬퍼는 이미 배포 환경에 구현되어 있다. 이 파일에서는 시그니처만 보고
그대로 호출만 하며, 직접 구현하거나 수정하지 않는다.

    def request_dialect_api(word: str):
        \"\"\"사내 지역어 사전 API를 호출해 requests.Response 객체를 반환한다.
        정상 응답(status_code == 200)의 JSON 바디는 {"matches": ["...", ...]} 형태다.
        서버 쪽 상태에 따라 5xx 상태 코드를 반환할 수도 있다.
        \"\"\"
"""


class DialectAPIError(Exception):
    """request_dialect_api가 5xx 등 비정상 상태 코드를 돌려줬을 때 발생한다.

    "물어봤는데 매칭이 없더라"(200 + 빈 matches)와 "애초에 못 물어봤다"(5xx 등
    조회 자체의 실패)를 똑같이 빈 리스트로 돌려주면, 서버 장애가 "이 단어는
    사투리 매칭이 없다"는 근거 있는 결론처럼 보이게 된다. 그래서 실패는 빈
    리스트가 아니라 예외로 올려 호출부가 두 경우를 구분해서 처리하게 한다.
    """


def find_dialect_matches(word: str) -> list[str]:
    """word에 대한 사투리 매칭 목록을 돌려준다.

    - 정상 응답(200)이면 JSON의 matches 배열을 그대로 리스트로 돌려준다.
      matches가 비어 있으면 그것 그대로 빈 리스트다(= 실제로 매칭이 없음).
    - 200이 아니면(5xx 등) 조회 자체가 실패한 것이므로 빈 리스트를 돌려주는
      대신 DialectAPIError를 올린다.
    """
    response = request_dialect_api(word)

    if response.status_code == 200:
        return list(response.json().get("matches", []))

    raise DialectAPIError(
        f"지역어 사전 API 조회 실패: word={word!r}, status_code={response.status_code}"
    )
