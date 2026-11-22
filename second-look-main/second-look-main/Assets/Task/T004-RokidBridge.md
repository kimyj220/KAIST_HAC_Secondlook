# T004 · RokidBridge

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `RokidBridge` (Kotlin). 부모: 없음 (합성).
- 역할: 공식 CXR SDK의 연결·capability·실제 지원 입력·표시 접수만 우리 계약으로 정규화한다.
- 연결 기능: F02, F09.
- 생성 예정 파일: `android/app/src/main/java/ai/secondlook/device/RokidBridge.kt`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: 없음. 고정 JSON 계약과 테스트 fixture를 먼저 사용한다.
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

G0 실기기 gate다. 공식 예제/테스트 harness에서 검증하므로 최종 CompanionActivity에 의존하지 않는다. SDK 메서드명·탭 callback을 추정해 구현하지 않는다. SDK 접수와 실제 시야 표시를 구분한다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `inspectCapabilities()` | 기기·펌웨어·Hi Rokid·SDK 버전 | 확인된 viewport·입출력 채널 JSON | 미확인 기능은 unknown. 해상도를 하드코딩하지 않는다. |
| `connect(authorizedSession)` | 공식 권한 절차를 거친 연결 정보 | 연결 상태 Flow | 취소·권한 거부·앱 부재를 별도 상태로 반환. |
| `observeInput()` | 실제로 지원되는 SDK callback | eventId·type·receivedMonoMs·source·uncertainty | SDK 시각 유무를 명시. 중복 구독 방지. |
| `sendLayout(layout, revision)` | 확인된 canvas에 맞는 layout·revision | SDK 접수 결과 | 지원 안 되는 layout은 거부. 렌더 완료로 오표시 금지. |
| `disconnect()` | 현재 연결 | 구독·리소스 해제 결과 | 여러 번 호출해도 안전. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```kotlin
/** 역할: 공식 CXR SDK의 연결·capability·실제 지원 입력·표시 접수만 우리 계약으로 정규화한다. 상태·스레드·의존 계약은 본 명세를 따른다. */
class RokidBridge {
    /** 입력: 기기·펌웨어·Hi Rokid·SDK 버전 출력: 확인된 viewport·입출력 채널 JSON 실패·부작용: 미확인 기능은 unknown. 해상도를 하드코딩하지 않는다. */
    // inspectCapabilities(): 아래 메서드 계약에 맞는 타입 별칭/라이브러리 타입으로 구현한다.
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

- [검증 문서](Verification/T004-RokidBridge.verification.md)
- [진행 Checklist](Checklist/T004-RokidBridge.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Rokid 한국 개발자 안내](https://kr.rokid.com/43), [Android 공식 아키텍처](https://developer.android.com/topic/architecture). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
