# SECOND LOOK · 전체 구성 검토안

> 브랜치2의 최신 면접 흐름과 AI·AR·보관 범위는 [면접 지원 기능 명세](SECOND_LOOK_면접지원_기능명세.md)에 정리했다. 아래는 초기 설계와 클래스 계약을 보존한 기술 참고 문서다.

> 상태: 기획·기술·TASK 문서 초안. 전체 구성 승인 대기. 제품 구현과 실행 검증은 하지 않았다.
>
> 읽는 순서: 1–4 기획 → 5 기기·구조·상세 기술 명세 → 6 TASK 순서 → 7 승인할 결정.

## 전체 구성 한눈에 보기

설계 권고는 **Android는 글래스 연결·입력·HUD, 현장 PC는 세션·동기화·보드, 외부 AI API는 근거 제안·짧은 전사**를 맡기는 방식이다. 서버 중심 추론이므로 S25를 AI 전용 실행기로 요구하지 않는다.

~~~mermaid
flowchart LR
  G["Rokid Glasses Display"] <--> H["Hi Rokid + CXR-L"]
  H <--> A["우리 Android 앱"]
  A <--> S["현장 PC: 세션/API/저장"]
  W["웹 보드: 원문·관점 그래프"] <--> S
  S <--> M["별도 AI API"]
~~~

연결 경로는 공식 자료 기반 권고이며 SDK 권한·탭 callback·한국어 표시·동시 네트워크는 G0 실기기 gate다. 장비와 스펙은 5.1, 전체 TASK는 [순서표](../Task/README.md)에서 확인한다.

| 승인할 결정 | 기본 권고 / 남은 선택 |
| --- | --- |
| D1 전체 범위 | 기존 핵심 경험을 19클래스·19TASK로 나누는 이 검토안을 승인할지 |
| D2 서버·AI 위치 | 현장 PC 세션 서버 + 별도 AI API를 기본으로 할지. 원격/로컬 GPU 대안은 같은 평가 set으로 비교 |
| D3 Android·연결 경로 | Galaxy S25 등 Android 폰 + Hi Rokid/CXR-L을 우선 검증할지. G0 실패 시 대안은 다시 승인 |
| D4 글래스 수량·시연 | 실제 확보 대수. 2평가자 동시 캡처는 각자 독립 연결이 필요하며 1대 교대 시연은 이를 제한적으로 보여준다는 점 수용 여부 |
| D5 공통 기준·사전 점수 | 3개 기준과 점수 척도/앵커 확정. 척도는 아직 임의 고정하지 않음 |
| D6 음성 메모 범위 | 원기획의 사후 최대30초 폰 음성 메모·전사·사람 확인을 포함할지. 초기 텍스트 대안 시연은 별도 승인 |

기획 기능을 새로 추가해 자동 TASK로 만든 항목은 없다. 여기서 승인하는 것은 구성과 범위이며, 제품 TASK 실행은 승인된 실행 범위 안에서 요청에 따라 진행한다.

## 1. 프로젝트명과 목적

**SECOND LOOK — 같은 면접, 서로 다른 시선**

동의받은 모의 면접을 함께 본 두 평가자의 선택적 관찰을 보존한다. 각자의 해석을 원문과 공통 기준에 연결한다. 사후 1:1 대면 대화에서 근거를 확인하고 남은 질문을 다음 면접으로 넘긴다.

### 문서의 판단 구분

| 표시 | 의미 |
| --- | --- |
| 기획 기준 | 사용자 콘텐츠 기획서·`second_look.docx`에서 유지한 핵심 경험 |
| 설계 제안 | 그 경험을 구현하기 위한 기술·구조·검증 초안. 전체 컨펌 대상 |
| 승인 필요 | 기기 미정·시연 우선순위·척도 등 사용자가 결정할 항목 |
| 미검증 | 코드 실행·API 실호출·성능 측정·실기기 연결을 하지 않은 상태 |

## 2. 콘텐츠 개요와 범위

- 대상: 학생 평가자, 모의 면접관 교육 참가자.
- 기본 시연: 평가자 A·B 2명, 고정 기준 3개, 3문항·약 5분의 대본 면접 1편.
- 핵심 대화: 면접 이후 A·B의 1:1 검토 회의.
- 입력: 동의받은 방 마이크의 녹음 또는 사전 녹음 자료. 글래스 카메라는 사용하지 않는다.
- 기본 데이터: 사전 검수한 발화·질문·시간 정보. 실시간 면접 전사는 후속 검증 범위로 구분한다.
- 결과: Perspective Graph와 공통 사실·서로 다른 해석·열린 질문·변경 사항의 공동 기록.
- 제외: 자동 합격 판정, 후보 순위, 표정·목소리·외모에 따른 성격·정직성 추정, 3D 홀로그램.
- 기존 웹 코드는 개념 시안으로 보존한다. 본 문서는 현재 코드가 완성됐다는 뜻이 아니다.

## 3. 핵심 컨셉

### 3.1 한 문장

**같은 면접에서 각자가 포착한 순간을 원문에 연결하고, 서로 다른 시선을 다음 질문으로 이어가는 AI·AR 공동 검토 도구.**

### 3.2 경험 원칙

| 원칙 | 구현에서 지킬 것 |
| --- | --- |
| 판단보다 관점 보존 | A·B의 기록과 사전 판단을 별도로 유지한다. AI가 점수나 합의안을 작성하지 않는다. |
| 먼저 기록, 나중에 공개 | 개인 메모·사전 점수·이유를 확정한 뒤에만 공동 공개한다. 서버가 이를 강제한다. |
| 원문과 해석 구분 | 발화 원문, 평가자 해석, AI 제안에 다른 유형·출처를 표시한다. |
| 차이는 검토할 대상 | 기준 차이·해석 충돌·단독 포착을 분리한다. 차이를 오류로 취급하지 않는다. |
| 대칭적 근거 검토 | 지지 근거와 반대·한계 근거를 같은 구조로 보여준다. 없으면 `찾지 못함`을 표시한다. |
| 사람이 연결을 확정 | AI 관계는 제안 상태로 시작한다. 사람이 수락·수정·거절한다. |
| 대면 대화 유지 | HUD에는 짧은 상태·질문을, 웹 보드에는 원문과 전체 관계를 보여준다. |
| 미해결도 결과 | 해소되지 않은 해석과 질문을 지우지 않고 이관한다. |

### 3.3 Perspective Graph의 최소 표현

| 노드 | 필수 속성 | 수정 원칙 |
| --- | --- | --- |
| Evidence | 발화 ID, 면접/전사 버전, 화자, 원문, 시작·종료 미디어 시간, 질문 ID | 사용한 원문 버전은 불변. 정정은 새 버전으로 구분한다. |
| Criterion | 기준 ID, 이름, 설명, 사전 점수 척도/앵커 버전 | 세션 시작 전에 고정. LLM이 추가·변경하지 않는다. |
| Interpretation | 평가자 ID, 발화 ID, 기준 ID, 극성, 사람 확인 메모, 생성 시점 | 공개 전 본인 편집. 확정본 보존 후 사후 변화는 별도 기록한다. |
| Question | 질문 ID, 문장, 관련 노드 ID, 소유 세션, 열림/해소/이관 상태 | 해소 근거·사람 확인과 함께 상태를 변경한다. |

연결은 `원문→해석`, `해석→기준`, `해석↔해석`, `근거→질문`으로 표현한다. AI 제안 여부, 발화 인용 ID, 사람 검토 상태를 연결에 붙인다. 그래프는 간단한 노드·연결 UI로 구현하고, 같은 관계를 읽을 수 있는 목록도 제공한다. 새로운 대규모 시각화 엔진은 전제하지 않는다.

### 3.4 성공으로 볼 수 있는 행동

- 상대만 포착한 순간을 원문에서 확인한다.
- 같은 발화를 다르게 본 기준을 설명한다.
- 자신의 해석에 불리한 발화도 검토한다.
- AI의 잘못된 연결을 거절할 수 있다.
- 생각을 유지·수정한 이유와 남은 질문을 기록한다.
- 평가자 점수의 일치나 상승만으로 성공을 판정하지 않는다.

## 4. 핵심 메커니즘

### 4.1 전체 상태 흐름

`준비 → 면접 캡처 → 개인 정리 → 개인 확정 → 공동 공개 → 근거 검토 → 공동 기록 → 질문 이관/종료`

연결 끊김·녹음 권한 거절·AI 실패는 별도 실패 상태다. 이를 성공 상태나 저장 완료로 표시하지 않는다. 기록의 로컬 보관과 서버 저장 완료도 구분한다.

### 4.2 기능별 세부 명세

