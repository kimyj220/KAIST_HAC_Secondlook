# T002 · SessionRepository

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `SessionRepository` (Python). 부모: 없음 (합성).
- 역할: SQLite 저장·원자적 공개·이벤트 멱등성을 담당하는 유일한 저장 접근 창구다.
- 연결 기능: F01–F11 저장.
- 생성 예정 파일: `server/second_look/session_repository.py`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: 없음. 고정 JSON 계약과 테스트 fixture를 먼저 사용한다.
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

유일 키와 expectedRevision으로 중복과 동시 수정을 제어한다. 트랜잭션은 짧게 유지한다. UNIQUE만으로 payload 충돌을 판정하지 말고 기존 내용을 명시적으로 비교한다. 멱등 입력 처리에 기존 행을 삭제·교체하는 INSERT OR REPLACE를 쓰지 않는다. 원격 AI 응답을 기다리며 DB 트랜잭션을 열어 두지 않는다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `transaction(command)` | 하나의 저장 명령 | 커밋된 결과 또는 롤백 | 예외 시 전체 롤백. 연결은 항상 닫는다. |
| `loadSession(id)` | 세션 ID | 세션 snapshot·revision | 없는 세션은 없음 오류. 조회 자체가 권한을 뜻하지 않는다. |
| `appendEvent(event, idempotencyKey)` | 세션 귀속 이벤트·고유 키 | 신규/기존 이벤트와 저장 ACK | 같은 키는 한 건. 다른 내용의 같은 키는 충돌. |
| `savePrivateSnapshot(actor, snapshot)` | 사람이 확정한 메모·사전 점수 | 불변 확정 snapshot | expectedRevision 불일치 거부. |
| `publishBoth(expectedRevision)` | 두 평가자 확정 상태·revision | 단일 공개 revision | 하나라도 미확정이면 거부. 동시 요청도 공개 한 번. |
| `storeBlobMetadata(metadata)` | 서버 확인 hash·기간·소유자·파일 참조 | 저장된 미디어 메타데이터 | 바이트와 메타데이터 불일치면 거부. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```python
class SessionRepository:
    """역할: SQLite 저장·원자적 공개·이벤트 멱등성을 담당하는 유일한 저장 접근 창구다. 상태 소유권과 의존은 본 명세를 따른다."""
    # transaction(command)
    # 입력: 하나의 저장 명령 출력: 커밋된 결과 또는 롤백
    # 실패·부작용: 예외 시 전체 롤백. 연결은 항상 닫는다.
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

- [검증 문서](Verification/T002-SessionRepository.verification.md)
- [진행 Checklist](Checklist/T002-SessionRepository.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Python 3.11 SQLite](https://docs.python.org/3.11/library/sqlite3.html), [SQLite transaction](https://www.sqlite.org/lang_transaction.html), [SQLite 충돌 처리](https://www.sqlite.org/lang_conflict.html). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
