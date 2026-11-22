# 004 · GitHub 비공개 저장소 생성 및 현재 스냅샷 업로드

- 담당: `github_private_publish`; 독립 검증은 별도 검토자가 수행한다.
- 범위: 현재 기획·기술 명세·TASK·프로토타입을 개인 GitHub 비공개 저장소로 공유한다. 제품 구현과 친구 초대는 수행하지 않는다.
- 승인 근거: 사용자의 비공개 업로드 요청과 후속 “깃허브 먼저 경로 줘” 요청.
- 저장소: https://github.com/kimyj220/second-look
- 상태: 비공개 저장소에 현재 스냅샷 업로드 완료. 완료 상태 기록도 후속 정상 커밋으로 반영한다.

## Checklist

- [x] AGENTS와 선행 사전 점검, GitHub 공식 생성 지침을 확인했다.
- [x] 텍스트 파일의 자격증명 패턴을 값 노출 없이 점검했다. 탐지 0건이며 완전한 비밀 검출을 보증하지 않는다.
- [x] 로그인 계정 `kimyj220`과 신규 이름 `second-look`의 사용 가능 상태를 확인했다.
- [x] 비공개를 명시해 원격 저장소를 생성하고 실제 `Private` 배지를 확인했다.
- [x] 로컬 DB·캐시·비밀 파일 제외 규칙과 저장소 읽기 순서를 준비했다.
- [x] 추적 대상과 제외 대상이 의도대로 구분되는지 독립 검토했다.
- [x] 로컬 Git 저장소에 현재 스냅샷을 커밋했다.
- [x] 비공개 원격에 업로드하고 파일·브랜치 결과를 확인했다.
- [x] 최종 저장소 URL, 공개 범위와 업로드 결과를 오케스트레이터에게 전달했다.

## 관측 근거

- 2026-11-16: GitHub 플러그인은 미연결 상태였다. 기존 Chrome 상태 읽기는 최소화된 창 때문에 실패했다. 별도 in-app GitHub 로그인 화면을 확인했고 사용자 로그인 후 동일 세션에서 저장소 생성 양식으로 이동했다.
- 생성 양식의 `Choose visibility: Private`와 생성 후 `kimyj220/second-look` 제목 옆 `Private`를 확인했다. 빈 저장소의 URL이 실제 표시됐다.
- 기존 제품 코드와 기획 파일은 수정하지 않았다. 저장소용 `.gitignore`와 루트 README, 이 체크리스트만 추가했다.
- 친구 초대는 사용자 수행 예정으로 남긴다.
- 초기 로컬 커밋은 `c8d166a`이며 76개 파일을 포함한다. 일반 HTTPS push는 Git Credential Manager의 인증 부재로 중단됐고, 브라우저 로그인과 Git 인증이 별개임을 확인했다. 공식 GCM 기기 인증을 사용자가 직접 승인한 뒤 helper가 종료 코드 0으로 완료됐으며, 토큰·비밀번호는 읽거나 출력하지 않았다.
- 최초 push 후 로컬 HEAD와 원격 `refs/heads/main`이 모두 `c8d166af1e6705ab4d8d7e81186ad2b4bab5679c`임을 확인했다. 이후 GitHub 웹 화면에서도 `Private` 배지, `main`, `Assets/`, `second-look/`, README와 원본 파일이 실제 표시됐다. CUA 완료 요약을 반환했다.
- `github_preflight_review`도 인증된 Git 읽기로 원격 `HEAD`·`main`과 로컬 초기 커밋의 일치, 76개 파일 구조, DB·캐시 제외를 독립 확인했다. 최종 상태 기록 커밋 후 HEAD 일치 여부를 한 번 더 확인하며 제품 TASK의 구현·실행 상태는 변경하지 않는다.
- `github_preflight_review`가 stage와 로컬 커밋 `c8d166a`의 tree 76개 파일을 읽기 전용으로 확인했다. 추적된 DB·SQLite·캐시·`.env`·키 파일 경로는 0개이고, T001~T019 제품 Checklist의 완료 체크는 0개다. 원본 기획 자료와 제품 코드·TASK 경로가 포함돼 있다.
- 최초 독립 로컬 검토 당시에는 IAB 초기화가 `os error 3`으로 실패했고 게시 담당의 업로드도 아직 미완료였다. 이후 원격 revision·파일 구조는 독립 Git 읽기로 검증했다. `Private` 배지는 게시 담당이 웹에서 직접 확인했으며 독립 UI 검증은 수행하지 못했다. 독립 검토자는 인증 추가·커밋·푸시·초대를 수행하지 않았다.

## 참고

- [GitHub 공식 새 저장소 생성](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository): 신규 개인 저장소·비공개 선택과 기존 소스 업로드 시 원격 초기화 파일을 추가하지 않는 절차에 적용했다.
- [GitHub 공식 파일 제외](https://docs.github.com/en/get-started/git-basics/ignoring-files): 추적 전에 로컬 DB·키·캐시를 제외하는 데 적용했다.
