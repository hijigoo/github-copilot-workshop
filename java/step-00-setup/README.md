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

## JDK 설치 확인

### Java 설치 여부 확인

터미널(또는 IntelliJ Terminal)에서 다음 명령어를 실행하세요:

```bash
java -version
```

**정상 출력 예시:**
```
openjdk version "17.0.x" 2024-xx-xx
OpenJDK Runtime Environment ...
```

`17` 이상의 버전이 출력되면 다음 단계로 넘어가세요! ✅

### 설치된 JDK 버전 전체 확인

여러 버전의 JDK가 설치되어 있을 수 있습니다. 현재 설치된 전체 목록을 확인하려면:

| OS | 명령어 | 설명 |
|----|--------|------|
| **macOS (Homebrew)** | `brew list \| grep openjdk` | Homebrew로 설치된 JDK 목록 |
| **macOS (전체 경로)** | `/usr/libexec/java_home -V` | 시스템에 등록된 모든 JDK |
| **Windows** | `dir "C:\Program Files\Java"` | Java 설치 폴더 확인 |
| **Windows** | `dir "C:\Program Files\Eclipse Adoptium"` | Adoptium JDK 확인 |
| **Linux (Ubuntu)** | `update-alternatives --list java` | 등록된 JDK 목록 |

### Java가 설치되어 있지 않다면?

`java: command not found` 또는 버전이 17 미만이라면 JDK를 설치해야 합니다.

#### 방법 1: 직접 설치

