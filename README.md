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
| 🐍 Python | VS Code | FastAPI + Pydantic | [Python 워크샵 →](python/README.md) |
| ☕ Java | IntelliJ IDEA / VS Code | Spring Boot + Spring Data JPA | [Java 워크샵 →](java/README.md) |

---

## 학습 로드맵 (공통)

### 메인 트랙

| Step | 주제 | 무엇을 배우나요? | 소요 시간 |
|:----:|------|-----------------|:--------:|
| 00 | 환경 세팅 | 개발 환경, IDE, Copilot 설치 및 동작 확인 | 15분 |
| 01 | 코드 완성 (Inline) | Tab 키로 Copilot 자동완성을 수락·거절하는 기본기 | 15분 |
| 02 | Copilot Chat | Chat 패널에서 대화로 코드 생성·리팩터링하기 | 20분 |
| 03 | Instructions | 프로젝트 규칙 파일을 만들어 반복 설명 없이 일관된 응답 받기 | 20분 |
| 04 | Prompt Files | 반복 작업을 매크로처럼 한 번에 실행하는 프롬프트 파일 만들기 | 15분 |
| 05 | Agent 모드 | 큰 작업(아키텍처 전환)을 Agent에게 통째로 맡기기 | 30분 |
| 06 | Custom Agent | 나만의 전문 Agent(코드 리뷰어, 빌더 등) 직접 만들기 | 25분 |
| 07 | Sub-Agent | Sub-Agent를 활용한 역할 분담 + 자동 연쇄 호출로 팀 협업 시뮬레이션 | 25분 |
| 08 | 고급 워크플로우 | Plan 기능으로 큰 기능을 체계적으로 계획 → 구현하기 | 25분 |
| 09 | Spec-Driven Dev | 문서 기반 스펙 → 분석/계획 → 테스트 → 구현 패턴 실습 | 25분 |

### 보너스 트랙

| Step | 주제 | 무엇을 배우나요? |
|:----:|------|-----------------|
| 10 | README 문서화 | Copilot으로 프로젝트 README + Mermaid 다이어그램 생성 |
| 11 | Docker | Copilot으로 Dockerfile, docker-compose 생성 및 컨테이너화 |
| 12 | React 프론트엔드 | Copilot과 함께 TODO 앱 UI 만들기 |

---

## 프로젝트 구조

```
github-copilot-workshop/
├── README.md              ← 이 파일
├── python/                ← Python 트랙 (FastAPI + VS Code)
│   ├── README.md
│   ├── step-00-setup/
│   ├── step-01-inline/
│   │   ├── starter/       ← 시작 코드
│   │   └── complete/      ← 참고 정답
│   ├── ...
    └── step-12-bonus-b-react/
└── java/                  ← Java 트랙 (Spring Boot + IntelliJ)
    ├── README.md
    ├── step-00-setup/
    ├── step-01-inline/
    │   ├── starter/
    │   └── complete/
    ├── ...
    └── step-12-bonus-b-react/
```

각 스텝에는 `starter/`(시작 코드)와 `complete/`(참고 정답)가 포함되어 있습니다.

---

## 참고

- 모든 주석·독스트링·커밋 메시지는 **한국어**로 작성합니다.
- 각 스텝은 **해당 단계까지 배운 기능만** 사용하도록 설계되어 있습니다.
- Step 07~09는 빈 프로젝트에서 시작하여 Agent가 처음부터 코드를 생성합니다.
- 막히면 `complete/` 폴더의 참고 코드를 확인하세요.

## 라이선스

MIT License
