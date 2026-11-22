# T013 · EvidenceSuggestionService

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `EvidenceSuggestionService` (Python). 부모: 없음 (합성).
- 역할: 같은 snapshot의 원문과 관점으로 지지·반대 근거를 한 요청에서 제안받고 검증·캐시한다.
- 연결 기능: F07.
- 생성 예정 파일: `server/second_look/evidence_suggestion_service.py`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: [T001 SessionPolicy](T001-SessionPolicy.md), [T002 SessionRepository](T002-SessionRepository.md), [T003 TranscriptTimeline](T003-TranscriptTimeline.md), [T006 SuggestionValidator](T006-SuggestionValidator.md), [T007 ModelGateway](T007-ModelGateway.md)
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

기본5분 전사는 전체를 작은context로 보낸다. 초기 vector DB나 다중LLM연쇄를 전제하지 않는다. 1~2연결을 우선한다. 캐시는 session·원문/루브릭·메모·prompt/model/settings hash가 모두같을때만 재생한다. AI 입력 inputRevision/hash와 전체 eventRevision은 구분한다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `createSnapshot(sessionId)` | 공개된 확정 관점·고정전사·루브릭 | 입력hash와revision snapshot | 외부AI동의·phase검사. |
| `suggestForDifference(snapshot)` | 검증된차이와전체원문 | 미신뢰 지지/반대 ID·열린질문 | 반대근거없으면빈배열. deadline 동안입력/HUD상태차단X. |
| `verifyAndPersistProposal(snapshot, response)` | AI응답·최초snapshot | suggested 제안·원문발췌 | Validator 통과 후 권한·phase와 의존 입력 inputRevision/hash 재확인. HUD/ACK eventRevision만의 변화로 거부하지 않음. |
| `replayExactCache(key)` | 완전동일입력hash·모델설정 | mode=cache 결과또는miss | prepared/live/cache 출처를 명시. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```python
class EvidenceSuggestionService:
    """역할: 같은 snapshot의 원문과 관점으로 지지·반대 근거를 한 요청에서 제안받고 검증·캐시한다. 상태 소유권과 의존은 본 명세를 따른다."""
    # createSnapshot(sessionId)
    # 입력: 공개된 확정 관점·고정전사·루브릭 출력: 입력hash와revision snapshot
    # 실패·부작용: 외부AI동의·phase검사.
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

- [검증 문서](Verification/T013-EvidenceSuggestionService.verification.md)
- [진행 Checklist](Checklist/T013-EvidenceSuggestionService.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Gemini 구조화 출력](https://ai.google.dev/gemini-api/docs/structured-output), [지연 최적화](https://developers.openai.com/api/docs/guides/latency-optimization). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
