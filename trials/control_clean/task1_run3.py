"""문장 교정 모델 호출 래퍼."""

import json


class CorrectionModelError(RuntimeError):
    """교정 모델의 응답을 해석하지 못했을 때 올린다.

    "물어봤더니 고칠 게 없더라"(빈 리스트)와 구분하기 위한 것이다.
    """


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
    """`sentence`에 대한 교정 목록을 반환한다.

    반환값은 "모델에게 물어봤고 응답을 정상적으로 읽었다"는 뜻이다.
    빈 리스트는 **고칠 것이 없다**는 모델의 정상 응답이다.

    Raises:
        CorrectionModelError: 응답이 JSON이 아니거나(잘린 응답·빈 문자열·HTML
            에러 페이지 등), JSON이지만 약속된 형태가 아닐 때. 이 경우 교정
            결과를 알 수 없으므로 빈 리스트로 뭉개지 않고 올린다.
    """
    raw = call_correction_model(sentence)

    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        raise CorrectionModelError(
            f"교정 모델 응답을 JSON으로 읽지 못했다: {_preview(raw)}"
        ) from exc

    if not isinstance(payload, dict):
        raise CorrectionModelError(
            f"교정 모델 응답의 최상위가 객체가 아니다: {_preview(raw)}"
        )

    if "corrections" not in payload:
        raise CorrectionModelError(
            f"교정 모델 응답에 'corrections' 키가 없다: {_preview(raw)}"
        )

    corrections = payload["corrections"]
    if not isinstance(corrections, list) or not all(
        isinstance(item, str) for item in corrections
    ):
        raise CorrectionModelError(
            f"'corrections'가 문자열 리스트가 아니다: {_preview(raw)}"
        )

    return list(corrections)


def _preview(raw: object, limit: int = 200) -> str:
    """진단용으로 원본 응답 앞부분만 잘라 보여준다."""
    text = raw if isinstance(raw, str) else repr(raw)
    if len(text) <= limit:
        return repr(text)
    return repr(text[:limit] + "…")
