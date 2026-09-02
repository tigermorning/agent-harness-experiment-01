"""문장을 넣으면 교정 제안 목록을 돌려주는 유틸리티."""

import json

# ---------------------------------------------------------------------------
# call_correction_model은 이미 배포 환경에 구현되어 있는 헬퍼 함수다.
# 여기서는 구현하거나 수정하지 않고, get_corrections()에서 그대로 호출만
# 한다. 참고용으로 시그니처와 docstring만 주석으로 남겨 둔다.
#
# def call_correction_model(sentence: str) -> str:
#     """외부 문장 교정 모델 API를 호출해 응답 JSON 문자열을 반환한다.
#     정상 시 예: '{"corrections": ["철수가 -> 철수가"]}' 같은 JSON 문자열을 반환한다.
#     드물게 모델 서버가 완전한 JSON이 아닌 문자열(예: 잘려나간 응답, 빈 문자열,
#     HTML 에러 페이지)을 반환할 수 있다.
#     """
# ---------------------------------------------------------------------------


def get_corrections(sentence: str) -> list[str]:
    """문장을 교정 모델에 보내 얻은 교정 제안 목록을 반환한다.

    call_correction_model(sentence)이 돌려주는 JSON 문자열에서 "corrections"
    배열을 꺼내 리스트로 돌려준다. 교정할 것이 없으면 빈 리스트를 반환한다.
    모델 응답이 온전한 JSON이 아니거나(잘린 응답, 빈 문자열, HTML 에러
    페이지 등) 기대한 구조(문자열 리스트)를 갖추지 못한 경우에도 예외를
    던지지 않고 빈 리스트를 반환한다.
    """
    raw_response = call_correction_model(sentence)

    try:
        parsed_response = json.loads(raw_response)
    except json.JSONDecodeError:
        return []

    if not isinstance(parsed_response, dict):
        return []

    corrections = parsed_response.get("corrections")
    if not isinstance(corrections, list):
        return []

    return [item for item in corrections if isinstance(item, str)]
