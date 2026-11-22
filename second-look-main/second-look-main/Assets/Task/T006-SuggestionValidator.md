# T006 · SuggestionValidator

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `SuggestionValidator` (Python). 부모: 없음 (합성).
- 역할: AI 제안의 구조·범위·실존 ID를 검증하고 인용문을 서버 원문에서 발췌한다.
- 연결 기능: F07, F08.
- 생성 예정 파일: `server/second_look/suggestion_validator.py`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: [T003 TranscriptTimeline](T003-TranscriptTimeline.md)
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

구조/ID 검증 통과는 관계 의미의 정확성 보증이 아니다. 의미는 gold set과 사람 검토로 따로 측정한다. 검증 실패 제안을 부분 성공처럼 조용히 확정하지 않는다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `validateSchema(payload)` | 미신뢰 AI JSON | 정규화 제안 또는 구조 오류 | 형·enum·길이·배열 크기·중복 제한 검증. |
| `validateReferences(snapshot, payload)` | 입력 snapshot·원문/기준/관점 ID | 같은 session/version에 속한 제안 | 실존해도 타 세션·낡은 version이면 거부. |
| `normalizeQuotes(timeline, payload)` | 검증된 인용 ID | 서버 발췌 verbatimText | LLM이 만든 인용문은 사용하지 않는다. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```python
class SuggestionValidator:
    """역할: AI 제안의 구조·범위·실존 ID를 검증하고 인용문을 서버 원문에서 발췌한다. 상태 소유권과 의존은 본 명세를 따른다."""
    # validateSchema(payload)
    # 입력: 미신뢰 AI JSON 출력: 정규화 제안 또는 구조 오류
    # 실패·부작용: 형·enum·길이·배열 크기·중복 제한 검증.
    # 구현 시 각 공개 함수에 이 계약의 docstring을 작성한다.
```

## 구현 순서와 완료 조건

1. 해당 클래스의 계약·보조 파일 소유권·입출력 타입 별칭을 고정한다.
2. 외부 의존을 mock으로 두고 클래스 하나만 구현한다.
3. 대응 검증 문서의 정상·경계·실패 사례를 실행한다. 필요한 실기기/API gate는 별도로 기록한다.
4. 결과·로그·환경·미검증을 Checklist에 반영한다. 독립 검증 후 다음 TASK에 계약을 인계한다.

- [ ] 클래스 하나와 해당 보조 산출물만 구현했다.
- [ ] 주석·입출력·실패 상태가 이 명세와 일치한다.
- [ ] 대응 검증 사례를 실행하고 근거를 남겼다.
- [ ] 독립 검증과 다음 TASK 인계를 마쳤다.

## 대응 문서와 근거

- [검증 문서](Verification/T006-SuggestionValidator.verification.md)
- [진행 Checklist](Checklist/T006-SuggestionValidator.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [JSON Schema 검증](https://python-jsonschema.readthedocs.io/en/stable/validate/), [Gemini 구조화 출력](https://ai.google.dev/gemini-api/docs/structured-output). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
