# T016 · AndroidSyncClient

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `AndroidSyncClient` (Kotlin). 부모: 없음 (합성).
- 역할: 세션 서버와 동기화하고 앱 전용 대기열·미디어 anchor·멱등 재전송을 관리한다.
- 연결 기능: F01, F02, F03, F05, F09.
- 생성 예정 파일: `android/app/src/main/java/ai/secondlook/data/AndroidSyncClient.kt`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: [T015 SecondLookApi](T015-SecondLookApi.md)
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

한연결은한서버actor/device에매핑한다. 로컬대기·원자저장·서버확인상태를분리한다. 재시작해도대기열을보존한다. 큐는 원래 anchor·client/server boot epoch 또는 확정 mediaMs를 보존한다. 기기/서버 재시작으로 epoch가 달라지면 낡은 시각축을 섞지 않고 재동기화한다. 외부AI비밀키를Android에두지않는다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `joinSession(invite, personToken)` | 초대정보·해당actor token | 본인세션scope | 다른역할자동전환금지. |
| `syncClock()` | 서버재생anchor·RTT샘플 | offset·uncertainty·anchor version | 벽시계변경의영향없이monotonic사용. |
| `queueBookmark(inputEvent)` | SDK/폰입력이벤트 | LOCAL_PENDING후SERVER_CONFIRMED | 앱전용파일원자저장후전송·eventId유지. |
| `uploadMemo(bookmarkId, file)` | 본인북마크·완료clip | memoId·전사상태 | 실패시파일·북마크보존. |
| `observeSession(afterRevision)` | 마지막수신revision | scope내새이벤트/snapshot | 끊김·순서역전을복구. |
| `flushPending()` | 저장된미전송이벤트 | 멱등재전송결과 | 동일ID재사용·중복구독금지. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```kotlin
/** 역할: 세션 서버와 동기화하고 앱 전용 대기열·미디어 anchor·멱등 재전송을 관리한다. 상태·스레드·의존 계약은 본 명세를 따른다. */
class AndroidSyncClient {
    /** 입력: 초대정보·해당actor token 출력: 본인세션scope 실패·부작용: 다른역할자동전환금지. */
    // joinSession(invite, personToken): 아래 메서드 계약에 맞는 타입 별칭/라이브러리 타입으로 구현한다.
}
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

- [검증 문서](Verification/T016-AndroidSyncClient.verification.md)
- [진행 Checklist](Checklist/T016-AndroidSyncClient.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Android SystemClock](https://developer.android.com/reference/android/os/SystemClock), [Android 네트워크 보안 설정](https://developer.android.com/privacy-and-security/security-config). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
