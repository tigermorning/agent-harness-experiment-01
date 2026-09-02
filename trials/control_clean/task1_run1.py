"""문장 교정 모델 응답을 파싱해 corrections 리스트를 돌려준다."""

import json


class CorrectionResponseError(RuntimeError):
    """교정 모델이 사용할 수 없는 응답을 돌려준 경우.

    호출부가 '교정할 것이 없었다'와 '응답을 읽지 못했다'를 구분할 수 있도록
    빈 리스트 대신 이 예외를 쓴다.
    """

    def __init__(self, reason: str, raw: str) -> None:
        super().__init__(f"{reason} (원문 응답: {raw!r:.200})")
        self.reason = reason
        self.raw = raw


# --- 아래 함수는 주어진 것 그대로다. 구현하거나 수정하지 않는다. ---
def call_correction_model(sentence: str) -> str:
    """외부 문장 교정 모델 API를 호출해 응답 JSON 문자열을 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 시 예: '{"corrections": ["철수가 -> 철수가"]}' 같은 JSON 문자열을 반환한다.
    드물게 모델 서버가 완전한 JSON이 아닌 문자열(예: 잘려나간 응답, 빈 문자열,
    HTML 에러 페이지)을 반환할 수 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")
# --- 주어진 함수 끝 ---


def get_corrections(sentence: str) -> list[str]:
    """`sentence`에 대한 교정 목록을 반환한다.

    정상 응답이면 `corrections` 리스트를 그대로 돌려준다. 교정할 것이 없으면
    빈 리스트가 나온다.

    Raises:
        CorrectionResponseError: 응답이 JSON이 아니거나(잘림, 빈 문자열, HTML
            에러 페이지 등), JSON이지만 기대한 모양(`corrections` 문자열 리스트)이
            아닌 경우. 이때 빈 리스트를 돌려주면 '교정 없음'과 구별되지 않으므로
            조용히 삼키지 않는다.
    """
    raw = call_correction_model(sentence)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CorrectionResponseError(f"JSON 파싱 실패: {exc.msg}", raw) from exc

    if not isinstance(payload, dict):
        raise CorrectionResponseError(
            f"최상위가 객체가 아님: {type(payload).__name__}", raw
        )

    if "corrections" not in payload:
        raise CorrectionResponseError("'corrections' 키가 없음", raw)

    corrections = payload["corrections"]
    if not isinstance(corrections, list):
        raise CorrectionResponseError(
            f"'corrections'가 리스트가 아님: {type(corrections).__name__}", raw
        )

    if not all(isinstance(item, str) for item in corrections):
        raise CorrectionResponseError("'corrections' 원소 중 문자열이 아닌 것이 있음", raw)

    return corrections
