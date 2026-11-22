# 003 · GitHub 비공개 공유 사전 점검

- 상태: 사전 점검 완료, 실제 업로드 대기.
- 담당: `github_private_preflight` 서브에이전트. 오케스트레이터가 사용자 결과 대화를 담당한다.
- 범위: 공식 절차와 로컬 Git 준비 상태를 읽기 전용으로 확인한다. 이 체크리스트만 새로 작성한다.
- 완료 기준: 현재 상태·제외 후보·후속 조건을 보고한다. 원격 저장소 생성·커밋·푸시·초대·로그인 변경은 수행하지 않는다.
- 사용자 의도: 이번 작업 마무리 후 비공개 저장소에 공유한다. 친구 1명 초대는 사용자가 할 예정이며, 에이전트가 초대하려면 추후 명시적 지시가 필요하다.

## Checklist

- [x] AGENTS.md와 이번 요청 범위를 읽었다.
- [x] GitHub 공식 비공개 저장소 생성·협업 초대·제외 파일 문서를 확인했다.
- [x] 로컬 Git 저장소·도구·파일 경로를 읽기 전용으로 점검했다.
- [x] 제외 후보와 미확인 인증 상태를 구분해 기록했다.
- [x] 독립 검토자가 사전 점검 결과와 체크 상태를 확인했다.
- [ ] 이번 작업 마무리 후 업로드 범위·소유 계정·저장소 이름을 확정했다.
- [ ] 비공개 원격 저장소를 생성하고 실제 공개 범위를 확인했다.
- [ ] 검토한 파일을 커밋·푸시하고 원격 결과를 확인했다.
- [ ] 친구 1명 초대는 사용자가 수행했다. 에이전트 수행 시 별도 명시적 지시와 대상 확인이 필요하다.

## 관측 결과 · 2026-11-16

- 루트는 현재 Git 저장소가 아니다. `git rev-parse` 결과와 루트 `.git` 부재를 교차 확인했다. 따라서 현재 프로젝트 remote도 없다.
- Git CLI는 PATH에 있다. GitHub CLI `gh`는 PATH와 표준 설치 경로에서 확인되지 않았다. 전역 미설치를 단정하지 않으며, `gh auth status`는 실행하지 못했다.
- GitHub 로그인·연결 계정·스코프는 미확인이다. 토큰이나 자격증명을 읽거나 출력하지 않았다.
- 루트 `.gitignore`가 없다. 생성·수정하지 않았다.
- 파일 경로 목록에서 `.env`·키·토큰 이름의 파일이나 녹음 파일은 발견하지 못했다. 이는 파일명 점검이며, 비밀 내용 전체 스캔 완료를 뜻하지 않는다.
- 업로드 제외 권고 후보: `second-look/second-look.db`, `second-look/__pycache__/`, `*.pyc`, 추후 생성될 `.env`·자격증명·실제 녹음/개인 데이터. 파일은 삭제하지 않았다.
- 공유 범위 확인 후보: 루트 `second_look.docx`, `SECOND_LOOK_최종.pdf`, `스크린샷 2026-11-16 154645.png`. 사용자 원본이므로 제외를 임의 확정하지 않았다.
- 저장소 이름 제안은 `second-look`이며 확정값은 아니다. 비공개 생성·첫 푸시·접근자 확인은 후속 실행 때 수행한다.
- 기존 제품 코드·기획·T001~T019 문서는 변경하지 않았다. 원격 작업과 로그인 변경은 0건이다.

## 참고 자료와 적용

- [GitHub · 새 저장소 생성](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository): 생성 시 소유 계정과 `private` 가시성을 선택한다. 이번에는 생성하지 않았다.
- [GitHub · 파일 제외](https://docs.github.com/en/get-started/git-basics/ignoring-files): 추적 전 공유할 `.gitignore`를 검토한다. 비공개 저장소 여부와 비밀 파일 제외는 별개다.
- [GitHub · 개인 저장소 협업자 초대](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository): 저장소 소유자가 지정한 사용자를 초대하며 상대의 수락 후 접근한다. 이번 초대는 사용자 수행 예정으로 남긴다.

## 다음 실행 조건

이번 작업 마무리 시 소유 계정 연결 상태와 공유 범위를 확인하고, 제외 규칙을 먼저 준비한다. 그 뒤 비공개 저장소 생성·커밋·푸시를 진행한다. 친구 계정을 지금 묻거나 초대하지 않는다.

## 독립 검토

- `github_preflight_review`가 루트 `.git`·`.gitignore` 부재, Git PATH 존재·`gh` PATH 미확인, 로컬 DB·캐시 경로 존재를 읽기 전용으로 재확인했다. 인증 상태는 확인하지 않았고 로그아웃으로 단정하지 않았다.
- 실제 업로드·초대 항목은 미체크이며, 원본 파일의 제외를 확정하지 않았다. 이번 검토에서 변경한 내용은 독립 검토 행과 이 근거 기록뿐이다.
- [GitHub 공식 저장소 시작 안내](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories)와 [파일 제외 안내](https://docs.github.com/en/get-started/git-basics/ignoring-files)를 직접 확인했다. 생성 시 가시성 선택과 커밋 전 제외 규칙 검토에 적용하며, 실제 원격 접근 권한·인증·비밀 내용 검증을 대신하지 않는다.
