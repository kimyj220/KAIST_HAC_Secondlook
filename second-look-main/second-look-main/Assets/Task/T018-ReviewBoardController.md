# T018 · ReviewBoardController

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `ReviewBoardController` (JavaScript). 부모: 없음 (합성).
- 역할: 개인 기록·공동 비교·관점 그래프·근거 확인·공동 기록을 웹 UI로 제공한다.
- 연결 기능: F03–F11 웹.
- 생성 예정 파일: `web/src/ReviewBoardController.js`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: [T015 SecondLookApi](T015-SecondLookApi.md)
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

서버권한을DOM숨김으로대체하지않는다. 간단SVG와같은관계의접근가능목록을함께쓴다. AI제안·사람검토·미검증·live/cache/prepared라벨을유지한다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `renderPrivate(snapshot)` | 본인scope관점·사전점수 | 개인기록화면 | 미공개상대자료를요청/보관하지않음. |
| `renderComparison(projection)` | 공개된두관점·차이유형 | 나란한비교·단독포착우선 | 서로다른해석을평균요약X. |
| `renderPerspectiveGraph(graph)` | 4노드유형·관계·검토상태 | SVG와동등연결목록 | 깨진ID/미검증관계를확정표현X. |
| `jumpToEvidence(id)` | 현재전사ID | 원문·재생구간이동 | 없는/타세션ID는오류. |
| `submitProposalReview(action)` | 수락/수정/거절·이유 | 서버확인된검토상태 | 낙관표시와영속화완료구분. |
| `renderFourColumns(record)` | 4칸기록·변화 | 입력/저장상태화면 | 원사전판단보존. |
| `renderHandoff(questions)` | 열림/해소/이관질문 | 후속확인화면 | 미해결차이숨김X. |
| `exportReview()` | 최신입력과서버확인기록 | 상태·출처·이견보존내보내기 | 저장중최신값누락여부검증. |
| `controlPlayback(command)` | 진행자 재생/정지/seek 의도 | 서버확인 anchor와 로컬 미디어 재생 | 브라우저의 벽시계를 권위로 삼지 않는다. 미승인 anchor 상태를 표시한다. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```javascript
/** 역할: 개인 기록·공동 비교·관점 그래프·근거 확인·공동 기록을 웹 UI로 제공한다. 상태 소유권과 의존은 본 명세를 따른다. */
class ReviewBoardController {
  /** 입력: 본인scope관점·사전점수 출력: 개인기록화면 실패·부작용: 미공개상대자료를요청/보관하지않음. */
  // renderPrivate(snapshot): 구현 시 JSON Schema와 일치하는 JSDoc 타입을 붙인다.
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

- [검증 문서](Verification/T018-ReviewBoardController.verification.md)
- [진행 Checklist](Checklist/T018-ReviewBoardController.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [MDN SVG](https://developer.mozilla.org/en-US/docs/Web/SVG), [HTML 미디어 시각](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime), [Metaview 원문 근거 검토](https://www.metaview.ai/resources/blog/candidate-review-align). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
