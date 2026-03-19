# Step 0. 환경 세팅

> ⏱️ 15분 | 난이도 ⭐
>
> Copilot과 개발 환경을 준비합니다.

---

## 사전 요구사항

- GitHub 계정 (Copilot 라이선스 활성화)
- Python 3.11+
- Git

---

## VS Code 환경 세팅

### 1. VS Code 설치

[https://code.visualstudio.com/](https://code.visualstudio.com/) 에서 최신 버전 설치

### 2. 확장 설치

| 확장 | 설명 |
|------|------|
| **GitHub Copilot** | 코드 자동완성 |
| **GitHub Copilot Chat** | AI 채팅 |
| **Python** (ms-python) | Python 지원 |

설치 후 VS Code 좌측 하단에 Copilot 아이콘이 보이는지 확인하세요.

### 3. Copilot 로그인

1. `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) → `GitHub Copilot: Sign In`
2. GitHub 계정으로 로그인
3. 상태 바에 Copilot 아이콘 ✅ 표시 확인

> 📸 **스크린샷**: VS Code 하단 상태 바에 Copilot 아이콘이 활성화된 모습
> ![VS Code 상태 바 Copilot 아이콘](./assets/vscode-copilot-status-bar.png)

### 4. 동작 확인

상태 바(좌측 하단)에 Copilot 아이콘 클릭 시 다음 항목을 확인하세요:

- **Copilot Enterprise Usage**: Inline Suggestions, Chat messages, Premium requests 포함 여부
- **Inline Suggestions**: `All files` 체크 ✅ 확인
- 필요 시 언어별(Markdown 등) 토글 가능
- `Snooze` 버튼으로 5분간 제안 일시 중지 가능

---

## IntelliJ 환경 세팅

### 1. IntelliJ IDEA 설치

[https://www.jetbrains.com/idea/](https://www.jetbrains.com/idea/) (Community 또는 Ultimate)

### 2. Copilot 플러그인 설치

1. `Settings > Plugins > Marketplace`
2. "GitHub Copilot" 검색 → 설치
3. IDE 재시작
4. GitHub 로그인 진행

### 3. Copilot 탭 확인

- 우측 사이드바 또는 하단에 **GitHub Copilot** 탭이 있는지 확인

> 📸 **스크린샷**: IntelliJ 우측에 Copilot Chat 탭이 보이는 모습
> ![IntelliJ Copilot Chat 탭](./assets/intellij-copilot-chat-tab.png)

### 4. IntelliJ 사용자 선택

- **Python 트랙**: Python Plugin 설치 후 동일하게 진행
- **Java/Kotlin 트랙**: Java 트랙의 Step 01부터 Spring Boot로 진행

---

## 프로젝트 초기화

터미널에서 실행:

```bash
# 프로젝트 폴더 생성
mkdir todo-app && cd todo-app

# Git 초기화
git init

# Python 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

# 의존성 설치 (서버 실행에 필요한 최소한만)
pip install fastapi uvicorn

# 프로젝트 디렉터리 구조 생성
mkdir -p app tests
touch app/__init__.py tests/__init__.py
```

---

## 검증

### Python 환경 확인

```bash
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
```

버전이 출력되면 성공! ✅

> 테스트 도구(pytest, httpx)는 Step 4에서, DB(sqlmodel)는 Step 7 Agent 모드에서 설치합니다.
> 각 단계의 `starter/requirements.txt`에 필요한 의존성이 포함되어 있습니다.

### Copilot 동작 확인

1. `app/main.py` 파일 생성
2. `from fastapi import` 까지 타이핑
3. Copilot이 자동완성을 제안하면 성공! ✅

---

## 프로젝트 구조 (완성 시)

```
todo-app/
├── .venv/
├── app/
│   ├── __init__.py
│   └── (이후 단계에서 추가)
├── tests/
│   ├── __init__.py
│   └── (이후 단계에서 추가)
└── requirements.txt
```

---

## ⚠️ 이 단계의 규칙

> **Copilot Inline(Tab 자동완성)만 사용하세요.**
> Chat은 아직 열지 마세요. 다음 단계에서 배워봅니다!

---

## 다음 단계

→ [Step 1. Inline Suggestions](../step-01-inline/README.md)