| ID | 기능 | 입력과 동작 | 결과·완료 기준 |
| --- | --- | --- | --- |
| F01 | 세션 준비 | 면접·전사 버전, 참여자, 3개 기준, 기록·AI 전송 동의를 고정한다. | 참여자별 역할과 허용 범위를 조회할 수 있다. 미동의 입력은 시작하지 않는다. |
| F02 | 순간 북마크 | 평가자가 탭하면 해당 미디어 시각 직전 15초를 참조한다. | 평가자·이벤트 ID·구간·연결 상태가 기록된다. 같은 이벤트 재전송은 중복 생성하지 않는다. |
| F03 | 개인 메모 | 면접 후 북마크를 보며 30초 이내 음성 메모를 남긴다. 초안을 확인해 해석·기준·극성을 정한다. | 확정된 사람 텍스트만 관점 노드로 사용한다. 녹음/전사 실패는 명시한다. 입력 우선순위와 텍스트 대안은 승인 항목이다. |
| F04 | 사전 판단·확정 | 상대 기록·AI 제안 공개 전에 기준별 사전 점수와 한 줄 이유를 사람이 작성한다. | 필수 입력을 검증한 뒤 본인 기록을 잠근다. 확정 전 상대 내용을 API로도 받지 않는다. |
| F05 | 공동 공개 | 두 사람이 모두 확정하면 공개 상태를 한 번에 변경한다. | 한 사람만 확정된 동안 다른 사람 기록이 노출되지 않는다. |
| F06 | 차이 분류 | 같은 원문에 달린 관점의 기준·극성을 규칙으로 비교한다. | 기준 차이, 해석 충돌, 단독 포착을 표시한다. 단독 포착부터 확인한다. |
| F07 | 근거 제안 | AI가 원문에서 각 해석을 지지하거나 반대·제한하는 발화 ID와 열린 질문을 제안한다. | 서버가 세션·버전·인용 ID를 검증한다. 결과는 제안으로 표시하고 지지/반대가 없으면 비워 둔다. |
| F08 | 사람 검증 | 원문과 시간을 확인하고 제안된 연결을 수락·수정·거절한다. | 최초 제안과 사람 결정을 구분해 남긴다. AI가 스스로 확정하지 않는다. |
| F09 | HUD 표시 | 캡처 상태 또는 공동 검토 질문 한 줄을 글래스로 보낸다. | 현재 참여자·세션의 최신 정보만 표시한다. 만료·늦은 응답은 버린다. |
| F10 | 공동 기록 | 사실, 해석 차이, 열린 질문, 논의 후 변경을 작성한다. | 원문·관점·연결을 추적할 수 있고 개별 사전 판단이 보존된다. |
| F11 | 질문 이관 | 미해결 질문을 다음 면접 세션/면접관에게 선택적으로 넘긴다. | 이관한 질문과 원 세션 연결을 보존하고 후속 해소 여부를 기록한다. |

### 4.3 차이 분류 규칙

- 같은 발화 + 서로 다른 기준: `기준 차이`.
- 같은 발화 + 같은 기준 + 긍정/부정의 반대 극성: `해석 충돌`.
- 한 평가자만 북마크한 발화: `단독 포착`.
- 긍정/의문은 반대 판단으로 단정하지 않는다. 해석을 나란히 보여준다.
- 여러 관계가 동시에 성립하면 복수 유형을 보존한다.
- 북마크 구간을 발화 ID에 연결하는 규칙은 미디어 시간 중첩으로 고정한다. LLM에 시각이나 발화 ID 생성을 맡기지 않는다.

### 4.4 최소 시연 시나리오

1. A는 같은 답변에서 실험을 통한 문제 해결을, B는 개인 기여의 모호함을 기록한다.
2. 다른 답변에 개인이 수행한 테스트 코드 작성 근거를 둔다.
3. 두 사람은 공개 후 차이와 한 사람만 포착한 순간을 확인한다.
4. 원문을 보고 개인 기여 질문이 해소되는지 판단한다. AI 연결이 틀리면 거절한다.
5. 남은 질문을 이관하고 4칸 공동 기록을 남긴다.

시연용 사전 자료·캐시 사용 여부를 표시한다. 캐시된 결과를 실시간 AI 생성으로 설명하지 않는다.

## 5. 기술 명세

> 아래 플랫폼·기기 조건을 먼저 확인한다. 이어서 항목 목록과 상세 설계 제안을 제시한다. 클래스·함수는 문서 명세이며 현재 생성된 제품 코드가 아니다.

### 5.1 플랫폼·기기·실행 환경

**Android 기반 연동 앱 + 디스플레이형 웨이브가이드 Rokid Glasses**를 기준으로 한다. 비디스플레이 Style이나 영상 출력용 Max 계열을 대상으로 가정하지 않는다.

| 구분 | 확인된 정보 / 공식 표기 | 미확정·검증할 것 |
| --- | --- | --- |
| 사용자 선택 글래스 | Rokid Glasses With Display. 공식 상품 표기: Snapdragon AR1, RAM 2GB, 저장 32GB, 약 49g, 배터리 210mAh, 녹색 양안 Micro-LED 웨이브가이드, 30° FOV, 최대 1,500nits, Bluetooth 5.3·Wi-Fi 6. | 실제 기기 수량, SN, 펌웨어, 앱·SDK 버전, 개발 권한. 상품 표기를 실기기 측정값으로 취급하지 않는다. |
| 글래스 해상도 | 사용자 링크는 480×640을 표기한다. 다른 공식 지역 상품에는 480×400, 한국 개발자 안내에는 앱 캔버스 480×352가 있어 일치하지 않는다. | 패널·앱 viewport 구분을 G0에서 확인한다. 어떤 수치도 앱 canvas 상수로 미리 고정하지 않는다. |
| 글래스 입력 | 기본 제품 기능에 터치바·버튼·음성이 있다. | 우리 SDK 경로에 필요한 탭 callback·마이크 스트림이 노출되는지는 별도 확인한다. |
| Android 후보 폰 | Galaxy S25 기본형. 공식 표기: Snapdragon 8 Elite for Galaxy, RAM 12GB, 국내 저장 256/512GB, 4,000mAh, Wi-Fi 7·Bluetooth 5.4. 출시 OS는 Android 15/One UI 7. | 실제 보유 여부·기종·현재 OS와 Hi Rokid/SDK 호환성. 폰에서 큰 LLM을 실행하는 것은 기본안이 아니다. |
| 현재 사용자 데스크톱 | 작업 환경에 Python 3.11 실행 파일이 있음. | CPU·RAM·GPU·VRAM은 확인하지 못했다. 성능 수치를 추정하지 않는다. |
| 행사장 Samsung PC | 사용자 제공: Intel Core Ultra 계열을 “Ultra i7”로 표현, RAM 16GB, SSD 약 528GB, NVIDIA GPU 모델 불명. | CPU 정확한 모델, 실제 저장 용량, GPU·VRAM, 설치 권한·현장 네트워크. 528GB를 임의로 다른 용량으로 고치지 않는다. |
| 서버·AI 후보 | 현장 PC의 세션/API/SQLite/웹 보드 + 별도 AI API를 기본 권고한다. 원격 서버도 같은 API 계약의 대안이다. | 모델 사용권·API 키·계정 한도·성능 측정. GPU 로컬 추론은 사양과 실측 확보 후 비교한다. |

