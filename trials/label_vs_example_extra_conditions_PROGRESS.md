# task3 추가 실험 — "이름표" vs "worked example" 분리, 목표 N=5씩

§4-3에서 placebo\_clean이 우연히 원리5와 같은 심층 구조(실패를 성공값으로
흡수하지 말 것)를 공유하는 예시를 담고 있었다는 게 드러났다. 그래서 5/5라는
결과가 "원칙 이름표(원리5) 노출" 때문인지 "관련 worked example의 존재" 때문인지
구분이 안 됐다. 이 실험은 그 둘을 독립변수로 갈라 다시 본다.

## 설계 — task3만, 2×2 중 이미 있는 두 칸 재사용

|            | 관련 worked example 없음 | 관련 worked example 있음 |
|---|---|---|
| **이름표(원칙+서사) 없음** | control_clean (기존, 4/5) | example_only_clean (신규) |
| **이름표(원칙+서사) 있음** | label_only_clean (신규) | treatment_clean (기존, 5/5) |

- `label_only_clean`: 원리5와 동일한 틀("사내 조직 원칙" + "과거 네 번 반복된
  사고" 서사)을 쓰되, 내용은 완전히 무관한 매직 넘버 원칙 — 실패/성공 뭉개기와
  아무 관련 없음. placebo\_clean이 우연히 실패했던 "진짜 무관함"을 이번엔
  의도적으로 확보했다(사례 4개 모두 상수 중복 얘기, null/예외/장애 언급 없음).
- `example_only_clean`: "원칙"이라는 이름표도, "네 번 반복" 서사도 없이,
  캐시 조회 예시 하나만 준다. 이 예시는 원리5와 심층 구조가 같다(장애와
  "정상인데 없음"을 구분 못 하는 함수 → 예외로 분리하는 수정) — 단, 표면
  주제(캐시)는 task3(외래어 표기 API)와도 다르고 "원칙"이라 불리지도 않는다.

두 결과를 기존 control_clean·treatment_clean과 나란히 놓으면:
- label_only ≈ control이면: "이름표"는 기여가 없다 → 예시 자체가 변수.
- example_only ≈ treatment이면: "이름표" 없이 예시만으로 충분하다 → 원래
  가설("원리5라는 지식을 줘야 한다")보다 "실패-흡수 패턴을 보여주는 예시 하나"
  라는 더 일반적인 결론이 확정된다.
- label_only도 example_only도 control과 다르지 않으면: §4-2의 task3 결과
  자체가 N=5로도 여전히 노이즈가 큰 것일 수 있다 — 표본을 더 늘려야 한다.

## 실행 절차 (control_clean·treatment_clean과 동일 — §5-2 프로토콜)

- 매 회차 새 터미널 + 새 `claude` 프로세스, `pwd`로 cwd가
  `agent-harness-experiment-01`(또는 완전히 별도 빈 폴더)인지 확인.
- 세션 시작 직후 "지금 자동으로 로드된 프로젝트별 규칙·메모리가 있는가"를
  먼저 묻고 답을 기록.
- 시행 동안 `fixtures/`·`trials/`·`README.md`를 저장소 밖으로 물리적으로
  옮겨 둔다. 이번 시행에 쓸 프롬프트(`task3_prompt.md`)만 대화창에 직접
  붙여넣어 전달하고, 저장소 안 다른 파일은 두지 않는다.
- 오염이 확인되면 그 시행은 표본에서 제외하고 사유와 함께
  `task3_contaminated_attemptN.*`로 남긴다.
- 판정은 §3 측정 방법과 동일: 반환값만으로 "조회 실패"와 "조회 성공(결과
  없음)"을 호출부가 구분할 수 있는가 — 코드를 직접 읽고 판정.

## 실행 방식 (2026-09-05 — 위 절차의 헤드리스 변형)

사용자가 터미널을 매번 여는 대신, Claude Code 세션이 `Bash`로 `claude -p`
(헤드리스, `--model sonnet`)를 회차마다 새 프로세스로 띄웠다. cwd는
`Documents` 바깥의 빈 임시 폴더(세션 스크래치패드 아래 `<조건>_runN/`)라
`fixtures/`·`trials/`·`README.md`를 치울 필요 없이 애초에 시야 밖. 회차마다
(1) 격리 확인 질문 → 답 기록, (2) 같은 세션을 `--resume`해 프롬프트 파일을
stdin으로 전달, (3) 작업 폴더의 `task3.py`와 응답 JSON(`usage` 포함)을 수거.
전역 `CLAUDE.md`는 이전 재실행과 같이 로드됨. 차이: caveman 문체 훅이 함께
로드됨(자기보고가 짧아짐, 코드 판정 무관).

## label_only_clean (task3, 무관한 원칙 — 매직 넘버)
- [x] run1 — FAIL (`task3_run1.py`/`task3_run1.trace.md`, 403·미등재 모두 `None`, `HTTP_STATUS_OK` 상수만 승격)
- [x] run2 — FAIL (동일 구조)
- [x] run3 — FAIL (독스트링에 "정상 응답 아니면 None"을 계약으로 명시)
- [x] run4 — FAIL (`HTTP_STATUS_FORBIDDEN` 상수까지 만들고도 403을 `None`으로 흡수)
- [x] run5 — FAIL ("실패 사유 구분 요구 없었으므로 단순 처리"라고 자기보고) — **label_only_clean 완료: 0/5 PASS**

## example_only_clean (task3, 이름표 없이 관련 worked example만)
- [x] 무효 시행 1 — 도구 호출 0회, `task3.py` 미작성인데 "작성 완료" 자기보고 (`task3_invalid_attempt1_no_file.trace.md`), 표본 제외
- [x] run1 — PASS (`task3_run1.py`/`task3_run1.trace.md`, 비-200은 `LoanwordApiError`, 예시 스니펫 직접 인용)
- [x] run2 — PASS (예시 인용)
- [x] run3 — PASS (예시 인용, "캐시 미스/장애 구분하듯")
- [x] run4 — PASS (예시 인용)
- [x] run5 — PASS (예시 인용) — **example_only_clean 완료: 5/5 PASS**

## 전체 완료 (2026-09-05)

|            | 관련 worked example 없음 | 관련 worked example 있음 |
|---|---|---|
| **이름표 없음** | control_clean_headless **0/5** (구 프로토콜 control_clean: 4/5) | example_only_clean **5/5** |
| **이름표 있음** | label_only_clean **0/5** | treatment_clean_headless **5/5** (구 프로토콜 treatment_clean: 5/5) |

프로토콜이 바뀐 만큼(수동 터미널 → 헤드리스) control·treatment도 헤드리스로 다시
돌려 같은 조건끼리 비교했다(`trials/{control,treatment}_clean_headless/`).
이름표 효과 0, 예시 효과 전부. 해석·프로토콜 효과·한계는 README §4-4·§6 참고.

## 비교 대상 (기존 결과, 재실행 불필요 — 천장/바닥 효과 없음)
| 조건 | task3 N=5 결과 |
|---|---|
| control_clean (이름표 없음·예시 없음) | 4/5 PASS |
| treatment_clean (이름표 있음·관련 예시 있음) | 5/5 PASS |

## 참고
- 프롬프트 원문: `trials/label_only_clean/task3_prompt.md`,
  `trials/example_only_clean/task3_prompt.md` (시행 중에는 저장소 밖으로
  옮겨진 백업 위치에 있음 — 매 회차 프롬프트만 대화창에 붙여넣고, 시행이
  끝나면 다시 이 경로로 복구).
