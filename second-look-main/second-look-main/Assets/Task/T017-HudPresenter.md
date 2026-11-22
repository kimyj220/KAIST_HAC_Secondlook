# T017 · HudPresenter

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `HudPresenter` (Kotlin). 부모: 없음 (합성).
- 역할: 확인된 글래스 표시 영역에 짧은 캡처 상태와 사람이 선택한 검토 질문을 표시한다.
- 연결 기능: F09.
- 생성 예정 파일: `android/app/src/main/java/ai/secondlook/presentation/HudPresenter.kt`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: [T004 RokidBridge](T004-RokidBridge.md)
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

그래프와긴원문은웹에둔다. 한질문·최대2줄은목표이며글자수하드코딩대신실측폰트/줄바꿈으로검증한다. TTL과세션revision으로늦은질문을버린다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `showCaptureState(state)` | localPending/serverConfirmed/error | 상태카드 | 로컬기록을서버저장완료로표시금지. |
| `showQuestion(id, text, sessionRevision, expiresAt)` | 사람선택질문·출처상태·기한 | 현재화면질문 | 구버전/다른세션/만료문장거부. |
| `clear()` | 현재카드 | 화면비움요청 | 연결해제·세션종료시호출. |
| `flush()` | 유효한최신대기카드 | Bridge SDK접수결과 | SDK접수와실표시는별도측정. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```kotlin
/** 역할: 확인된 글래스 표시 영역에 짧은 캡처 상태와 사람이 선택한 검토 질문을 표시한다. 상태·스레드·의존 계약은 본 명세를 따른다. */
class HudPresenter {
    /** 입력: localPending/serverConfirmed/error 출력: 상태카드 실패·부작용: 로컬기록을서버저장완료로표시금지. */
    // showCaptureState(state): 아래 메서드 계약에 맞는 타입 별칭/라이브러리 타입으로 구현한다.
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

- [검증 문서](Verification/T017-HudPresenter.verification.md)
- [진행 Checklist](Checklist/T017-HudPresenter.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Rokid 한국 개발자 안내](https://kr.rokid.com/43), [Android 공식 아키텍처](https://developer.android.com/topic/architecture). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