글래스 수치 출처: [사용자 지정 Rokid 공식 상품](https://global.rokid.com/products/b-h-rokid-glasses-with-display?variant=46066446368947), [Rokid 한국 개발자 안내](https://kr.rokid.com/43). S25 수치 출처: [Samsung 공식 스펙](https://www.samsung.com/sec/smartphones/galaxy-s25/specs/), [Samsung S25 Series 공식 스펙 시트](https://images.samsung.com/is/content/samsung/assets/us/business/mobile/phones/galaxy-s25/02052025/S25_Series_B2B_Spec_Sheet_HRc.pdf).

### 5.2 기술 명세 항목 목록

사용자 요청의 “항목 먼저”와 “개발 가능한 상세”를 함께 검토할 수 있도록 목록을 먼저 두고, 이하에 상세 초안을 둔다.

1. 플랫폼·기기·실행 환경
2. 명세 항목 목록
3. 실행 위치·Hi Rokid·SDK 연결 경로
4. 기술 스택과 단일 클래스 소유권
5. 세션·원문·관점·음성·그래프 데이터 계약
6. 시간 동기화·15초 북마크·멱등성
7. API·인증·원자적 공개
8. AI 응답·근거 검증·캐시
9. 성능·품질·실측 원칙
10. 클래스 구조와 함수 계약
11. G0·기존 시안 한계·미검증 범위

### 5.3 실행 위치와 Hi Rokid 연결 경로

| 역할 | 기본 권고 | 이유와 한계 |
| --- | --- | --- |
| 글래스 | 입력·짧은 HUD 표시 | 무거운 추론과 전체 그래프를 글래스에서 수행하지 않는다. |
| Android 폰 | Rokid 연결 허브, 입력 정규화, 로컬 대기열, HUD 전송, 사후 메모 녹음 | S25는 후보 기기다. 별도의 AI 폰이 필수라는 뜻은 아니다. |
| 현장 PC | 권위 세션 서버, 짧은 DB 트랜잭션, 미디어 anchor, 웹 보드, 캐시 | LAN 지연을 줄이고 현장 복원성을 확보하는 설계 제안이다. |
| AI API | 서버가 별도 키로 근거 제안·짧은 음성 전사를 요청 | 폰/글래스의 기존 AI 서비스 사용권이 개발 API 권한을 뜻하지 않는다. |
| 원격 서버 대안 | 현장 서버와 같은 API | 현장 인터넷 RTT·유실·제한을 측정해야 한다. 서버를 열어도 선택한 SDK의 Android 연결 허브가 자동으로 없어지지는 않는다. |

**기본 연결 권고: Rokid Glasses ↔ Hi Rokid + CXR-L ↔ 우리 Android 앱 ↔ 현장 서버 ↔ AI API.** 공식 연결 문서는 Hi Rokid 안에서 페어링하도록 안내한다. 최소 Android 10, 권장 Android 12 이상이라는 앱 안내와 선택 SDK의 실제 최소 SDK는 별도로 확인한다. [Hi Rokid 앱](https://global.rokid.com/blogs/academy-glasses/2-2), [공식 페어링 안내](https://global.rokid.com/blogs/academy-glasses/2-4-connect-to-your-devices)

| SDK 경로 | Hi Rokid 필요성 | 우리 범위의 판단 |
| --- | --- | --- |
| CXR-L | 공식 안내상 Hi Rokid를 경유해 I/O를 확장한다. | 기본 권고. SDK 권한·해당 기기/펌웨어·표시·입력·폰 네트워크 동시성을 G0에서 확인한다. |
| CXR-M | Android 직접 연결 방식이며 별도 승인 등이 필요하다고 안내한다. Hi Rokid와 동시 사용 불가 조건이 있다. | L 경로가 목적을 충족하지 못할 때 검토할 대안. 지금 둘을 병행 구현하지 않는다. |
| CXR-S | 글래스 독립 앱 및 M과의 양방향 경로로 안내한다. | 현재 기본 범위 아님. 폰 생략·개발 자유도를 이유로 지원을 추정하지 않는다. |

SDK 근거: [Rokid 한국 개발자 안내](https://kr.rokid.com/43), [Rokid 공식 개발자 플랫폼](https://open.rokid.com/?lang=en). CXR-L 상세 웹 문서는 본문 접근이 제한돼 정확한 메서드명·탭 callback·서명/권한을 확정하지 못했다. 설치할 SDK의 공식 샘플과 실기기가 최종 기준이다.

수동 텔레프롬프터 붙여넣기는 SDK 실패 시 가능한 표시 시연 대안이다. 자동 HUD 전송·실제 탭 북마크를 달성한 것으로 체크하지 않는다. [공식 텔레프롬프터](https://global.rokid.com/en-hispano/blogs/academy-glasses/3-1-ai-teleprompter)

### 5.4 기술 스택과 소유권

- 권고: Android Kotlin, Python 3.11 + FastAPI/Uvicorn, SQLite, vanilla HTML/CSS/ES modules + SVG.
- 모두 승인 대기 기술 선택이다. 이번 문서 작업에서 설치·빌드·코드 변경은 하지 않았다.
- 라이브러리 버전은 구현 착수 시 SDK·Python·Android 호환성을 확인해 lock한다. 임의 최신 버전이나 존재를 전제로 고정하지 않는다.
- 서버는 해커톤 규모의 단일 권위 프로세스를 기본으로 한다. 분산 저장·멀티테넌트·배포 자동화는 현재 범위에 넣지 않는다.
- 비동기 프레임워크를 사용해도 동기 네트워크/SQLite I/O가 자동으로 비동기가 되지 않는다. ModelGateway I/O는 async 또는 작업자 격리, DB는 짧은 트랜잭션으로 분리한다.
- **1 TASK = 직접 작성하는 프로덕션 클래스 1개.** 해당 클래스 테스트·fixture·JSON Schema·리소스·설정은 보조 산출물이다. 다른 직접 작성 클래스는 같은 TASK에 추가하지 않는다.
- DTO·enum·event는 JSON Schema와 타입 별칭/JSDoc 계약으로 정의한다. 직접 만든 Pydantic/ORM/베이스 클래스를 목록 밖에서 늘리지 않는다.
- 부모 없는 클래스는 합성을 사용한다. Android 앱 호스트만 ComponentActivity를 상속한다.
- 모든 클래스·공개 함수 주석에 역할·입출력·단위·실패·부작용을 적는다. 파일 소유권은 TASK별로 고정한다.

근거: [FastAPI WebSocket](https://fastapi.tiangolo.com/advanced/websockets/), [Python 3.11 SQLite](https://docs.python.org/3.11/library/sqlite3.html), [Android 앱 아키텍처](https://developer.android.com/topic/architecture), [JSON Schema 검증](https://python-jsonschema.readthedocs.io/en/stable/validate/).

### 5.5 데이터 계약

아래 명칭은 직렬화 계약 이름이다. 별도의 프로덕션 클래스를 뜻하지 않는다. ID는 서버에서 세션 귀속을 검증하며 시간은 명시된 단위로 다룬다.

| 계약 | 필수 내용 |
| --- | --- |
| Session | id, phase, revision, rubricVersion, transcriptVersion, consentFlags, participants, media/playback anchor |
| TranscriptSegment | id, sessionId, mediaId, startMs, endMs, speakerId, verbatimText, source(script_reviewed/asr_reviewed), revision |
| Bookmark | id, eventId, actorId, deviceId, clientMonoMs, serverReceivedMonoMs, clientBootEpochId, serverBootEpochId, mediaAnchorVersion, startMs, endMs, uncertaintyMs, segmentIds, deliveryState |
| Perspective | id, ownerId, bookmarkId, evidenceIds, criterionId, polarity(positive/negative/question), text, revision, source(typed/voice_confirmed) |
| PriorScore | actorId, criterionId, value, scaleVersion, reason, committedAt, revision. 척도는 승인된 설정이다. |
| Proposal | id, snapshotHash, inputRevision, noteIds, supportEvidenceIds, challengeEvidenceIds, question, provider, modelId, promptVersion, mode(live/cache/prepared), status(suggested/accepted/modified/rejected), reviewerId, reviewReason |
| MemoClip | id, actorId, bookmarkId, audioSource(android_mic), durationMs, mimeType, sampleRate, channels, sha256, storageRef, transcriptionDraft, confirmedText, revision |
| Question | id, text, evidenceIds, status(open/resolved/transferred), targetConversationId, resolutionEvidenceIds |
| GraphProjection | nodes(evidence/criterion/interpretation/question), edges(evidence_of/uses_criterion/compares_with/support/challenge/follow_up), proposalStatus, revision |
| FourColumnRecord | facts, differingInterpretations, openQuestions, changes, referencedIds, revision |
| Event | eventId, type, sessionId, revision, actorId, serverMonoMs, payload |

개별 메모 확정 상태와 세션 공개 상태는 별도다. 단계는 consent → capture → private_annotation → committed → review → handoff/closed를 사용한다. 모든 개인 확정이 끝나기 전 공동 조회와 AI 제안은 열리지 않는다. 질문의 transferred는 다음 대화로 넘겼다는 뜻이며 resolved와 다르다.

음성은 원음·전사 초안·사람 확정 텍스트를 구분한다. 30초 제한은 실제 파일 기간으로 재검증한다. 허용 포맷·용량·sample rate는 선택한 녹음기와 STT 모델의 교집합을 실호출로 확인한 후 lock한다. 웹의 초 단위 currentTime을 서버 ms로 바꿀 때 한 번만 명시적으로 변환한다.

원문은 고정 version을 참조한다. 정정이 필요하면 새 version을 만들고 이전 해석·AI snapshot을 조용히 새 원문으로 옮기지 않는다.

### 5.6 시간·북마크·연결 품질

1. 서버가 playbackId, mediaTimeMs, serverMonoMs, rate, playing, anchorRevision을 배포한다.
2. Android가 여러 RTT 샘플로 offset·불확실성을 기록한다. 벽시계 대신 monotonic clock을 사용한다.
3. 원래 탭의 clientMonoMs를 고정 anchor로 미디어 시각에 대응한다. 서버 도착 시각으로 15초를 계산하지 않는다.
4. start=max(0,tapMediaMs−15000), end=tapMediaMs로 선택 구간을 저장한다. 발화 중첩 판정은 [start,end) 규칙을 사용한다.
5. seek/pause/restart는 새 anchor를 만든다. restart는 앱·폰·서버 재시작을 포함한다. anchor와 큐에 client/server boot epoch ID 또는 동등 식별자 및 원 anchor/확정 mediaMs를 보존한다. 서로 다른 epoch의 monotonic 값을 빼지 않고 재동기화한다. 진행자 UI는 서버 확인 anchor로 동기화한다.
6. 불확실성이 승인된 문턱을 넘으면 raw tap은 보존하고 정확한 원문 연결은 보류한다. 수동 재확인 필요 상태를 보여준다.
7. eventId는 재송신해도 유지한다. 같은 eventId의 다른 내용은 충돌로 거부한다.
8. 로컬 표시·로컬 원자 저장·서버 영속화 ACK·SDK 접수·실제 렌즈 표시는 서로 다른 완료 상태다.
9. 단독 포착은 실제 북마크 coverage로 판정한다. 메모 없는 북마크가 있다는 이유로 그 평가자가 순간을 보지 못했다고 추론하지 않는다.

근거: [Python monotonic clock](https://docs.python.org/3.11/library/time.html#time.monotonic), [HTML 미디어 시각과 seek](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime). 기기 간 offset 추정 정확도는 이 자료만으로 보장되지 않으며 실측 gate다.

### 5.7 API·인증·동시 공개

권한은 서버가 토큰에서 얻은 actor에 바인딩한다. 요청 payload의 A/B 또는 ownerId로 권한을 바꾸지 않는다. 개인 조회 API는 공개 전 본인 자료만 반환하고 WebSocket도 같은 scope를 적용한다.

| 대표 API | 책임 |
| --- | --- |
| POST /sessions | 진행자 세션·동의·3기준·미디어/검수 전사 등록 |
| POST /sessions/{id}/join | 1회 역할 nonce → 서버 actor token |
| GET /sessions/{id}/private | 본인 북마크·해석·사전 점수만 |
| POST /sessions/{id}/playback-anchor | 진행자 재생/정지/seek → 새 서버 anchor |
| POST /bookmarks | 멱등 탭 이벤트 저장과 ACK |
| POST /perspectives, PUT /prior-scores/{criterionId} | 개인 해석·사전 점수·이유 |
| POST /commit-private | expectedRevision으로 개인 확정 |
| GET /review, GET /graph | 모두 확정한 뒤 공동 projection |
| POST /memos/upload, POST /memos/{id}/confirm | 원음 업로드·전사 초안·사람 확인 |
| POST /suggestions | 동의와 snapshot을 검증한 AI 요청 |
| PATCH /proposals/{id} | 사람 수락/수정/거절과 이유 |
| PUT /review-record, PATCH /questions/{id} | 공동 기록·질문 이관/해소 |
| WS /events | scope가 적용된 phase·anchor·ACK·HUD·revision 이벤트 |

- 변경 요청: Bearer actorToken, Idempotency-Key, expectedRevision을 사용한다.
- 성공: {requestId, ok:true, sessionId, revision, data, sourceMode?, timings?}.
- 오류: {requestId, ok:false, error:{code,message,retryable}, revision?}.
- 400 형식, 401 미인증, 403 권한/공개 게이트, 409 낡은 revision/단계 충돌, 413 업로드 제한, 429 한도, 503 AI/기기 불가를 구분한다.
- Repository의 원자적 확정/공개로 두 참여자의 마지막 확정 경쟁을 처리한다.
- 외부 호출은 DB 트랜잭션 밖에서 수행한다. 응답 뒤 권한·phase와 의존 입력 inputRevision/hash를 확인한다. 전역 eventRevision과 AI 입력 버전은 구분하고 HUD/ACK/진행상태만 바뀌었다고 유효 응답을 거부하지 않는다.
- 재연결은 afterRevision으로 빠진 이벤트를 보충하거나 현재 snapshot을 받는다.
- LAN 개발 서버도 허용 host/origin을 명시한다. PC의 LAN 주소·baseURL·포트·방화벽과 폰의 동일 LAN 여부를 확인한다. 현재 시안의 127.0.0.1 바인딩은 폰에서 접속할 수 없으며 승인 후 개발 서버 바인딩을 별도로 정해야 한다.
- 기본은 HTTPS/WSS를 사용한다. 현장 개발용 HTTP/WS가 필요한 경우 debug 한정·허용 호스트 한정 네트워크 설정을 G0에서 검증한다. release 전체 cleartext 허용으로 넘기지 않는다. 원격 서버는 HTTPS/WSS를 전제로 한다. 이번에 서버 설정을 바꾸지 않았고 인터넷 공개용 운영 보안 완료도 아니다. [Android 네트워크 보안 설정](https://developer.android.com/privacy-and-security/security-config)

### 5.8 AI 응답·검증·캐시 원칙

**근거 선택 코드와 생성 모델의 역할을 분리한다.** 차이 유형·시간 매핑·ID 검사는 코드가 수행한다. 모델은 고정된 기준과 원문을 바탕으로 1~2개의 지지/반대 근거 연결 및 열린 질문을 제안한다.

- 기본 5분 전사 전체를 한 요청의 작은 context로 사용한다. 질문 밖에 있는 결정 근거도 검토한다.
- 결과는 제한된 JSON Schema를 따른다. 구조화 출력 지원도 값의 정확성을 보장하지 않는다.
- 검증 순서: schema → 같은 session/version의 원문·관점·기준 ID → 서버 원문 발췌 → 사람의 의미 검토.
- 인용문은 모델이 쓴 문장을 사용하지 않고 서버 원문에서 가져온다.
- 지지/반대 근거가 없으면 빈 배열이다. 개수를 맞추려고 근거를 만들지 않는다.
- 답을 모름, 관련 근거 없음, 오류·거절·출력 잘림·시간 초과를 성공 제안과 구분한다.
- 후보 적합성·성격·정직성·합격 여부·자동 점수·새 기준 생성은 출력 계약에 포함하지 않는다.
- AI 제안은 suggested로 시작한다. 사람 검토와 이유가 있어야 accepted/modified/rejected가 된다.
- 완성 JSON의 검증 전에는 토큰 스트림을 확정 그래프·HUD 질문으로 보내지 않는다. 진행 상태만 보여준다.
- 캐시 키에는 session, transcript/rubric version, prompt/model/provider/settings, 사람 메모·판단 hash를 넣는다.
- live/cache/prepared를 화면과 로그에 표시한다. 준비된 응답을 실시간 생성으로 설명하지 않는다.
- 자동 provider 변경은 동일한 전송 동의·권한 조건이 확인된 경우에만 허용한다. 실패 시 원문 보드와 캡처 대기열은 유지한다.
- API 키·계정 권한은 별도 준비 조건이다. 현재 Gemini 기본 모델이 최적이라는 판단은 하지 않는다. 실제 사용할 계정에서 접근·지원·품질·지연을 측정해 modelId와 endpointVersion을 고정한다.

근거: [구조화 출력](https://ai.google.dev/gemini-api/docs/structured-output), [구조 출력의 내용 오류 한계](https://developers.openai.com/api/docs/guides/structured-outputs), [지연 최적화](https://developers.openai.com/api/docs/guides/latency-optimization), [Gemini 전사](https://ai.google.dev/gemini-api/docs/transcribe). 모델별 한국어·파일 포맷·시간표시 지원과 실제 계정 접근성은 미검증이다.

### 5.9 성능·품질 목표와 측정

아래는 모두 **권고 목표·승인 대기·미측정**이다. 상품 성능이나 이미 달성한 결과가 아니다. 품질 문턱을 통과한 후보 중 E2E p95가 낮은 경로를 선택한다.

| 구간 | 권고 목표 | 측정 경계 |
| --- | --- | --- |
| 입력 → 로컬 대기 표시 | p95 ≤100ms | SDK callback 수신부터. 서버 저장 성공을 뜻하지 않는다. |
| 입력 → 로컬 원자 저장 | p95 ≤150ms | 앱 전용 대기열 write 완료 |
| 북마크 → 서버 영속화 ACK | 동일 LAN p95 ≤500ms | 기본은 Android 입력 callback 수신→서버 저장 확인. SDK 원탭 timestamp 지원 여부를 기록하고 물리 탭 E2E는 영상으로 별도 계측 |
| 두 확정 → 공개 보드 | p95 ≤500ms | 서버 마지막 확정부터 두 보드의 공개 revision 표시 |
| HUD 요청 → SDK 접수 | p95 ≤300ms | Presenter 요청부터 SDK 접수. 실제 표시와 별개 |
| HUD 요청 → 실제 시야 표시 | p95 ≤500ms | 영상 등 별도 계측. AI 추론 대기시간은 포함하지 않은 표시 구간 |
| exact cache 제안 | p95 ≤500ms | 캐시 조회·서버 검증·보드 표시 |
| 미캐시 AI 제안 | p50 ≤5s / p95 ≤8s, hard timeout 12s | 요청부터 검증된 제안 표시. 입력과 상태 표시는 차단하지 않는다. |
| 북마크 미디어 정렬 오차 | p95 ≤250ms | 알려진 입력 시점과 매핑 미디어 시점 비교. 불확실성 문턱도 승인 필요 |

| 품질 항목 | 권고 문턱 |
| --- | --- |
| 허구/타 세션 원문 ID, 공개 전 타인 메모 노출 | 0건 |
| 서버 발췌 인용문 | 고정 전사 원문과 100% 일치 |
| 검수 gold 20개 관점 쌍의 근거 정밀도 | ≥90% |
| 심어 둔 결정 근거 재현율 | ≥80% |
| 의견 보존 | 거절·미해결·사전 판단·사후 변화가 export/graph에서 누락되지 않음 |

정밀도의 단위는 사람이 검수한 (noteId, evidenceId, relation=support/challenge) 관계다. 정밀도=방향까지 맞는 제안 관계 수/모델의 전체 제안 관계 수, 결정 근거 재현율=회수한 gold 결정 근거 관계 수/gold 전체 결정 근거 관계 수다. 분모가 0이면 N/A로 두고 abstention·제안 coverage를 별도로 기록한다. gold는 발화와 해석 관계를 사람 검수한 데이터이며 지원자 합격 정답이 아니다.

측정은 폰·PC·펌웨어·앱·SDK·모델·전사·네트워크를 고정한다. cold/warm 상태의 미캐시 요청을 각 30회 권고하고 p50/p95/최댓값·실패율을 기록한다. exact cache hit는 따로 측정한다. 소표본 gold 수치는 해커톤용 탐색 지표이며 실제 채용 성과로 일반화하지 않는다.

### 5.10 클래스 구조와 함수 계약

아래 19개 클래스만 직접 작성하는 기본안을 제안한다. 클래스별 TASK와 검증 문서가 1:1로 대응한다. 실제 제품 클래스 파일은 아직 생성하지 않았다.

| 순서 | 클래스 / 부모 | 역할 | 선행 TASK |
| --- | --- | --- | --- |
| [T001](../Task/T001-SessionPolicy.md) | `SessionPolicy` / 없음 (합성) | 세션·참여자·공개 단계·동의에 따른 접근 권한을 기본 거부 방식으로 판정한다. | 없음 |
| [T002](../Task/T002-SessionRepository.md) | `SessionRepository` / 없음 (합성) | SQLite 저장·원자적 공개·이벤트 멱등성을 담당하는 유일한 저장 접근 창구다. | 없음 |
| [T003](../Task/T003-TranscriptTimeline.md) | `TranscriptTimeline` / 없음 (합성) | 검수 전사와 미디어 시간축을 고정하고 탭을 직전 15초 구간과 발화 ID에 연결한다. | 없음 |
| [T004](../Task/T004-RokidBridge.md) | `RokidBridge` / 없음 (합성) | 공식 CXR SDK의 연결·capability·실제 지원 입력·표시 접수만 우리 계약으로 정규화한다. | 없음 |
| [T005](../Task/T005-DifferenceClassifier.md) | `DifferenceClassifier` / 없음 (합성) | 고정 발화 앵커·기준·극성으로 관점 차이를 규칙 분류하고 단독 포착을 우선한다. | 없음 |
| [T006](../Task/T006-SuggestionValidator.md) | `SuggestionValidator` / 없음 (합성) | AI 제안의 구조·범위·실존 ID를 검증하고 인용문을 서버 원문에서 발췌한다. | T003 |
| [T007](../Task/T007-ModelGateway.md) | `ModelGateway` / 없음 (합성) | 별도 서버 키를 사용하는 외부 텍스트 생성·음성 전사 호출을 제한된 모델 어댑터로 처리한다. | 없음 |
| [T008](../Task/T008-AudioMemoRecorder.md) | `AudioMemoRecorder` / 없음 (합성) | 면접 후 Android 폰 마이크로 본인 북마크에 연결된 최대 30초 음성 메모를 녹음한다. | 없음 |
| [T009](../Task/T009-BookmarkService.md) | `BookmarkService` / 없음 (합성) | 인증된 탭 이벤트를 영속화하고 원래 탭 시각의 15초 구간과 발화 앵커를 보존한다. | T001, T002, T003 |
| [T010](../Task/T010-PerspectiveService.md) | `PerspectiveService` / 없음 (합성) | 개인 해석·질문·사전 점수와 이유를 사람 입력으로 저장하고 공개 전 확정본을 만든다. | T001, T002 |
| [T011](../Task/T011-ReviewSessionService.md) | `ReviewSessionService` / 없음 (합성) | 세션 단계·참여자 가입·원자적 공동 공개와 비교 projection을 관리한다. | T001, T002, T005 |
| [T012](../Task/T012-AudioMemoService.md) | `AudioMemoService` / 없음 (합성) | 30초 음성 메모의 업로드·원음 보존·전사 초안·사람 확인 과정을 관리한다. | T001, T002, T007 |
| [T013](../Task/T013-EvidenceSuggestionService.md) | `EvidenceSuggestionService` / 없음 (합성) | 같은 snapshot의 원문과 관점으로 지지·반대 근거를 한 요청에서 제안받고 검증·캐시한다. | T001, T002, T003, T006, T007 |
| [T014](../Task/T014-ReviewRecordService.md) | `ReviewRecordService` / 없음 (합성) | 사람의 제안 검토·관점 변화·그래프·4칸 기록·질문 이관과 해소 이력을 보존한다. | T001, T002, T003 |
| [T015](../Task/T015-SecondLookApi.md) | `SecondLookApi` / 없음 (합성) | 인증된 HTTP·WebSocket 요청을 스키마 검증해 도메인 서비스로 전달한다. | T009, T010, T011, T012, T013, T014 |
| [T016](../Task/T016-AndroidSyncClient.md) | `AndroidSyncClient` / 없음 (합성) | 세션 서버와 동기화하고 앱 전용 대기열·미디어 anchor·멱등 재전송을 관리한다. | T015 |
| [T017](../Task/T017-HudPresenter.md) | `HudPresenter` / 없음 (합성) | 확인된 글래스 표시 영역에 짧은 캡처 상태와 사람이 선택한 검토 질문을 표시한다. | T004 |
| [T018](../Task/T018-ReviewBoardController.md) | `ReviewBoardController` / 없음 (합성) | 개인 기록·공동 비교·관점 그래프·근거 확인·공동 기록을 웹 UI로 제공한다. | T015 |
| [T019](../Task/T019-CompanionActivity.md) | `CompanionActivity` / androidx.activity.ComponentActivity | Android 앱 진입·런타임 권한·연결과 개인 캡처 화면을 조립하는 최종 호스트다. | T004, T008, T016, T017 |

#### T001 · SessionPolicy

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/session_policy.py`.
- 기능: F01, F04, F05, F07. 선행: 없음.
- 역할·상태: 상태를 변경하지 않는 순수 정책이다. 서버에서 해석한 actor 역할만 신뢰한다. 사용자 payload의 owner/evaluator 값은 권한 근거가 아니다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `requireActor(session, actor)` | 서버 세션과 인증된 actor | 허용 또는 권한 오류 | 다른 세션·만료 토큰이면 거부. 저장 부작용 없음. |
| `canReadPrivate(actor, owner, phase)` | 인증 역할·소유자·단계 | 본인 조회 허용 여부 | 공개 전 타인 자료는 false. 단순 DOM 숨김으로 대체 금지. |
| `requirePhase(phase, allowed)` | 현재 단계와 허용 단계 집합 | 통과 또는 단계 오류 | 불허 전이는 거부. 단계 변경은 서비스가 담당. |
| `requireExternalAiConsent(session)` | 기록·외부 AI 전송 동의 상태 | 호출 허용 또는 동의 오류 | 미동의·철회 상태에서는 전송 거부. |

[TASK](../Task/T001-SessionPolicy.md) · [재현 검증](../Task/Verification/T001-SessionPolicy.verification.md) · [Checklist](../Task/Checklist/T001-SessionPolicy.checklist.md)

#### T002 · SessionRepository

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/session_repository.py`.
- 기능: F01–F11 저장. 선행: 없음.
- 역할·상태: 유일 키와 expectedRevision으로 중복과 동시 수정을 제어한다. 트랜잭션은 짧게 유지한다. UNIQUE 외에 기존 payload를 명시적으로 비교한다. 멱등 처리에 기존 행을 삭제·교체하는 INSERT OR REPLACE를 쓰지 않는다. 원격 AI 응답을 기다리며 DB 트랜잭션을 열어 두지 않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `transaction(command)` | 하나의 저장 명령 | 커밋된 결과 또는 롤백 | 예외 시 전체 롤백. 연결은 항상 닫는다. |
| `loadSession(id)` | 세션 ID | 세션 snapshot·revision | 없는 세션은 없음 오류. 조회 자체가 권한을 뜻하지 않는다. |
| `appendEvent(event, idempotencyKey)` | 세션 귀속 이벤트·고유 키 | 신규/기존 이벤트와 저장 ACK | 같은 키는 한 건. 다른 내용의 같은 키는 충돌. |
| `savePrivateSnapshot(actor, snapshot)` | 사람이 확정한 메모·사전 점수 | 불변 확정 snapshot | expectedRevision 불일치 거부. |
| `publishBoth(expectedRevision)` | 두 평가자 확정 상태·revision | 단일 공개 revision | 하나라도 미확정이면 거부. 동시 요청도 공개 한 번. |
| `storeBlobMetadata(metadata)` | 서버 확인 hash·기간·소유자·파일 참조 | 저장된 미디어 메타데이터 | 바이트와 메타데이터 불일치면 거부. |

[TASK](../Task/T002-SessionRepository.md) · [재현 검증](../Task/Verification/T002-SessionRepository.verification.md) · [Checklist](../Task/Checklist/T002-SessionRepository.checklist.md)

#### T003 · TranscriptTimeline

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/transcript_timeline.py`.
- 기능: F01, F02, F06, F07, F08. 선행: 없음.
- 역할·상태: 모든 미디어 시간은 정수 ms다. 북마크 원시 구간과 문장 맥락 인용 범위를 분리한다. 원문 수정은 기존 version 덮어쓰기가 아니라 새 version이다. client/server boot epoch ID를 기록하고 재시작 뒤 새 anchor로 동기화한다. 다른 epoch의 monotonic 값을 빼지 않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `importTranscript(media, segments)` | 검수된 미디어·발화 ID·시작/종료 ms | 불변 전사 version | 겹침·누락 ID·잘못된 시각은 명시 오류. |
| `normalizeTap(anchor, clientMono)` | 서버 재생 anchor·클라이언트 monotonic ms | tapMediaMs·uncertaintyMs | seek/pause 후 낡은 anchor나 불확실성 초과는 확정 연결 보류. |
| `windowAt(mediaMs, lookbackMs=15000)` | 정규화된 탭 시각 | [max(0,t-15000), t] | 음수·미디어 끝 초과 입력 거부. |
| `overlappingSegments(startMs, endMs)` | 북마크 구간과 고정 전사 | 중첩 발화 ID 목록 | 경계 규칙은 [start,end)로 고정. |
| `jumpRange(evidenceId)` | 현재 전사 version의 ID | 원문 발화와 재생 구간 | 타 version/없는 ID 거부. |

[TASK](../Task/T003-TranscriptTimeline.md) · [재현 검증](../Task/Verification/T003-TranscriptTimeline.verification.md) · [Checklist](../Task/Checklist/T003-TranscriptTimeline.checklist.md)

#### T004 · RokidBridge

- 언어/부모: Kotlin / 없음 (합성). 생성 예정 파일: `android/app/src/main/java/ai/secondlook/device/RokidBridge.kt`.
- 기능: F02, F09. 선행: 없음.
- 역할·상태: G0 실기기 gate다. 공식 예제/테스트 harness에서 검증하므로 최종 CompanionActivity에 의존하지 않는다. SDK 메서드명·탭 callback을 추정해 구현하지 않는다. SDK 접수와 실제 시야 표시를 구분한다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `inspectCapabilities()` | 기기·펌웨어·Hi Rokid·SDK 버전 | 확인된 viewport·입출력 채널 JSON | 미확인 기능은 unknown. 해상도를 하드코딩하지 않는다. |
| `connect(authorizedSession)` | 공식 권한 절차를 거친 연결 정보 | 연결 상태 Flow | 취소·권한 거부·앱 부재를 별도 상태로 반환. |
| `observeInput()` | 실제로 지원되는 SDK callback | eventId·type·receivedMonoMs·source·uncertainty | SDK 시각 유무를 명시. 중복 구독 방지. |
| `sendLayout(layout, revision)` | 확인된 canvas에 맞는 layout·revision | SDK 접수 결과 | 지원 안 되는 layout은 거부. 렌더 완료로 오표시 금지. |
| `disconnect()` | 현재 연결 | 구독·리소스 해제 결과 | 여러 번 호출해도 안전. |

[TASK](../Task/T004-RokidBridge.md) · [재현 검증](../Task/Verification/T004-RokidBridge.verification.md) · [Checklist](../Task/Checklist/T004-RokidBridge.checklist.md)

#### T005 · DifferenceClassifier

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/difference_classifier.py`.
- 기능: F06. 선행: 없음.
- 역할·상태: LLM을 호출하지 않는 순수 함수다. 같은 발화 앵커일 때만 비교한다. 한 자료가 복수 유형에 해당하면 모두 보존한다. 시연 기준은 2명이며 3명 확장은 현재 승인 범위가 아니다. 단독 포착 여부는 실제 북마크 coverage로 계산하며 메모 존재 여부로 대체하지 않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `pairByEvidenceAnchor(bookmarks, perspectives)` | 실제 북마크 coverage·평가자별 확정 관점 | 같은 evidence anchor의 그룹 | 메모 유무로 북마크 유무를 대신 추정하지 않는다. 다른 세션·version은 비교하지 않는다. |
| `classify(bookmarks, perspectives)` | 앵커별 북마크·criterion·polarity·owner | 차이 유형과 관련 북마크/관점 ID | 긍정/의문을 반대 극성으로 단정하지 않는다. |
| `priorityOrder(groups)` | 유형이 붙은 그룹 | 단독 포착 우선의 안정된 순서 | 동률은 원문 시간·ID로 정렬. |

[TASK](../Task/T005-DifferenceClassifier.md) · [재현 검증](../Task/Verification/T005-DifferenceClassifier.verification.md) · [Checklist](../Task/Checklist/T005-DifferenceClassifier.checklist.md)

#### T006 · SuggestionValidator

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/suggestion_validator.py`.
- 기능: F07, F08. 선행: T003.
- 역할·상태: 구조/ID 검증 통과는 관계 의미의 정확성 보증이 아니다. 의미는 gold set과 사람 검토로 따로 측정한다. 검증 실패 제안을 부분 성공처럼 조용히 확정하지 않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `validateSchema(payload)` | 미신뢰 AI JSON | 정규화 제안 또는 구조 오류 | 형·enum·길이·배열 크기·중복 제한 검증. |
| `validateReferences(snapshot, payload)` | 입력 snapshot·원문/기준/관점 ID | 같은 session/version에 속한 제안 | 실존해도 타 세션·낡은 version이면 거부. |
| `normalizeQuotes(timeline, payload)` | 검증된 인용 ID | 서버 발췌 verbatimText | LLM이 만든 인용문은 사용하지 않는다. |

[TASK](../Task/T006-SuggestionValidator.md) · [재현 검증](../Task/Verification/T006-SuggestionValidator.verification.md) · [Checklist](../Task/Checklist/T006-SuggestionValidator.checklist.md)

#### T007 · ModelGateway

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/model_gateway.py`.
- 기능: F03, F07. 선행: 없음.
- 역할·상태: provider/model/endpointVersion/제한은 설정으로 주입한다. 비밀 키를 클라이언트·로그·오류에 내보내지 않는다. 음성 전사와 근거 제안은 모델을 따로 선택할 수 있다. 실호출 전 mock 계약부터 검증한다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `capabilities()` | 구성된 provider·모델 설정 | 구조 출력·전사·포맷 등 확인 상태 | 계정 접근 권한·지원 여부는 실호출 결과로 확정. |
| `generateEvidence(request, deadline)` | 전사·메모 snapshot·마감 시각 | 미신뢰 구조화 응답·사용량·모델 버전 | 12초 hard timeout 제안. 출력 잘림·거절은 실패. |
| `transcribeMemo(clip, mode)` | 검증된 짧은 clip·전사 모드 | 초안 텍스트와 상태 | 요약문을 원문으로 반환하지 않는다. |
| `redactProviderError(error)` | provider 오류 | 비밀 제거한 errorCode·retryable | 429/5xx 재시도는 전체 deadline 안의 한도로 제한. |

[TASK](../Task/T007-ModelGateway.md) · [재현 검증](../Task/Verification/T007-ModelGateway.verification.md) · [Checklist](../Task/Checklist/T007-ModelGateway.checklist.md)

#### T008 · AudioMemoRecorder

- 언어/부모: Kotlin / 없음 (합성). 생성 예정 파일: `android/app/src/main/java/ai/secondlook/capture/AudioMemoRecorder.kt`.
- 기능: F03. 선행: 없음.
- 역할·상태: 글래스 마이크가 우리 앱에 제공된다고 가정하지 않는다. 초기 시연은 앱 전경 녹음이다. 백그라운드 지속 녹음용 새 서비스 클래스는 별도 승인 대상이다. 원음 파일은 앱 전용 영역에 둔다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `start(bookmarkId, consent)` | 본인 북마크·동의·런타임 권한 | 녹음 중 상태 | 권한 미허용·다른 평가자 북마크면 시작 거부. |
| `stop()` | 현재 녹음 | clip 파일·durationMs·mimeType·sampleRate·channels·hash | 최대 30000ms. 파일 완료와 업로드 성공은 구분. |
| `cancel()` | 진행 중 녹음 | 취소 상태 | 불완전 파일을 완료 clip으로 사용하지 않는다. |
| `release()` | 녹음기 리소스 | 해제 상태 | 중단·재호출에도 안전. |

[TASK](../Task/T008-AudioMemoRecorder.md) · [재현 검증](../Task/Verification/T008-AudioMemoRecorder.verification.md) · [Checklist](../Task/Checklist/T008-AudioMemoRecorder.checklist.md)

#### T009 · BookmarkService

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/bookmark_service.py`.
- 기능: F02. 선행: T001, T002, T003.
- 역할·상태: serverReceived 시각으로 북마크 범위를 계산하지 않는다. raw tap, media mapping, 불확실성을 모두 남긴다. 영속화 후 ACK하며 연결 보류도 저장 성공과 분리한다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `recordTap(actor, event)` | 인증 actor·클라이언트 event/anchor | 북마크 ID·저장 ACK·mapping 상태 | 인증·phase·멱등 키 검증 후 저장. |
| `acknowledge(id)` | 저장된 북마크 ID | 영속화 확인 ACK | 미저장·없는 ID를 성공 처리하지 않는다. |
| `resolveWindow(bookmark)` | raw tap·anchor·고정 전사 | 15초 구간·중첩 발화 ID | 불확실성 초과는 연결 확정 보류. |

[TASK](../Task/T009-BookmarkService.md) · [재현 검증](../Task/Verification/T009-BookmarkService.verification.md) · [Checklist](../Task/Checklist/T009-BookmarkService.checklist.md)

#### T010 · PerspectiveService

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/perspective_service.py`.
- 기능: F03, F04. 선행: T001, T002.
- 역할·상태: 루브릭은 세션의 고정3기준이다. 점수척도는 승인된 설정을 사용하며 임의1~5를 하드코딩하지 않는다. AI가 점수·이유를 대신 생성하거나 원래 확정본을 덮어쓰지 않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `addInterpretation(actor, input)` | 본인 북마크·기준·극성·사람확인 텍스트 | 개인 관점 ID·revision | 없는 기준/남의 북마크/미확인 전사 초안 거부. |
| `addQuestion(actor, input)` | 본인 열린 질문·근거 ID | Question ID | 근거 범위·소유 세션 검증. |
| `savePriorScore(actor, criterionId, value, reason)` | 승인 척도의 사람 점수와 이유 | 개인 사전 판단 revision | 기준 밖 점수·빈 이유 거부. |
| `submitPrivateSnapshot(actor, expectedRevision)` | 완성된 메모와3기준 사전 판단 | 불변 확정 snapshot | 필수 항목 누락·낡은 revision 거부. |

[TASK](../Task/T010-PerspectiveService.md) · [재현 검증](../Task/Verification/T010-PerspectiveService.verification.md) · [Checklist](../Task/Checklist/T010-PerspectiveService.checklist.md)

#### T011 · ReviewSessionService

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/review_session_service.py`.
- 기능: F01, F05, F06. 선행: T001, T002, T005.
- 역할·상태: 두 평가자가 각자 확정하기 전 공동 자료를 반환하지 않는다. 단계 진실과 revision은 서버가 소유한다. 1회 역할 nonce는 서버 actor에 매핑하고 재사용을 막는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `createSession(config)` | 동의·미디어·전사·고정루브릭·참여자 수 | 세션과 초대 정보 | 조건 누락 시 생성 거부. |
| `join(roleToken)` | 1회 초대 nonce | 서버 매핑 actor token | 다른 세션/이미 쓴 nonce 거부. |
| `transition(command, expectedRevision)` | 인증 진행 명령·revision | 새 단계·revision | 허용하지 않는 전이·stale state 거부. |
| `revealWhenAllCommitted()` | 각 개인 확정 상태 | 한 번의 공동 공개 | 하나라도 미확정이면 비공개 유지. |
| `comparisonProjection(actor)` | 공개 세션 actor | 단독포착 우선 비교 데이터 | 공개 전에는 본인 범위만. |
| `publishPlaybackAnchor(command)` | 진행자 재생/정지/seek 명령·mediaTimeMs·expectedRevision | 서버 mono시각을 붙인 새 anchorRevision | 진행자 권한·미디어 범위 검증. seek/pause마다 anchor를 교체하고 배포한다. |

[TASK](../Task/T011-ReviewSessionService.md) · [재현 검증](../Task/Verification/T011-ReviewSessionService.verification.md) · [Checklist](../Task/Checklist/T011-ReviewSessionService.checklist.md)

#### T012 · AudioMemoService

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/audio_memo_service.py`.
- 기능: F03. 선행: T001, T002, T007.
- 역할·상태: raw clip·전사 초안·사람 확정 텍스트를 별도로 보존한다. Android가 보낸 duration/MIME을 그대로 신뢰하지 않고 파일과 메타데이터를 검증한다. STT 실패는 북마크를 지우지 않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `acceptClip(actor, bookmarkId, upload)` | 인증 actor·본인북마크·clip | 메모 ID·원음 참조·상태 | 소유자·phase·동의·크기·형식 검증. |
| `validateDurationAndHash(clip)` | 업로드 실제 바이트·메타데이터 | 검증된 duration/hash/MIME | 빈파일·30000ms초과·위장MIME 거부. |
| `transcribeAndPropose(memoId)` | 검증된 clip | 전사 초안과 모델 출처 | 외부동의 확인 후 Gateway 호출. 실패 상태 보존. |
| `confirmTranscript(actor, memoId, editedText)` | 작성자가 검토한 텍스트 | voice_confirmed 텍스트·revision | 원음과초안 덮어쓰지 않음. 확정 후 해석입력에 사용. |

[TASK](../Task/T012-AudioMemoService.md) · [재현 검증](../Task/Verification/T012-AudioMemoService.verification.md) · [Checklist](../Task/Checklist/T012-AudioMemoService.checklist.md)

#### T013 · EvidenceSuggestionService

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/evidence_suggestion_service.py`.
- 기능: F07. 선행: T001, T002, T003, T006, T007.
- 역할·상태: 기본5분 전사는 전체를 작은context로 보낸다. 초기 vector DB나 다중LLM연쇄를 전제하지 않는다. 1~2연결을 우선한다. 캐시는 session·원문/루브릭·메모·prompt/model/settings hash가 모두같을때만 재생한다. AI 입력 inputRevision/hash와 전체 eventRevision은 구분한다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `createSnapshot(sessionId)` | 공개된 확정 관점·고정전사·루브릭 | 입력hash와revision snapshot | 외부AI동의·phase검사. |
| `suggestForDifference(snapshot)` | 검증된차이와전체원문 | 미신뢰 지지/반대 ID·열린질문 | 반대근거없으면빈배열. deadline 동안입력/HUD상태차단X. |
| `verifyAndPersistProposal(snapshot, response)` | AI응답·최초snapshot | suggested 제안·원문발췌 | Validator 통과 후 권한·phase와 의존 입력 inputRevision/hash 재확인. HUD/ACK eventRevision만의 변화로 거부하지 않음. |
| `replayExactCache(key)` | 완전동일입력hash·모델설정 | mode=cache 결과또는miss | prepared/live/cache 출처를 명시. |

[TASK](../Task/T013-EvidenceSuggestionService.md) · [재현 검증](../Task/Verification/T013-EvidenceSuggestionService.verification.md) · [Checklist](../Task/Checklist/T013-EvidenceSuggestionService.checklist.md)

#### T014 · ReviewRecordService

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/review_record_service.py`.
- 기능: F08, F10, F11. 선행: T001, T002, T003.
- 역할·상태: accepted는 사람이 검토했다는 상태이며 객관적 진실 인증이 아니다. 제안/사람결정/원사전판단을 구분한다. 거절한 연결은 합의 사실로 승격하지 않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `reviewProposal(action, reason, changes)` | 수락/수정/거절·이유·수정관계 | 제안과사람검토revision | 기존제안보존·원문범위재검증. |
| `recordFourColumns(input)` | 사실·해석차이·열린질문·변화 | 공동기록revision | 타세션참조·stale revision거부. |
| `revisePerspective(input)` | 초기사전판단을참조한사후변화 | 별도변화기록 | 확정snapshot덮어쓰기금지. |
| `projectGraph()` | 현재노드·연결·검토상태 | Evidence/Criterion/Interpretation/Question 그래프 | 삭제된의견처럼보이지않게미해결·거절상태보존. |
| `handoffQuestion(questionId, target)` | 미해결질문·허용된다음대화 | transferred와원세션연결 | 승인되지않은대상공유거부. |
| `resolveQuestion(questionId, evidenceIds)` | 후속근거와사람확인 | resolved와해소근거 | 해소근거없는해소거부. |

[TASK](../Task/T014-ReviewRecordService.md) · [재현 검증](../Task/Verification/T014-ReviewRecordService.verification.md) · [Checklist](../Task/Checklist/T014-ReviewRecordService.checklist.md)

#### T015 · SecondLookApi

- 언어/부모: Python / 없음 (합성). 생성 예정 파일: `server/second_look/second_look_api.py`.
- 기능: F01–F11 API. 선행: T009, T010, T011, T012, T013, T014.
- 역할·상태: 개인조회와공동조회를분리한다. 업무규칙을API에복제하지않는다. 기존/api/state처럼모든메모를항상반환하는endpoint는두지않는다. requestId/revision/errorCode/retryable응답을통일한다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `bindRoutes(app)` | FastAPI 앱·주입된서비스 | 대표API와WS등록 | 이클래스만API배선·미들웨어설정소유. |
| `authenticate(request)` | actor token | 서버검증actor scope | payload의A/B주장불신·만료/타세션거부. |
| `parseSchema(payload, schema)` | 미신뢰JSON/업로드 | 검증된계약데이터 | 형·크기·필수값오류400/413. |
| `handleCommand(command)` | 인증actor·revision·멱등키 | 서비스결과또는공통오류 | 권한403·충돌409·AI불가503구분. |
| `subscribeEvents(afterRevision)` | 인증scope·마지막revision | 누락이벤트또는현재snapshot | 상대private이벤트전송금지. |

[TASK](../Task/T015-SecondLookApi.md) · [재현 검증](../Task/Verification/T015-SecondLookApi.verification.md) · [Checklist](../Task/Checklist/T015-SecondLookApi.checklist.md)

#### T016 · AndroidSyncClient

- 언어/부모: Kotlin / 없음 (합성). 생성 예정 파일: `android/app/src/main/java/ai/secondlook/data/AndroidSyncClient.kt`.
- 기능: F01, F02, F03, F05, F09. 선행: T015.
- 역할·상태: 한연결은한서버actor/device에매핑한다. 로컬대기·원자저장·서버확인상태를분리한다. 재시작해도대기열과 원 anchor/boot epoch 또는 확정 mediaMs를 보존한다. 다른 시각축을 혼합하지 않고 재동기화한다. 외부AI비밀키를Android에두지않는다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `joinSession(invite, personToken)` | 초대정보·해당actor token | 본인세션scope | 다른역할자동전환금지. |
| `syncClock()` | 서버재생anchor·RTT샘플 | offset·uncertainty·anchor version | 벽시계변경의영향없이monotonic사용. |
| `queueBookmark(inputEvent)` | SDK/폰입력이벤트 | LOCAL_PENDING후SERVER_CONFIRMED | 앱전용파일원자저장후전송·eventId유지. |
| `uploadMemo(bookmarkId, file)` | 본인북마크·완료clip | memoId·전사상태 | 실패시파일·북마크보존. |
| `observeSession(afterRevision)` | 마지막수신revision | scope내새이벤트/snapshot | 끊김·순서역전을복구. |
| `flushPending()` | 저장된미전송이벤트 | 멱등재전송결과 | 동일ID재사용·중복구독금지. |

[TASK](../Task/T016-AndroidSyncClient.md) · [재현 검증](../Task/Verification/T016-AndroidSyncClient.verification.md) · [Checklist](../Task/Checklist/T016-AndroidSyncClient.checklist.md)

#### T017 · HudPresenter

- 언어/부모: Kotlin / 없음 (합성). 생성 예정 파일: `android/app/src/main/java/ai/secondlook/presentation/HudPresenter.kt`.
- 기능: F09. 선행: T004.
- 역할·상태: 그래프와긴원문은웹에둔다. 한질문·최대2줄은목표이며글자수하드코딩대신실측폰트/줄바꿈으로검증한다. TTL과세션revision으로늦은질문을버린다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `showCaptureState(state)` | localPending/serverConfirmed/error | 상태카드 | 로컬기록을서버저장완료로표시금지. |
| `showQuestion(id, text, sessionRevision, expiresAt)` | 사람선택질문·출처상태·기한 | 현재화면질문 | 구버전/다른세션/만료문장거부. |
| `clear()` | 현재카드 | 화면비움요청 | 연결해제·세션종료시호출. |
| `flush()` | 유효한최신대기카드 | Bridge SDK접수결과 | SDK접수와실표시는별도측정. |

[TASK](../Task/T017-HudPresenter.md) · [재현 검증](../Task/Verification/T017-HudPresenter.verification.md) · [Checklist](../Task/Checklist/T017-HudPresenter.checklist.md)

#### T018 · ReviewBoardController

- 언어/부모: JavaScript / 없음 (합성). 생성 예정 파일: `web/src/ReviewBoardController.js`.
- 기능: F03–F11 웹. 선행: T015.
- 역할·상태: 서버권한을DOM숨김으로대체하지않는다. 간단SVG와같은관계의접근가능목록을함께쓴다. AI제안·사람검토·미검증·live/cache/prepared라벨을유지한다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
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

[TASK](../Task/T018-ReviewBoardController.md) · [재현 검증](../Task/Verification/T018-ReviewBoardController.verification.md) · [Checklist](../Task/Checklist/T018-ReviewBoardController.checklist.md)

#### T019 · CompanionActivity

- 언어/부모: Kotlin / androidx.activity.ComponentActivity. 생성 예정 파일: `android/app/src/main/java/ai/secondlook/CompanionActivity.kt`.
- 기능: F01–F05, F09 Android. 선행: T004, T008, T016, T017.
- 역할·상태: 기기·녹음·동기화·HUD클래스를조립하고업무판정은서버에둔다. UI스레드에서네트워크/전사를기다리지않는다. 초기G0실험은기존공식예제로완료하므로순환의존이없다.

| 공개 메서드 | 입력 | 출력 | 실패·부작용 / 구현 주석 계약 |
| --- | --- | --- | --- |
| `onCreate(savedState)` | 앱복원정보·주입설정 | 권한·연결·세션화면초기화 | 새actor자동생성/역할바꿈금지. |
| `onStart()` | 전경생명주기 | 필요구독연결 | 구독중복방지. |
| `onStop()` | 이탈/잠금/백그라운드 | 녹음중단·상태보존정책 | 지속녹음성공으로오표시X. |
| `render(state)` | 연결·대기·녹음·개인확정상태 | 사용자화면 | 상대공개전자료없음. |
| `bindActions()` | 탭/메모/확정등사용자행동 | 담당클래스호출 | AI판단/저장규칙복제X. |

[TASK](../Task/T019-CompanionActivity.md) · [재현 검증](../Task/Verification/T019-CompanionActivity.verification.md) · [Checklist](../Task/Checklist/T019-CompanionActivity.checklist.md)


### 5.11 G0 gate·기존 시안과의 차이·미검증

**초기 G0: T004 RokidBridge에서 공식 샘플 또는 최소 테스트 harness로 확인한다.** 최후의 CompanionActivity를 선행 요구하지 않는다.

- 실기기/SN·펌웨어·Android·Hi Rokid·SDK 버전과 SDK 인증/개발 승인 상태.
- 실제 앱 viewport·한국어 질문 표시·읽기 가능성.
- 요구하는 탭 입력 callback 지원·20회 수신/누락/중복.
- SDK 연결 중 서버 LAN/인터넷 경로의 동시 연결 가능성.
- 허용 서명·패키지·토큰·배포 방식과 실제 개발 권한.
- 실패 시 원인·확인한 조건을 보고하고 CXR-M 또는 수동 시연 대안을 승인받는다. 지원을 가정해 후속 통합을 완료 처리하지 않는다.

현재 시안의 한계는 요구사항 대조, 읽기/쓰기 경로 추적, 반례 세 관점의 정적 검토로 확인했다. HTTP 재현·실기기·AI 실호출은 이번에 하지 않았다.

| 현재 관측 | 영향 | 승인 뒤 바꿀 부분 |
| --- | --- | --- |
| 기존 /api/state는 항상 전체 메모를 반환하고 actor 인증이 없다. | 화면을 숨겨도 독립 기록·공개 게이트를 강제할 수 없다. | SessionPolicy·Repository·ReviewSessionService·SecondLookApi의 권한/원자 공개 구조 |
| 기존 AI 검사는 형식과 ID 존재 중심이다. | 타 세션·낡은 snapshot·관계 의미 정확성을 보장하지 못한다. | Validator·SuggestionService의 범위/버전 검사와 사람 검토 경로 |
| 15초 미디어 매핑·사전 점수·실제 Graph·검토 이력이 없다. | 콘텐츠 핵심 경험의 일부는 화면 시안에 머문다. | Timeline·Perspective/ReviewRecordService·웹 보드 |
| HUD는 웹 시안이고 Android/글래스 연결이 없다. | 실제 글래스 입력·표시·지연을 주장할 수 없다. | Bridge G0 뒤 Android 동기화·Presenter·Activity |

이는 현재 개념 시안의 설계 한계를 설명한 것이며, 본 문서 작업에서 기존 코드를 수정하거나 재구현하지 않았다. 승인 전까지 기존 시안을 보존한다.

## 6. TASK 구현 순서

[전체 TASK 인덱스](../Task/README.md)에서 클래스별 구현·검증·Checklist로 이동한다. **19 TASK = 19 프로덕션 클래스**이며, 모든 제품 TASK는 미구현·실행 미검증이다.

- T001–T003: 접근 정책·저장·시간 계약을 독립 fixture로 고정한다.
- T004: 최우선 G0 기기 연결·표시·입력·네트워크 가능성을 공식 예제로 확인한다. 최종 Activity에 의존하지 않는다.
- T005–T008: 규칙 분류·AI 검증/호출 계약·폰 녹음 독립 도구를 검증한다.
- T009–T014: 북마크·개인 관점·공개·음성·AI 제안·공동 검토 서비스를 순서대로 검증한다.
- T015–T018: API·Android 동기화·HUD·웹 보드를 연결한다.
- T019: Android 호스트를 조립하고 승인된 전체 시나리오를 검증한다.

각 TASK는 관련 클래스 하나를 구현·검증한 뒤 다음 TASK로 인계한다. 의존성이 큰 최종 조립은 나중에 두되, 기기와 네트워크 연결 가능성은 초반에 확인한다. 포괄 실행 승인에 포함된 범위는 반복 승인하지 않는다. 범위/기획이 바뀌면 다시 검토한다.

## 7. 전체 컨펌에서 결정할 항목

첫 화면 D1–D6을 기준으로 승인·수정 의견을 받는다. 사양·권한·수량·척도가 아직 없다는 이유로 지원을 가정하거나 기능을 몰래 제거하지 않는다.

- 1대만 사용할 경우: 한 SDK 연결을 A·B 두 명에게 동시에 매핑하지 않는다. 교대 시연의 한계를 표시하고, 독립 입력 대안은 승인 후 선택한다.
- 음성 메모: 원기획에서 유지한다. 텍스트 입력을 기본 시연으로 바꾸는 것은 사용자 범위 결정이다.
- 서버/모델: 품질 문턱을 통과한 경로 중 실측 지연이 좋은 것을 선택한다. 실제 모델·키·성능은 아직 확인하지 않았다.
- 연구 실험의 4조건 비교나 범용 채용 제품 기능은 별도 자동 TASK로 만들지 않았다.
- 승인 전에는 제품 구현·기존 시스템 재작성·패키지 설치·기기 배포를 시작하지 않는다.

## 8. 기획·UX 참고 근거와 한계

- [Metaview 공식 제품 설명](https://www.metaview.ai/resources/blog/candidate-review-align): 원문·역량·평가자 의견 차이에서 근거로 이동하는 구조를 참고했다. 원문 연결 자체를 SECOND LOOK만의 신규 기능으로 주장하지 않는다.
- [Buçinca et al. (2021), To Trust or to Think](https://www.iis.seas.harvard.edu/papers/2021/bucinca2021trust.shtml): AI 공개 전 사람의 사전 판단을 보존하는 설계 근거다. 해당 연구는 인지적 개입이 과의존을 줄일 수 있지만 사용 만족도와의 상충도 보고한다. 본 면접 맥락의 효과는 별도 검증이 필요하다.
- [Chiang et al. (2024), LLM-Powered Devil’s Advocate](https://doi.org/10.1145/3640543.3645199): 반대 관점 검토를 위한 관련 연구다. 논문 존재와 원저자 공개 목록을 확인했으며 전문을 안정적으로 열지 못했으므로 결과 수치를 인용하지 않는다. 지지·반대 근거 대칭 검토는 이미 주어진 기획에서 유지한 조건이다.
