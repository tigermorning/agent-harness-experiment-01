# trace — control_clean / task2 (find_dialect_matches), run3

## 참고: 이 run의 절차상 문제

이 run의 오염 확인 응답은 대화에 정상적으로 기록됐고 깨끗했다(전역 CLAUDE.md만,
프로젝트 규칙·메모리 없음 — 다른 run들과 동일). 그런데 **자기보고 텍스트를
받기 전에, 다음 run(run4)의 세션이 같은 파일명(`task2.py`)에 결과를 쓰면서
"이미 존재해서 덮어씁니다(내용은 열지 않았습니다)"라며 이 run의 산출물을
디스크에서 덮어썼다.** 다행히 코드 내용은 덮어써지기 전에 이미 `Read`로
확인해 대화 기록에 남아 있어 복구할 수 있었다(`task2_run3.py`는 그 복구본).
**자기보고 원문은 복구하지 못했다** — 판정은 코드만으로 내린다.

**교훈**: 병렬로 여러 run을 동시에 돌리지 않더라도, 항상 같은 출력 파일명
(`task1.py`/`task2.py`/`task3.py`)을 쓰게 하는 지금 프로토콜은 앞 run 결과가
대화에 채 기록되기 전에 다음 run이 같은 이름으로 덮어쓸 수 있다는 위험이 있다.
다음부터는 각 run의 결과를 받는 즉시(다음 run을 시작하기 전에) 파일을 옮겨
번호를 매기는 순서를 반드시 지킨다.

## 판정: PASS (코드 기준)

```python
def find_dialect_matches(word: str) -> list[str]:
    response = request_dialect_api(word)

    if response.status_code != 200:
        raise DialectAPIError(word, response.status_code)

    return response.json()["matches"]
```

`DialectAPIError`로 200이 아닌 응답(5xx 포함)과 매칭-없음(`[]`)을 분리. run1·
run2와 구조적으로 동일한 해법. 다른 run과 다른 점은 `request_dialect_api`
헬퍼 본문을 그대로 복사하지 않고 `# from <기존_모듈> import request_dialect_api`
주석으로 대체했다는 것 — 실행 가능한 단독 파일이 아니라는 뜻이지만, 판정
대상인 `find_dialect_matches`의 실패/성공 분리 로직 자체에는 영향이 없다.
