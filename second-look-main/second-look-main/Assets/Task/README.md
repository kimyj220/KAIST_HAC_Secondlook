# SECOND LOOK · 클래스 TASK 인덱스

> 전체 구성 승인 대기. 모든 제품 클래스는 미구현·실행 미검증이다. 이번 산출물은 TASK 19개와 대응 검증·Checklist이며 제품 코드가 아니다.

- [전체 구성 검토안](../Docs/SECOND_LOOK_전체구성_검토안.md)
- [이번 문서 작업 Checklist](Checklist/002-planning-spec-breakdown.checklist.md)
- 1 TASK = 직접 작성 프로덕션 클래스 1개. 클래스 테스트·fixture·스키마·리소스·설정은 해당 TASK의 보조 산출물이다.
- DTO·이벤트는 JSON Schema/타입 별칭이며 추가 프로덕션 클래스가 아니다. 새 클래스가 필요하면 전체 목록·의존·승인 범위를 먼저 갱신한다.
- 실행은 아래 순서로 한다. 각 TASK를 구현·검증한 뒤 계약을 다음 TASK로 인계한다. 포괄 승인된 실행 범위는 반복 승인을 요구하지 않는다.
- 실제 돌리지 않은 항목은 미체크/미검증으로 남긴다. mock 테스트를 실기기/API/성능 통과로 대체하지 않는다.

## 구현 순서

