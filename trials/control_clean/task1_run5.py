"""교정 모델 응답에서 corrections 목록을 뽑아내는 얇은 래퍼."""

from __future__ import annotations

import json


class CorrectionResponseError(RuntimeError):
    """교정 모델이 기대한 형태의 JSON 응답을 주지 않았을 때 발생한다.

    잘려나간 응답, 빈 문자열, HTML 에러 페이지처럼 파싱 자체가 실패한 경우와
    JSON이긴 하지만 모양이 다른 경우를 모두 포함한다.
    """

    def __init__(self, reason: str, raw: str) -> None:
        excerpt = raw if len(raw) <= 200 else raw[:200] + " ...(이하 생략)"
        super().__init__(f"{reason} (원본 응답: {excerpt!r})")
        self.reason = reason
        self.raw = raw


# --- 아래 헬퍼는 프롬프트에 주어진 그대로다. 구현하거나 수정하지 않는다. ---
def call_correction_model(sentence: str) -> str:
    """외부 문장 교정 모델 API를 호출해 응답 JSON 문자열을 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 시 예: '{"corrections": ["철수가 -> 철수가"]}' 같은 JSON 문자열을 반환한다.
    드물게 모델 서버가 완전한 JSON이 아닌 문자열(예: 잘려나간 응답, 빈 문자열,
    HTML 에러 페이지)을 반환할 수 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")


def get_corrections(sentence: str) -> list[str]:
    """문장 하나를 교정 모델에 보내고 교정 목록을 돌려준다.

    Args:
        sentence: 교정할 문장.

    Returns:
        교정 문자열의 리스트. 교정할 것이 없으면 빈 리스트.

    Raises:
        CorrectionResponseError: 응답이 JSON이 아니거나, corrections 키가 없거나,
            corrections가 문자열 리스트가 아닐 때.
    """
    raw = call_correction_model(sentence)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CorrectionResponseError("JSON으로 파싱할 수 없는 응답", raw) from exc

    if not isinstance(payload, dict):
        raise CorrectionResponseError(
            f"최상위가 JSON 객체가 아님 ({type(payload).__name__})", raw
        )

    if "corrections" not in payload:
        raise CorrectionResponseError("응답에 'corrections' 키가 없음", raw)

    corrections = payload["corrections"]

    if not isinstance(corrections, list):
        raise CorrectionResponseError(
            f"'corrections'가 리스트가 아님 ({type(corrections).__name__})", raw
        )

    if not all(isinstance(item, str) for item in corrections):
        raise CorrectionResponseError("'corrections' 안에 문자열이 아닌 원소가 있음", raw)

    return corrections
