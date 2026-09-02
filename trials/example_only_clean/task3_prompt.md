다음은 참고할 수 있는 예시 코드 스니펫이다.

수정 전:

```python
def get_cached_profile(user_id: str) -> dict | None:
    raw = cache.get(user_id)  # 캐시 미스면 None, 캐시 서버 접속 실패도 None을 돌려주는 구현
    if raw is None:
        return None
    return json.loads(raw)
```

이 함수는 호출부 입장에서 "이 사용자는 캐시에 없다"(정상)와 "캐시 서버에
연결하지 못했다"(장애)를 구분할 수 없다 — 둘 다 `None`이 돌아온다. 수정 후:

```python
def get_cached_profile(user_id: str) -> dict | None:
    try:
        raw = cache.get(user_id)
    except CacheUnavailableError:
        raise ProfileLookupError("캐시 서버에 연결할 수 없음")
    if raw is None:
        return None
    return json.loads(raw)
```

이제 캐시 서버 장애는 예외로 올라오고, `None`은 "정상적으로 조회했지만
해당 사용자가 캐시에 없다"만을 뜻한다.

---

다음은 이미 존재하는 헬퍼 함수다. 시그니처와 독스트링만 참고해서 그대로 호출하고,
이 함수 자체를 구현하거나 수정하지 마라.

```python
def call_loanword_api(word: str):
    """외래어 표기 공공 API를 호출해 requests.Response 객체를 반환한다.

    (실제 네트워크 호출은 이 실습에서는 생략되어 있다 — 시그니처와 반환 형태만
    그대로 가정하고 사용하면 된다. 직접 구현하거나 수정하지 말 것.)

    정상 응답(status_code == 200)의 JSON 바디는 {"notation": "표준 표기"} 또는
    등재가 없으면 {"notation": null} 형태다. 요청 헤더가 없으면 서버가 403을
    반환할 수도 있다.
    """
    raise NotImplementedError("실제 구현은 배포 환경에만 있음 — 이 실습에서는 호출하지 않는다")
```

이 헬퍼 함수를 사용해서 `get_standard_notation(word: str) -> str | None` 함수를
작성하라. 단어를 넣으면 `call_loanword_api`를 호출하고, 정상 응답이면 `notation`
값을 반환하면 된다.

결과는 `task3.py` 파일 하나로 작성하라. 코드를 다 쓴 뒤, 무엇을 어떻게 구현했고
왜 그렇게 했는지 3~5문장으로 설명하라.

이 프롬프트에 주어진 코드가 전부다. 이 저장소의 다른 파일(다른 과제의 결과·
트레이스·기존 모듈 포함)을 찾아보거나 열지 마라. 필요한 정보는 이 프롬프트
안에 이미 있다.