| 순서 | 단일 클래스 | 부모 | 선행 결과 | 구현 | 검증 / Checklist |
| --- | --- | --- | --- | --- | --- |
| T001 | [SessionPolicy](T001-SessionPolicy.md) | 없음 (합성) | 없음 | 미구현·승인 대기 | [검증](Verification/T001-SessionPolicy.verification.md) / [Checklist](Checklist/T001-SessionPolicy.checklist.md) |
| T002 | [SessionRepository](T002-SessionRepository.md) | 없음 (합성) | 없음 | 미구현·승인 대기 | [검증](Verification/T002-SessionRepository.verification.md) / [Checklist](Checklist/T002-SessionRepository.checklist.md) |
| T003 | [TranscriptTimeline](T003-TranscriptTimeline.md) | 없음 (합성) | 없음 | 미구현·승인 대기 | [검증](Verification/T003-TranscriptTimeline.verification.md) / [Checklist](Checklist/T003-TranscriptTimeline.checklist.md) |
| T004 | [RokidBridge](T004-RokidBridge.md) | 없음 (합성) | 없음 | 미구현·승인 대기 | [검증](Verification/T004-RokidBridge.verification.md) / [Checklist](Checklist/T004-RokidBridge.checklist.md) |
| T005 | [DifferenceClassifier](T005-DifferenceClassifier.md) | 없음 (합성) | 없음 | 미구현·승인 대기 | [검증](Verification/T005-DifferenceClassifier.verification.md) / [Checklist](Checklist/T005-DifferenceClassifier.checklist.md) |
| T006 | [SuggestionValidator](T006-SuggestionValidator.md) | 없음 (합성) | T003 | 미구현·승인 대기 | [검증](Verification/T006-SuggestionValidator.verification.md) / [Checklist](Checklist/T006-SuggestionValidator.checklist.md) |
| T007 | [ModelGateway](T007-ModelGateway.md) | 없음 (합성) | 없음 | 미구현·승인 대기 | [검증](Verification/T007-ModelGateway.verification.md) / [Checklist](Checklist/T007-ModelGateway.checklist.md) |
| T008 | [AudioMemoRecorder](T008-AudioMemoRecorder.md) | 없음 (합성) | 없음 | 미구현·승인 대기 | [검증](Verification/T008-AudioMemoRecorder.verification.md) / [Checklist](Checklist/T008-AudioMemoRecorder.checklist.md) |
| T009 | [BookmarkService](T009-BookmarkService.md) | 없음 (합성) | T001, T002, T003 | 미구현·승인 대기 | [검증](Verification/T009-BookmarkService.verification.md) / [Checklist](Checklist/T009-BookmarkService.checklist.md) |
| T010 | [PerspectiveService](T010-PerspectiveService.md) | 없음 (합성) | T001, T002 | 미구현·승인 대기 | [검증](Verification/T010-PerspectiveService.verification.md) / [Checklist](Checklist/T010-PerspectiveService.checklist.md) |
| T011 | [ReviewSessionService](T011-ReviewSessionService.md) | 없음 (합성) | T001, T002, T005 | 미구현·승인 대기 | [검증](Verification/T011-ReviewSessionService.verification.md) / [Checklist](Checklist/T011-ReviewSessionService.checklist.md) |
| T012 | [AudioMemoService](T012-AudioMemoService.md) | 없음 (합성) | T001, T002, T007 | 미구현·승인 대기 | [검증](Verification/T012-AudioMemoService.verification.md) / [Checklist](Checklist/T012-AudioMemoService.checklist.md) |
| T013 | [EvidenceSuggestionService](T013-EvidenceSuggestionService.md) | 없음 (합성) | T001, T002, T003, T006, T007 | 미구현·승인 대기 | [검증](Verification/T013-EvidenceSuggestionService.verification.md) / [Checklist](Checklist/T013-EvidenceSuggestionService.checklist.md) |
| T014 | [ReviewRecordService](T014-ReviewRecordService.md) | 없음 (합성) | T001, T002, T003 | 미구현·승인 대기 | [검증](Verification/T014-ReviewRecordService.verification.md) / [Checklist](Checklist/T014-ReviewRecordService.checklist.md) |
| T015 | [SecondLookApi](T015-SecondLookApi.md) | 없음 (합성) | T009, T010, T011, T012, T013, T014 | 미구현·승인 대기 | [검증](Verification/T015-SecondLookApi.verification.md) / [Checklist](Checklist/T015-SecondLookApi.checklist.md) |
| T016 | [AndroidSyncClient](T016-AndroidSyncClient.md) | 없음 (합성) | T015 | 미구현·승인 대기 | [검증](Verification/T016-AndroidSyncClient.verification.md) / [Checklist](Checklist/T016-AndroidSyncClient.checklist.md) |
| T017 | [HudPresenter](T017-HudPresenter.md) | 없음 (합성) | T004 | 미구현·승인 대기 | [검증](Verification/T017-HudPresenter.verification.md) / [Checklist](Checklist/T017-HudPresenter.checklist.md) |
| T018 | [ReviewBoardController](T018-ReviewBoardController.md) | 없음 (합성) | T015 | 미구현·승인 대기 | [검증](Verification/T018-ReviewBoardController.verification.md) / [Checklist](Checklist/T018-ReviewBoardController.checklist.md) |
| T019 | [CompanionActivity](T019-CompanionActivity.md) | androidx.activity.ComponentActivity | T004, T008, T016, T017 | 미구현·승인 대기 | [검증](Verification/T019-CompanionActivity.verification.md) / [Checklist](Checklist/T019-CompanionActivity.checklist.md) |

## 초반 gate와 최종 조립

- T004 RokidBridge: 공식 예제/테스트 harness로 SDK 인증·Hi Rokid 버전·viewport·한글·탭·동시 네트워크를 확인한다. 최종 T019 Activity를 선행 요구하지 않는다.
- T015 이후: 앞 서비스의 고정 계약을 API·네트워크·HUD·웹에 연결한다.
- T019 CompanionActivity: 기존 라이브러리와 앞의 네 Android 클래스를 조립한다. 별도 업무 규칙을 넣지 않는다.
- 현재 `second-look/`은 보존한 시안이다. 승인 뒤 새 구조를 구현하되, 이 문서 작성 중 이동·삭제·수정하지 않았다.

## 문서 수와 상태

- 구현 TASK 19개, 대응 검증 문서 19개, 대응 제품 Checklist 19개.
- 운영 규칙 및 이번 문서 작업 Checklist는 별도이며 제품 TASK 개수에 포함하지 않는다.
- TASK ID는 T001–T019, 문서 작업 ID는 002로 구분한다.
