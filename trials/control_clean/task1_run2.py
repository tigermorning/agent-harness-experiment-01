"""교정 모델 응답을 파싱해 교정 목록을 돌려준다."""

from __future__ import annotations

import json

_MAX_SNIPPET = 200


class CorrectionModelError(RuntimeError):
    """교정 모델 응답을 신뢰할 수 없다 = 조회에 실패했다는 뜻이다.

    '물어보지 못했다'(이 예외)와 '물어봤더니 고칠 게 없더라'(빈 리스트)는
    서로 다른 사실이므로 같은 반환값으로 뭉개지 않는다.
    """


# --- 이미 존재하는 헬퍼 (주어진 그대로, 구현·수정하지 않음) --------------------
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
    """`sentence`에 대한 교정 목록을 반환한다.

    빈 리스트는 **모델이 정상 응답했고 고칠 것이 없었다**는 뜻으로만 쓰인다.
    응답을 파싱할 수 없거나 형식이 계약과 다르면 `CorrectionModelError`를 올린다.
    """
    raw = call_correction_model(sentence)

    try:
        payload = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise CorrectionModelError(
            f"교정 모델이 JSON이 아닌 응답을 반환했다: {raw!r:.{_MAX_SNIPPET}}"
        ) from exc

    if not isinstance(payload, dict):
        raise CorrectionModelError(
            f"교정 모델 응답의 최상위가 객체가 아니다: {type(payload).__name__}"
        )

    if "corrections" not in payload:
        raise CorrectionModelError(
            f"교정 모델 응답에 'corrections' 키가 없다: {sorted(payload)!r:.{_MAX_SNIPPET}}"
        )

    corrections = payload["corrections"]
    if not isinstance(corrections, list) or not all(isinstance(c, str) for c in corrections):
        raise CorrectionModelError(
            f"'corrections'가 문자열 리스트가 아니다: {corrections!r:.{_MAX_SNIPPET}}"
        )

    return list(corrections)
