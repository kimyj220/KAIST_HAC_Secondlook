# T005 · DifferenceClassifier

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `DifferenceClassifier` (Python). 부모: 없음 (합성).
- 역할: 고정 발화 앵커·기준·극성으로 관점 차이를 규칙 분류하고 단독 포착을 우선한다.
- 연결 기능: F06.
- 생성 예정 파일: `server/second_look/difference_classifier.py`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: 없음. 고정 JSON 계약과 테스트 fixture를 먼저 사용한다.
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

LLM을 호출하지 않는 순수 함수다. 같은 발화 앵커일 때만 비교한다. 한 자료가 복수 유형에 해당하면 모두 보존한다. 시연 기준은 2명이며 3명 확장은 현재 승인 범위가 아니다. 단독 포착 여부는 실제 북마크 coverage로 계산하며 메모 존재 여부로 대체하지 않는다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `pairByEvidenceAnchor(bookmarks, perspectives)` | 실제 북마크 coverage·평가자별 확정 관점 | 같은 evidence anchor의 그룹 | 메모 유무로 북마크 유무를 대신 추정하지 않는다. 다른 세션·version은 비교하지 않는다. |
| `classify(bookmarks, perspectives)` | 앵커별 북마크·criterion·polarity·owner | 차이 유형과 관련 북마크/관점 ID | 긍정/의문을 반대 극성으로 단정하지 않는다. |
| `priorityOrder(groups)` | 유형이 붙은 그룹 | 단독 포착 우선의 안정된 순서 | 동률은 원문 시간·ID로 정렬. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```python
class DifferenceClassifier:
    """역할: 고정 발화 앵커·기준·극성으로 관점 차이를 규칙 분류하고 단독 포착을 우선한다. 상태 소유권과 의존은 본 명세를 따른다."""
    # pairByEvidenceAnchor(bookmarks, perspectives)
    # 입력: 실제 북마크 coverage·평가자별 확정 관점 출력: 같은 evidence anchor의 그룹
    # 실패·부작용: 메모 유무로 북마크 유무를 대신 추정하지 않는다. 다른 세션·version은 비교하지 않는다.
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

- [검증 문서](Verification/T005-DifferenceClassifier.verification.md)
- [진행 Checklist](Checklist/T005-DifferenceClassifier.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Metaview 근거 기반 비교](https://www.metaview.ai/resources/blog/candidate-review-align), [사전 판단 개입 연구](https://www.iis.seas.harvard.edu/papers/2021/bucinca2021trust.shtml). 분류 truth-table 자체는 본 기획에서 정의한 규칙이다. 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
