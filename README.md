# 🤖 GitHub Copilot 점진적 체험 워크샵

GitHub Copilot의 기능을 단계별로 익히는 핸즈온 워크샵입니다.
TODO 앱을 처음부터 만들어가며, 자동완성부터 Chat, Agent, Custom Agent까지 Copilot의 핵심 기능을 하나씩 체험합니다.
각 단계의 README를 따라가기만 하면 되고, 외부 서비스 없이 로컬 환경에서 모두 진행할 수 있습니다.

---

## 언어별 워크샵 선택

동일한 커리큘럼을 **Python**과 **Java** 두 가지 언어로 제공합니다.
본인에게 익숙한 언어를 선택하세요.

| 언어 | IDE | 프레임워크 | 시작하기 |
|:----:|:---:|----------|---------|
| 🐍 Python | VS Code | FastAPI + SQLModel | [Python 워크샵 →](python/README.md) |
| ☕ Java | IntelliJ IDEA | Spring Boot + Spring Data JPA | [Java 워크샵 →](java/README.md) |

---

## 학습 로드맵 (공통)

### 메인 트랙

| Step | 주제 | 무엇을 배우나요? |
|:----:|------|-----------------|
| 00 | 환경 세팅 | 개발 환경, IDE, Copilot 설치 및 동작 확인 |
| 01 | 코드 완성 | Tab 키로 Copilot 자동완성을 수락·거절하는 기본기 |
| 02 | Copilot Chat | Chat 패널에서 대화로 코드 생성·리팩터링하기 |
| 03 | Instructions | 프로젝트 규칙 파일을 만들어 반복 설명 없이 일관된 응답 받기 |
| 04 | Spec-Driven Dev | 타입 정의 → 테스트 → 구현 순서로 정확한 코드 생성하기 |
| 05 | Prompt Files | 반복 작업을 매크로처럼 한 번에 실행하는 프롬프트 파일 만들기 |
| 06 | Agent 모드 | 큰 작업(아키텍처 전환)을 Agent에게 통째로 맡기기 |
| 07 | Custom Agent | 나만의 전문 Agent(코드 리뷰, DB 등) 직접 만들기 |
| 08 | 고급 워크플로우 | Plan 기능 + Custom Agent 조합으로 Vibe Coding 실습 |

### 보너스 트랙

| Step | 주제 | 무엇을 배우나요? |
|:----:|------|-----------------|
| 09 | Docker | Copilot으로 Dockerfile, docker-compose 설정 생성 및 컨테이너화 |
| 10 | React 프론트엔드 | Copilot과 함께 TODO 앱 UI 만들기 |
| 11 | 언어 마이그레이션 | 다른 언어로 TODO API를 다시 구현하며 전환 체험 |
| 12 | Chat Debug View | Chat Debug View로 Copilot 내부 동작 분석 |

---

## 참고

- 모든 주석·독스트링·커밋 메시지는 **한국어**로 작성합니다.
- 각 스텝은 **해당 단계까지 배운 기능만** 사용하도록 설계되어 있습니다.
- 막히면 `complete/` 폴더의 참고 코드를 확인하세요.

## 라이선스

MIT License
