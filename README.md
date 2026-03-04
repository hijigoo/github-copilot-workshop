# 🤖 GitHub Copilot 점진적 체험 워크샵

GitHub Copilot의 기능을 단계별로 익히는 핸즈온 워크샵입니다.
TODO 앱을 처음부터 만들어가며, 자동완성부터 Chat, Agent, Custom Agent까지 Copilot의 핵심 기능을 하나씩 체험합니다.
각 단계의 README를 따라가기만 하면 되고, 외부 서비스 없이 로컬 환경에서 모두 진행할 수 있습니다.

---

## 시작하기

[Step 00 — 환경 세팅](step-00-setup/)부터 따라가세요. 각 스텝의 README가 튜토리얼 가이드입니다.

> 이 저장소는 **튜토리얼 문서와 참고 코드**를 제공합니다.
> 특정 스텝만 실습하고 싶다면 해당 스텝의 `starter/` 코드를 복사해 시작할 수 있지만, 처음부터 순서대로 진행하는 것을 추천합니다.

---

## 프로젝트 구조

각 스텝 폴더는 `README.md`(가이드) + `starter/`(시작 코드) + `complete/`(완성 코드)로 구성됩니다.
보너스 트랙(09~11)은 README 가이드만 제공하는 자율 실습입니다.

---

## 학습 로드맵

### 메인 트랙

| Step | 주제 | 무엇을 배우나요? |
|:----:|------|-----------------|
| [00](step-00-setup/) | 환경 세팅 | Python, VS Code, Copilot 설치 및 동작 확인 |
| [01](step-01-inline/) | 코드 완성 | Tab 키로 Copilot 자동완성을 수락·거절하는 기본기 |
| [02](step-02-chat/) | Copilot Chat | Chat 패널에서 대화로 코드 생성·리팩터링하기 |
| [03](step-03-instructions/) | Instructions | 프로젝트 규칙 파일을 만들어 반복 설명 없이 일관된 응답 받기 |
| [04](step-04-spec-driven/) | Spec-Driven Dev | 타입 정의 → 테스트 → 구현 순서로 정확한 코드 생성하기 |
| [05](step-05-prompt-files/) | Prompt Files | 반복 작업을 매크로처럼 한 번에 실행하는 프롬프트 파일 만들기 |
| [06](step-06-agent/) | Agent 모드 | 큰 작업(아키텍처 전환)을 Agent에게 통째로 맡기기 |
| [07](step-07-custom-agent/) | Custom Agent | 나만의 전문 Agent(코드 리뷰, DB 등) 직접 만들기 |
| [08](step-08-advanced/) | 고급 워크플로우 | Plan 기능 + Custom Agent 조합으로 Vibe Coding 실습 |

### 보너스 트랙

| Step | 주제 | 무엇을 배우나요? |
|:----:|------|-----------------|
| [09](step-09-bonus-a-extras/) | 추가 실습 | 언어 마이그레이션, Docker, API 문서 자동화 등 실전 시나리오 |
| [10](step-10-bonus-b-react/) | React 프론트엔드 | Copilot과 함께 TODO 앱 UI 만들기 (Vite + TS + Tailwind) |
| [11](step-11-bonus-c-spring/) | Spring Boot 백엔드 | 같은 TODO API를 Java로 다시 구현하며 언어 전환 체험 |

---

## 참고

- 모든 주석·독스트링·커밋 메시지는 **한국어**로 작성합니다.
- 각 스텝은 **해당 단계까지 배운 기능만** 사용하도록 설계되어 있습니다.
- 막히면 `complete/` 폴더의 참고 코드를 확인하세요.

## 라이선스

MIT License
