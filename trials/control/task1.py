"""문장을 넣으면 교정 제안 목록을 돌려주는 get_corrections().

call_correction_model()은 이 파일 밖(배포 환경)에 이미 구현되어 있는 외부
함수이므로 여기서는 재구현하지 않고 그대로 호출만 한다. 참고용으로 시그니처와
독스트링만 아래에 옮겨 둔다.

    def call_correction_model(sentence: str) -> str:
        # 외부 문장 교정 모델 API를 호출해 응답 JSON 문자열을 반환한다.
        # 정상 시 예: '{"corrections": ["철수가 -> 철수가"]}' 같은 JSON
        # 문자열을 반환한다.
        # 드물게 모델 서버가 완전한 JSON이 아닌 문자열(예: 잘려나간 응답,
        # 빈 문자열, HTML 에러 페이지)을 반환할 수 있다.
        ...
"""

import json


def get_corrections(sentence: str) -> list[str]:
    """sentence에 대한 교정 제안 목록을 반환한다.

    call_correction_model()이 돌려주는 문자열은 정상 시 '{"corrections": [...]}'
    형태의 JSON이지만, 그 독스트링에 모델 서버가 드물게 완전한 JSON이 아닌
    문자열(잘려나간 응답, 빈 문자열, HTML 에러 페이지 등)을 돌려줄 수 있다고
    명시되어 있다. 그런 경우 json.loads가 실패하거나 파싱은 되어도 기대한
    구조("corrections" 키를 가진 dict, 그 값이 list)가 아닐 수 있으므로,
    이런 입력에도 예외를 올리지 않고 빈 목록을 반환한다.
    """
    raw = call_correction_model(sentence)

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(data, dict):
        return []

    corrections = data.get("corrections")
    if not isinstance(corrections, list):
        return []

    return [item for item in corrections if isinstance(item, str)]
