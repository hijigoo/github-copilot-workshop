# Step 0. 환경 세팅

> ⏱️ 15분 | 난이도 ⭐
>
> Copilot과 개발 환경을 준비합니다.

---

## 사전 요구사항

- GitHub 계정 (Copilot 라이선스 활성화)
- JDK 17+
- Git

---

## IntelliJ IDEA 환경 세팅

### 1. IntelliJ IDEA 설치

[https://www.jetbrains.com/idea/](https://www.jetbrains.com/idea/) 에서 Community 또는 Ultimate 버전 설치

### 2. Copilot 플러그인 설치

1. `Settings > Plugins > Marketplace`
2. "GitHub Copilot" 검색 → 설치
3. IDE 재시작
4. GitHub 계정으로 로그인 진행

> 📸 **[IntelliJ 스크린샷]** Settings > Plugins > Marketplace에서 "GitHub Copilot"을 검색하여 설치하는 화면
>
> ![Copilot 플러그인 설치](./images/step00-plugin-install.png)

| 플러그인 | 설명 |
|---------|------|
| **GitHub Copilot** | 코드 자동완성 + AI 채팅 |

설치 후 IntelliJ 우측 사이드바 또는 하단에 **GitHub Copilot** 탭이 보이는지 확인하세요.

### 3. Copilot 로그인

1. `Settings > Tools > GitHub Copilot` 으로 이동
2. `Login to GitHub` 클릭
3. 브라우저에서 인증 코드 입력 후 로그인
4. IntelliJ로 돌아오면 Copilot 활성화 완료

> 📸 **[IntelliJ 스크린샷]** Settings > Tools > GitHub Copilot에서 "Login to GitHub" 버튼이 보이는 화면
>
> ![Copilot 로그인](./images/step00-copilot-login.png)

### 4. 동작 확인

- 우측 사이드바 또는 하단에 **GitHub Copilot Chat** 탭이 있는지 확인
- Java 파일에서 코드 입력 시 Ghost Text 제안이 나타나는지 확인

> 📸 **[IntelliJ 스크린샷]** IntelliJ 우측 사이드바 또는 하단에 표시되는 GitHub Copilot Chat 탭 위치
>
> ![Copilot Chat 탭 위치](./images/step00-copilot-chat-tab.png)

---

## 프로젝트 초기화

### Spring Initializr로 프로젝트 생성

1. [https://start.spring.io/](https://start.spring.io/) 접속
2. 다음 설정으로 프로젝트 생성:

| 항목 | 값 |
|------|-----|
| Project | Gradle - Kotlin |
| Language | Java |
| Spring Boot | 3.x (최신 안정 버전) |
| Group | `com.example` |
| Artifact | `todo` |
| Java | 17 |

3. Dependencies 추가:
   - **Spring Web**
   - **Spring Data JPA** (Step 6에서 사용, 미리 추가)
   - **H2 Database** (Step 6에서 사용, 미리 추가)
   - **Validation** (Bean Validation)

> 📸 **[스크린샷]** Spring Initializr 웹사이트에서 위 설정을 입력하고 Dependencies를 추가한 화면
>
> ![Spring Initializr 설정](./images/step00-spring-initializr.png)

4. **Generate** 클릭 → ZIP 다운로드 → 압축 해제

### IntelliJ에서 프로젝트 열기

```bash
# 또는 IntelliJ에서 File > Open > 압축 해제한 폴더 선택
```

Gradle 빌드가 완료될 때까지 기다립니다.

---

## 검증

### 빌드 확인

```bash
./gradlew build
```

BUILD SUCCESSFUL이 출력되면 성공! ✅

### Copilot 동작 확인

1. `src/main/java/com/example/todo/` 아래에 아무 Java 파일 열기
2. `public class` 까지 타이핑
3. Copilot이 자동완성을 제안하면 성공! ✅

> 📸 **[IntelliJ 스크린샷]** Java 파일에서 코드 입력 시 Ghost Text(회색 텍스트)가 나타나는 모습
>
> ![Ghost Text 제안](./images/step00-ghost-text.png)

---

## 프로젝트 구조 (초기)

```
todo/
├── build.gradle.kts
├── settings.gradle.kts
├── src/
│   ├── main/
│   │   ├── java/com/example/todo/
│   │   │   └── TodoApplication.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/com/example/todo/
│           └── TodoApplicationTests.java
└── gradlew
```

---

## ⚠️ 이 단계의 규칙

> **Copilot Inline(Tab 자동완성)만 사용하세요.**
> Chat은 아직 열지 마세요. 다음 단계에서 배워봅니다!

---

## 다음 단계

→ [Step 1. Inline Suggestions](../step-01-inline/README.md)
