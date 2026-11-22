# T012 · AudioMemoService

> 상태: 전체 구성 승인 대기 · 미구현 · 실행 미검증. 이 문서는 지금 코드를 실행하라는 요청이 아니다.

## 범위와 책임

- 단일 프로덕션 클래스: `AudioMemoService` (Python). 부모: 없음 (합성).
- 역할: 30초 음성 메모의 업로드·원음 보존·전사 초안·사람 확인 과정을 관리한다.
- 연결 기능: F03.
- 생성 예정 파일: `server/second_look/audio_memo_service.py`. 현재 파일 생성은 하지 않는다.
- 해당 클래스의 단위 테스트·fixture·JSON Schema·리소스·설정은 부속 산출물로 허용한다. 다른 직접 작성 프로덕션 클래스를 같은 TASK에 추가하지 않는다.
- 기존 `second-look/` 시안과 사용자 원본은 보존한다. 의존 클래스가 미완료이면 명시적 mock/계약으로 검증하며 완료처럼 표시하지 않는다.

## 실행 전 조건과 선행 결과

- 전체 구성과 이 TASK를 포함한 실행 범위가 승인돼야 한다. 포괄 승인은 유효하며 승인 범위의 반복 확인은 요구하지 않는다.
- 담당 전문 서브에이전트가 아래 근거의 현재 지원 상태를 확인하고 출처·적용·한계를 보고한다.
- 선행 TASK: [T001 SessionPolicy](T001-SessionPolicy.md), [T002 SessionRepository](T002-SessionRepository.md), [T007 ModelGateway](T007-ModelGateway.md)
- 선행 결과는 통과한 검증 기록과 고정 입력·출력 계약으로 인계한다. 선행 API를 임의 변경하지 않는다.

## 설계와 상태 소유권

raw clip·전사 초안·사람 확정 텍스트를 별도로 보존한다. Android가 보낸 duration/MIME을 그대로 신뢰하지 않고 파일과 메타데이터를 검증한다. STT 실패는 북마크를 지우지 않는다.

| 메서드 | 입력 | 출력 | 실패·부작용·주석에 포함할 계약 |
| --- | --- | --- | --- |
| `acceptClip(actor, bookmarkId, upload)` | 인증 actor·본인북마크·clip | 메모 ID·원음 참조·상태 | 소유자·phase·동의·크기·형식 검증. |
| `validateDurationAndHash(clip)` | 업로드 실제 바이트·메타데이터 | 검증된 duration/hash/MIME | 빈파일·30000ms초과·위장MIME 거부. |
| `transcribeAndPropose(memoId)` | 검증된 clip | 전사 초안과 모델 출처 | 외부동의 확인 후 Gateway 호출. 실패 상태 보존. |
| `confirmTranscript(actor, memoId, editedText)` | 작성자가 검토한 텍스트 | voice_confirmed 텍스트·revision | 원음과초안 덮어쓰지 않음. 확정 후 해석입력에 사용. |

## 클래스·함수 주석 요구

모든 클래스와 공개 함수에 역할·입출력·시간/크기 단위·실패·부작용을 설명하는 docstring/KDoc/JSDoc을 넣는다. 아래는 주석 형식 예시이며 제품 구현 코드가 아니다. 모든 메서드 행의 계약을 해당 함수 주석에 반영한다.

```python
class AudioMemoService:
    """역할: 30초 음성 메모의 업로드·원음 보존·전사 초안·사람 확인 과정을 관리한다. 상태 소유권과 의존은 본 명세를 따른다."""
    # acceptClip(actor, bookmarkId, upload)
    # 입력: 인증 actor·본인북마크·clip 출력: 메모 ID·원음 참조·상태
    # 실패·부작용: 소유자·phase·동의·크기·형식 검증.
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

- [검증 문서](Verification/T012-AudioMemoService.verification.md)
- [진행 Checklist](Checklist/T012-AudioMemoService.checklist.md)
- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- 조사 시작점: [Gemini 전사](https://ai.google.dev/gemini-api/docs/transcribe), [Python SQLite](https://docs.python.org/3.11/library/sqlite3.html). 현재 문서 조사 근거이며 실행 성공이나 대상 기기 지원을 보증하지 않는다.
