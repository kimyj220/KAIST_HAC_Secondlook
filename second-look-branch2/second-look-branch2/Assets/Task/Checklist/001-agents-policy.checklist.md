# 001 · AGENTS.md 운영 규칙 작성

- 범위: 루트 AGENTS.md와 이 체크리스트만 작성한다. 제품 개발·기획 명세·제품 TASK 분리는 진행하지 않는다.
- 담당: 운영 지침 작성 서브에이전트 / 독립 검증 서브에이전트.

## Checklist

- [x] 루트·상위 경로의 기존 AGENTS.md와 Assets/Task 구조 확인: 해당 파일·폴더 없음.
- [x] 사용자 조건 및 승인된 문서 작성 범위 확인.
- [x] 공식 운영 사례 조사: 역할별 위임, 작업별 범위·완료 기준·검증 기록 구조 참고.
- [x] 짧은 수행문 중심의 루트 AGENTS.md 작성 및 작성자 자체 점검: 37줄, 요청 조건 포함 확인.
- [x] 독립 검증자가 사용자 요구 누락·모순·과도한 단정·범위 이탈 확인.
- [x] 검증 결과와 생성 파일을 오케스트레이터에게 전달.

## 참고 근거

- [OpenAI — Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex): 지속 운영 지침은 AGENTS.md에, 작업 범위와 완료·검증 근거는 작업 문서에 두는 구조를 참고했다. 사용자 요청에 맞춰 최소 두 문서만 작성한다.
- [OpenAI — Multi-agent](https://developers.openai.com/api/docs/guides/agents-api/multi-agent): 명확한 질문·산출물을 가진 위임과 같은 파일의 변경 조정을 참고했다. 모든 실무를 서브에이전트로 수행하는 조건은 사용자 요청을 따른다.
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system): 독립 검증자는 목표·산출물·범위가 분명한 전문 역할 분담과 검증 구조를 참고했다.

## 검증 기록

- 작성자: 루트 AGENTS.md 37줄과 대응 체크리스트만 신규 생성했으며, 기존 사용자 파일·제품 코드는 변경하거나 삭제하지 않았다. 역할·기기·TASK·승인·3회 점검 조건을 원 요청과 대조했다.
- 독립 검증: 사용자 조건과 37줄 수행문을 대조해 누락·모순 없음 확인. 승인된 범위의 수행과 기획 변경 승인, 조건을 바꾼 3회 문제 점검, 실기기 지원 미단정이 일관된다. 수정 요청 없음. 제품 기능은 검증·변경하지 않았다.