| OS | 설치 방법 |
|----|----------|
| **macOS** | `brew install openjdk@17` |
| **Windows** | [Adoptium](https://adoptium.net/) 에서 JDK 17 다운로드 후 설치 |
| **Linux (Ubuntu)** | `sudo apt install openjdk-17-jdk` |

설치 후 `java -version`으로 다시 확인하세요.

> 💡 macOS에서 Homebrew가 없다면: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

#### 방법 2: Copilot Agent에게 설치 시키기 🤖

Copilot Agent 모드를 사용하면 설치까지 한 번에 해결할 수 있습니다! IntelliJ Copilot Chat에서:

```
내 컴퓨터에 JDK 17이 설치되어 있는지 확인하고, 없으면 설치해줘
```

Agent가 터미널에서 `java -version`을 실행하여 확인하고, 설치되어 있지 않으면 OS에 맞는 설치 명령어를 직접 실행해 줍니다.

> 💡 Agent 모드는 Step 5에서 자세히 배우지만, 이렇게 환경 세팅에도 활용할 수 있습니다!

#### 방법 3: IntelliJ에서 JDK 자동 다운로드

IntelliJ IDEA는 JDK를 직접 다운로드하는 기능을 제공합니다:

1. `File > Project Structure > Project` (또는 `Ctrl+Alt+Shift+S`)
2. **SDK** 드롭다운 → `Add SDK > Download JDK...`
3. **Version**: `17`, **Vendor**: `Eclipse Temurin` (또는 원하는 벤더) 선택
4. **Download** 클릭

> 📸 **[IntelliJ 스크린샷]** Project Structure > SDK > Download JDK 화면에서 JDK 17을 선택하여 다운로드하는 모습
>
> ![IntelliJ JDK 다운로드](./images/step00-intellij-download-jdk.png)

---

## IntelliJ IDEA 환경 세팅

### 1. IntelliJ IDEA 설치

[https://www.jetbrains.com/idea/](https://www.jetbrains.com/idea/) 에서 Community 또는 Ultimate 버전 설치

### 2. Copilot 플러그인 설치

1. `Settings > Plugins > Marketplace`
2. "GitHub Copilot" 검색 → 설치

> 📸 **[IntelliJ 스크린샷]** Settings > Plugins > Marketplace에서 "GitHub Copilot"을 검색하여 설치하는 화면

>![Copilot 플러그인 설치](./images/step00-plugin-install.png)

3. IDE 재시작


### 3. Copilot 로그인

1. `Settings > Tools > GitHub Copilot` 으로 이동
   - Mac: `IntelliJ IDEA > Settings > Tools > GitHub Copilot`
   - Windows: `File > Settings > Tools > GitHub Copilot`
2. **General** 탭에서 `Sign in to GitHub Copilot` 클릭
3. 브라우저에서 인증 코드 입력 후 로그인
4. IntelliJ로 돌아오면 Copilot 활성화 완료

> 📸 **[IntelliJ 스크린샷]** Settings > Tools > GitHub Copilot > General에서 "Sign in to GitHub Copilot" 링크가 보이는 화면
>
> ![Copilot 로그인](./images/step00-copilot-login.png)

---

## 프로젝트 초기화

### Spring Initializr로 프로젝트 생성

1. [https://start.spring.io/](https://start.spring.io/) 접속
2. 다음 설정으로 프로젝트 생성:

| 항목 | 값 |
|------|-----|
| Project | Gradle - Kotlin |
| Language | Java |
| Spring Boot | 4.x (최신 안정 버전) |
| Group | `com.example` |
| Artifact | `todo` |
| Packaging | Jar |
| Configuration | Properties |
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

- IntelliJ 시작 화면에서 **열기** 버튼 클릭 → 압축 해제한 폴더 선택
- 또는 이미 프로젝트가 열려있다면: `File > Open` → 폴더 선택

> 📸 **[IntelliJ 스크린샷]** IntelliJ 시작 화면에서 "열기" 버튼을 클릭하여 프로젝트를 여는 모습
>
> ![IntelliJ 프로젝트 열기](./images/step00-open-project.png)

---

## 검증

### Gradle 빌드 확인

IntelliJ에서 프로젝트를 열면 **Gradle 빌드가 자동으로 시작**됩니다.
좌측 사이드바의 **빌드 도구 아이콘**(🔨 망치 모양)을 클릭하면 빌드 진행 상황과 결과를 확인할 수 있습니다.

> 📸 **[IntelliJ 스크린샷]** 좌측 사이드바의 빌드 도구 아이콘(🔨)을 클릭하여 Gradle 빌드 진행 상황을 확인하는 화면
>
> ![빌드 도구 확인](./images/step00-build-tool.png)


터미널에서도 확인할 수 있습니다:

```bash
./gradlew build
```

BUILD SUCCESSFUL이 출력되면 성공! ✅

만약 JDK 버전 관련 에러가 발생하면 `-D` 옵션으로 Java Home 경로를 직접 지정해 보세요:

```bash
# macOS (Homebrew로 JDK 17 설치한 경우)
./gradlew build -Dorg.gradle.java.home=/opt/homebrew/opt/openjdk@17

# Windows (PowerShell)
.\gradlew build -Dorg.gradle.java.home="C:\Program Files\Eclipse Adoptium\jdk-17"
```

JDK 경로를 모르겠다면 [🔧 JDK 경로를 모르겠다면?](#-jdk-경로를-모르겠다면)을 참고하세요.
위 방버으로 해결되지 않으면 하단의 [🔧 빌드 에러가 나면?](#-빌드-에러가-나면)을 참고하세요.


### Copilot 동작 확인

1. 우측 사이드바 또는 하단에 **GitHub Copilot Chat** 탭이 있는지 확인

> 📸 **[IntelliJ 스크린샷]** IntelliJ 우측 사이드바 또는 하단에 표시되는 GitHub Copilot Chat 탭 위치
>
> ![Copilot Chat 탭 위치](./images/step00-copilot-chat-tab.png)

2. `src/main/java/com/example/todo/` 아래에 아무 Java 파일 열기
3. `public class` 까지 타이핑
4. Copilot이 자동완성을 제안하면 성공! ✅

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

## 트러블슈팅

<details>
<summary><strong>🔧 빌드 에러가 나면?</strong></summary>

### 1. 프로젝트 SDK 설정

| OS | 진입 경로 | 단축키 |
|----|----------|--------|
| **Mac** | `File > Project Structure` | `Cmd + ;` |
| **Windows** | `File > Project Structure` | `Ctrl + Alt + Shift + S` |

- 좌측 메뉴에서 **Project** 선택
- SDK가 `<No SDK>`로 되어 있다면 → `Add SDK > Download JDK` → `build.gradle.kts`에 명시된 버전(17) 선택

### 2. Gradle JVM 설정 확인

| OS | 진입 경로 | 단축키 |
|----|----------|--------|
| **Mac** | `Settings` | `Cmd + ,` |
| **Windows** | `Settings` | `Ctrl + Alt + S` |

- `Build, Execution, Deployment > Build Tools > Gradle`로 이동
- **Gradle JVM** 항목을 1번에서 설정한 SDK와 동일한 버전으로 변경

### 3. Gradle 새로고침

설정 변경 후 반드시 실행:

- 우측 사이드바의 **Gradle 탭**(🐘 코끼리 아이콘) 열기
- 좌측 상단의 **Reload All Gradle Projects** (🔄 회전 화살표 아이콘) 클릭

</details>

<details>
<summary><strong>🔧 IntelliJ에서는 빌드되는데 터미널에서 <code>./gradlew build</code> 실패?</strong></summary>

`Cannot find a Java installation matching: {languageVersion=17}` 에러가 나는 경우,
IntelliJ 내부에서는 JDK를 찾지만 터미널의 Gradle은 시스템에 설치된 JDK를 찾지 못하는 것입니다.

#### 해결 방법 A: JAVA_HOME 지정하여 빌드

JDK 17이 시스템에 설치되어 있지만 기본 버전이 21 등 다른 버전인 경우에 사용합니다.
먼저 경로가 존재하는지 확인하세요:

```bash
# macOS — JDK 17 경로 존재 확인
ls /opt/homebrew/opt/openjdk@17
```

폴더 내용이 출력되면 JDK 17이 설치된 것입니다. 다음과 같이 JAVA_HOME을 지정하고 빌드하세요:

```bash
# macOS (Homebrew로 설치한 경우)
export JAVA_HOME=/opt/homebrew/opt/openjdk@17
export PATH=$JAVA_HOME/bin:$PATH
./gradlew build

# Windows (PowerShell)
$env:JAVA_HOME="C:\Program Files\Eclipse Adoptium\jdk-17"; .\gradlew build
```

> 💡 매번 입력하기 번거로우면 `~/.zshrc` (macOS) 또는 시스템 환경 변수 (Windows)에 추가하세요.

> ⚠️ 해당 경로에 JDK 17이 없으면 **방법 B**로 먼저 설치하세요.

#### 해결 방법 B: JDK 17을 시스템에 설치

```bash
# macOS
brew install openjdk@17

# 설치 후 심볼릭 링크 생성 (Gradle이 찾을 수 있도록)
sudo ln -sfn $(brew --prefix openjdk@17)/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk
```

#### 해결 방법 C: Gradle 툴체인 자동 다운로드 설정

`settings.gradle.kts` 파일 상단에 다음을 추가하면 Gradle이 필요한 JDK를 자동으로 다운로드합니다:

```kotlin
plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "0.9.0"
}
```

추가 후 다시 `./gradlew build`를 실행하세요.

</details>

<details>
<summary><strong>🔧 JDK 경로를 모르겠다면?</strong></summary>

IntelliJ가 사용 중인 실제 JDK 경로를 복사할 수 있습니다:

1. `File > Project Structure` (Mac: `Cmd + ;` / Windows: `Ctrl + Alt + Shift + S`)
2. 좌측 메뉴에서 **SDKs** 클릭
3. JDK 17 선택 → **JDK home path**에 표시된 경로를 복사

이 경로를 터미널 빌드 시 사용하세요:

```bash
# macOS — 복사한 경로를 그대로 사용
./gradlew build -Dorg.gradle.java.home=/복사한/경로

# Windows (PowerShell)
.\gradlew build -Dorg.gradle.java.home="복사한\경로"
```

</details>

---

## 다음 단계

→ [Step 1. Inline Suggestions](../step-01-inline/README.md)

</details>
