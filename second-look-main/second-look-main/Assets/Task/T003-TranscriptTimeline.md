# T003 · TranscriptTimeline

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `TranscriptTimeline` (Python). 부모: 없음 (합성).
- 역할: 검수 전사와 미디어 시간축을 고정하고 탭을 직전 15초 구간과 발화 ID에 연결한다.
- 연결 기능: F01, F02, F06, F07, F08.
- 생성 예정 파일: `server/second_look/transcript_timeline.py`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: 없음. 고정 JSON 계약과 테스트 fixture를 먼저 사용한다.
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

모든 미디어 시간은 정수 ms다. 북마크 원시 구간과 문장 맥락 인용 범위를 분리한다. 원문 수정은 기존 version 덮어쓰기가 아니라 새 version이다. client/server boot epoch ID를 anchor와 함께 저장한다. 앱·폰·서버 재시작 뒤 새 anchor로 재동기화하며 다른 epoch의 monotonic 값을 빼지 않는다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `importTranscript(media, segments)` | 검수된 미디어·발화 ID·시작/종료 ms | 불변 전사 version | 겹침·누락 ID·잘못된 시각은 명시 오류. |
| `normalizeTap(anchor, clientMono)` | 서버 재생 anchor·클라이언트 monotonic ms | tapMediaMs·uncertaintyMs | seek/pause 후 낡은 anchor나 불확실성 초과는 확정 연결 보류. |
| `windowAt(mediaMs, lookbackMs=15000)` | 정규화된 탭 시각 | [max(0,t-15000), t] | 음수·미디어 끝 초과 입력 거부. |
| `overlappingSegments(startMs, endMs)` | 북마크 구간과 고정 전사 | 중첩 발화 ID 목록 | 경계 규칙은 [start,end)로 고정. |
| `jumpRange(evidenceId)` | 현재 전사 version의 ID | 원문 발화와 재생 구간 | 타 version/없는 ID 거부. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```python
class TranscriptTimeline:
    """역할: 검수 전사와 미디어 시간축을 고정하고 탭을 직전 15초 구간과 발화 ID에 연결한다. 상태 소유권과 의존은 본 명세를 따른다."""
    # importTranscript(media, segments)
    # 입력: 검수된 미디어·발화 ID·시작/종료 ms 출력: 불변 전사 version
    # 실패·부작용: 겹침·누락 ID·잘못된 시각은 명시 오류.
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

- [검증 문서](Verification/T003-TranscriptTimeline.verification.md)
- [진행 Checklist](Checklist/T003-TranscriptTimeline.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Python monotonic clock](https://docs.python.org/3.11/library/time.html#time.monotonic), [Android SystemClock](https://developer.android.com/reference/android/os/SystemClock), [HTML 미디어 시각](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
