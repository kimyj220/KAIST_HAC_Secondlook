# T011 · ReviewSessionService

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `ReviewSessionService` (Python). 부모: 없음 (합성).
- 역할: 세션 단계·참여자 가입·원자적 공동 공개와 비교 projection을 관리한다.
- 연결 기능: F01, F05, F06.
- 생성 예정 파일: `server/second_look/review_session_service.py`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: [T001 SessionPolicy](T001-SessionPolicy.md), [T002 SessionRepository](T002-SessionRepository.md), [T005 DifferenceClassifier](T005-DifferenceClassifier.md)
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

두 평가자가 각자 확정하기 전 공동 자료를 반환하지 않는다. 단계 진실과 revision은 서버가 소유한다. 1회 역할 nonce는 서버 actor에 매핑하고 재사용을 막는다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `createSession(config)` | 동의·미디어·전사·고정루브릭·참여자 수 | 세션과 초대 정보 | 조건 누락 시 생성 거부. |
| `join(roleToken)` | 1회 초대 nonce | 서버 매핑 actor token | 다른 세션/이미 쓴 nonce 거부. |
| `transition(command, expectedRevision)` | 인증 진행 명령·revision | 새 단계·revision | 허용하지 않는 전이·stale state 거부. |
| `revealWhenAllCommitted()` | 각 개인 확정 상태 | 한 번의 공동 공개 | 하나라도 미확정이면 비공개 유지. |
| `comparisonProjection(actor)` | 공개 세션 actor | 단독포착 우선 비교 데이터 | 공개 전에는 본인 범위만. |
| `publishPlaybackAnchor(command)` | 진행자 재생/정지/seek 명령·mediaTimeMs·expectedRevision | 서버 mono시각을 붙인 새 anchorRevision | 진행자 권한·미디어 범위 검증. seek/pause마다 anchor를 교체하고 배포한다. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```python
class ReviewSessionService:
    """역할: 세션 단계·참여자 가입·원자적 공동 공개와 비교 projection을 관리한다. 상태 소유권과 의존은 본 명세를 따른다."""
    # createSession(config)
    # 입력: 동의·미디어·전사·고정루브릭·참여자 수 출력: 세션과 초대 정보
    # 실패·부작용: 조건 누락 시 생성 거부.
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

- [검증 문서](Verification/T011-ReviewSessionService.verification.md)
- [진행 Checklist](Checklist/T011-ReviewSessionService.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [SQLite transaction](https://www.sqlite.org/lang_transaction.html), [FastAPI WebSocket](https://fastapi.tiangolo.com/advanced/websockets/). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
