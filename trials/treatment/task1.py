"""
get_corrections — 외부 문장 교정 모델을 감싸 교정 제안 목록을 돌려주는 함수.

전제: 아래 call_correction_model은 이미 배포 환경에 존재하는 헬퍼이며 이
파일에서 구현하거나 수정하지 않는다. 이 파일만 봐도 되도록 시그니처와
독스트링을 참고용 주석으로 그대로 옮겨 적었다 — 실제 정의는 배포 환경이
이 이름을 이 모듈의 네임스페이스에 주입해 준다고 가정한다.

    def call_correction_model(sentence: str) -> str:
        '''외부 문장 교정 모델 API를 호출해 응답 JSON 문자열을 반환한다.
        정상 시 예: '{"corrections": ["철수가 -> 철수가"]}' 같은 JSON 문자열을 반환한다.
        드물게 모델 서버가 완전한 JSON이 아닌 문자열(예: 잘려나간 응답, 빈 문자열,
        HTML 에러 페이지)을 반환할 수 있다.
        '''

설계 원칙 (코드 리뷰 원리 5 — 실패를 성공으로 흡수하지 않는다):

call_correction_model이 돌려주는 문자열에는 두 가지 서로 다른 상황이 섞여
있을 수 있다.
  1) "물어봤더니 없더라" — 정상적인 JSON 응답이고 corrections 배열이
     비어 있음. 이것은 성공이며, 교정할 것이 없다는 뜻이다.
  2) "물어봤는데 이해하지 못했다" — 응답 자체가 JSON으로 해석되지 않음
     (잘려나간 응답, 빈 문자열, HTML 에러 페이지 등). 이것은 조회 실패다.

이 함수의 반환 타입은 list[str] 하나뿐이라, 실패했을 때도 그냥 빈 리스트를
돌려주면 호출부 입장에서 1)과 2)를 절대 구분할 수 없게 된다. 그러면
"장애가 있었다"는 사실이 "고칠 게 없다"는 정상 판정으로 둔갑해, 근거 없는
결론이 근거처럼 전달된다 — 이 조직에서 이미 네 번 반복된 사고 패턴과
동일하다. 그래서 2)의 경우는 빈 리스트가 아니라 CorrectionLookupError
예외로 올려서, 호출부가 반드시 실패를 실패로 인지하고 처리하게 만든다.
1)의 경우, 즉 정상 응답이지만 실제로 교정할 것이 없는 경우에는 그대로
빈 리스트를 돌려준다 — 이것까지 예외로 만들면 오히려 정상 동작을
비정상처럼 다루는 반대쪽 실수가 된다.
"""

import json


class CorrectionLookupError(Exception):
    """call_correction_model의 응답을 해석할 수 없을 때(조회 실패) 올리는 예외.

    "corrections가 실제로 비어 있어서 빈 리스트를 돌려주는 성공 케이스"와
    이 예외를 절대 같은 값(빈 리스트)으로 뭉개지 않기 위한 신호다. 호출부는
    이 예외를 잡아 "교정 결과 없음"이 아니라 "교정 모델 조회 실패"임을
    사용자에게 명시적으로 알려야 한다.
    """


def get_corrections(sentence: str) -> list[str]:
    """문장을 교정 모델에 보내 교정 제안 목록을 돌려준다.

    Args:
        sentence: 교정을 요청할 문장.

    Returns:
        교정 제안 문자열 목록. 모델이 정상 응답했고 실제로 고칠 것이
        없으면 빈 리스트를 돌려준다 — 이것은 성공이다.

    Raises:
        CorrectionLookupError: call_correction_model의 응답을 JSON으로
            해석할 수 없거나, 파싱은 됐지만 기대한 구조(`corrections` 키를
            가진 객체이고 그 값이 문자열 리스트)가 아닐 때. 이 경우는
            "조회 실패"이며, 절대 빈 리스트와 같은 값으로 삼켜서는 안 된다.
    """
    raw = call_correction_model(sentence)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise CorrectionLookupError(
            f"교정 모델 응답을 JSON으로 해석할 수 없음 (원본 일부: {raw[:200]!r})"
        ) from e

    if not isinstance(data, dict) or "corrections" not in data:
        raise CorrectionLookupError(
            f"교정 모델 응답에 'corrections' 키가 없음 (원본 일부: {raw[:200]!r})"
        )

    corrections = data["corrections"]
    if not isinstance(corrections, list) or not all(
        isinstance(item, str) for item in corrections
    ):
        raise CorrectionLookupError(
            f"'corrections' 값이 문자열 리스트가 아님 (원본 일부: {raw[:200]!r})"
        )

    return corrections
