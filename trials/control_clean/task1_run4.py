"""문장 교정 모델 응답을 파싱해 corrections 리스트를 돌려주는 얇은 래퍼."""

import json


class CorrectionResponseError(RuntimeError):
    """교정 모델이 기대한 형태의 JSON 응답을 주지 않았을 때 발생한다.

    `raw` 에 원본 응답을 그대로 담아 두므로, 잘린 응답인지 HTML 에러 페이지인지
    빈 문자열인지를 호출부나 로그에서 바로 확인할 수 있다.
    """

    def __init__(self, message: str, raw: str) -> None:
        super().__init__(f"{message} (raw={raw[:200]!r})")
        self.raw = raw


# --- 이미 존재하는 헬퍼 (주어진 그대로, 손대지 않음) ---------------------------
def call_correction_model(sentence: str) -> str:
    """외부 문장 교정 모델 API를 호출해 응답 JSON 문자열을 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 시 예: '{"corrections": ["철수가 -> 철수가"]}' 같은 JSON 문자열을 반환한다.
    드물게 모델 서버가 완전한 JSON이 아닌 문자열(예: 잘려나간 응답, 빈 문자열,
    HTML 에러 페이지)을 반환할 수 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")
# -----------------------------------------------------------------------------


def get_corrections(sentence: str) -> list[str]:
    """`sentence` 를 교정 모델에 넣고 교정 목록을 반환한다.

    교정할 게 없으면 빈 리스트를 반환한다. 응답이 JSON이 아니거나
    기대한 구조가 아니면 `CorrectionResponseError` 를 발생시킨다 —
    "교정할 게 없음"과 "서버가 깨진 응답을 줌"은 다른 사건이므로
    같은 빈 리스트로 뭉뚱그리지 않는다.
    """
    raw = call_correction_model(sentence)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CorrectionResponseError(
            f"교정 모델 응답을 JSON으로 파싱하지 못했습니다: {exc}", raw
        ) from exc

    if not isinstance(payload, dict):
        raise CorrectionResponseError(
            f"교정 모델 응답이 JSON 객체가 아닙니다 (type={type(payload).__name__})", raw
        )

    if "corrections" not in payload:
        raise CorrectionResponseError(
            "교정 모델 응답에 'corrections' 키가 없습니다", raw
        )

    corrections = payload["corrections"]
    if not isinstance(corrections, list):
        raise CorrectionResponseError(
            f"'corrections' 가 리스트가 아닙니다 (type={type(corrections).__name__})", raw
        )

    non_str = [item for item in corrections if not isinstance(item, str)]
    if non_str:
        raise CorrectionResponseError(
            f"'corrections' 에 문자열이 아닌 항목이 있습니다: {non_str[:3]!r}", raw
        )

    return corrections
