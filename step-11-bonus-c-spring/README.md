# Bonus C. Spring Boot 백엔드 — 같은 TODO API를 Java로

> ⏱️ 40분 | 난이도 ⭐⭐ | **체감: "같은 API를 다른 언어로!"**
>
> 🎯 **목표**: Python FastAPI 프로젝트를 Spring Boot로 재구현하며 Copilot의 다중 언어 지원 체험

## 📚 사전 준비

- **메인 트랙 Step 04 이상 완료** (API 스펙 이해)
- JDK 17+ 설치
- IntelliJ IDEA (권장) 또는 VS Code + Java Extension Pack
- Gradle 또는 Maven

## 🛠️ 기술 스택

| 도구 | 버전 | 용도 |
|------|------|------|
| Spring Boot | 3.x | 웹 프레임워크 |
| Spring Web | - | REST API |
| Spring Data JPA | - | ORM |
| H2 Database | - | 인메모리 DB |
| Lombok | - | 보일러플레이트 감소 |
| JDK | 17+ | Java 런타임 |

---

## 🔧 프로젝트 초기화

터미널에서 실행:

```bash
# 프로젝트 폴더 생성 및 이동
mkdir todo-api && cd todo-api

# Git 초기화
git init

# Spring Initializr로 프로젝트 생성 (curl 사용)
curl https://start.spring.io/starter.zip \
  -d type=gradle-project \
  -d language=java \
  -d bootVersion=3.4.3 \
  -d baseDir=. \
  -d groupId=com.workshop \
  -d artifactId=todo-api \
  -d name=todo-api \
  -d packageName=com.workshop.todoapi \
  -d javaVersion=17 \
  -d dependencies=web,data-jpa,h2,lombok,validation \
  -o todo-api.zip

# 압축 해제 및 정리
unzip todo-api.zip
rm todo-api.zip

# 프로젝트 디렉터리 구조 생성
mkdir -p src/main/java/com/workshop/todoapi/{entity,repository,dto,service,controller,exception}
mkdir -p src/test/java/com/workshop/todoapi
```

> 💡 또는 [start.spring.io](https://start.spring.io/) 에서 위와 동일한 설정으로 직접 생성할 수도 있습니다.

### 검증

```bash
./gradlew bootRun
```

브라우저에서 `http://localhost:8080` 접속 시 Whitelabel Error Page가 보이면 성공! ✅
(아직 컨트롤러가 없으므로 에러 페이지가 정상입니다)

### 프로젝트 구조 (초기화 후)

```
todo-api/
├── build.gradle
├── settings.gradle
├── gradlew / gradlew.bat
├── src/
│   ├── main/
│   │   ├── java/com/workshop/todoapi/
│   │   │   ├── TodoApiApplication.java
│   │   │   ├── entity/
│   │   │   ├── repository/
│   │   │   ├── dto/
│   │   │   ├── service/
│   │   │   ├── controller/
│   │   │   └── exception/
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/com/workshop/todoapi/
│           └── TodoApiApplicationTests.java
└── gradle/
```

---

## 🚀 실습 1: 프로젝트 설정

### 1-1. Spring Initializr 프로젝트 확인

프로젝트 초기화가 완료되었으면 `todo-api/` 디렉터리에서 진행합니다.

**💬 Copilot Chat:**
```
Spring Boot 프로젝트의 구조와 각 파일의 역할을 설명해줘.
```

### 1-2. application.yml 설정

**💬 Copilot Inline:**
```yaml
# src/main/resources/application.yml
# H2 인메모리 DB, 콘솔 활성화, JPA 설정을 작성해줘
```

**예상 결과:**
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:tododb
    driver-class-name: org.h2.Driver
  h2:
    console:
      enabled: true
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true

server:
  port: 8080
```

---

## 🚀 실습 2: Entity & Repository

### 2-1. Todo Entity

**💬 Copilot Agent:**
```
Python의 Todo 모델을 참고해서 JPA Entity를 만들어줘.

Python Todo 모델:
- id: int (PK, auto)
- title: str (not null)
- description: str (nullable)
- priority: str (default "medium", values: low/medium/high)  
- completed: bool (default false)
- created_at: datetime
- updated_at: datetime
- due_date: str (nullable, "YYYY-MM-DD")

패키지: com.workshop.todoapi.entity
Lombok 어노테이션도 사용해줘.
```

### 2-2. Todo Repository

**💬 Copilot Inline** (`TodoRepository.java` 파일 생성 후):
```java
// JpaRepository를 상속하는 TodoRepository
// 우선순위로 필터링, 완료 여부 필터링, 제목 검색 메서드 포함
```

---

## 🚀 실습 3: DTO & Service

### 3-1. Request/Response DTO

**💬 Copilot Agent:**
```
Python의 Pydantic 스키마를 참고해서 Java DTO를 만들어줘.

필요한 DTO:
1. TodoCreateRequest (title 필수, description/priority/due_date 선택)
2. TodoUpdateRequest (모든 필드 선택)
3. TodoResponse (전체 필드)
4. TodoListResponse (items, total, page, size)

Jakarta Validation 어노테이션을 사용해줘:
- title: @NotBlank, @Size(max=200)
- description: @Size(max=1000)
- priority: @Pattern으로 low/medium/high만 허용
```

### 3-2. TodoService

**💬 Copilot Agent:**
```
TodoService를 만들어줘.

메서드:
- createTodo(TodoCreateRequest) → TodoResponse
- getTodoById(Long id) → TodoResponse
- listTodos(int page, int size, String priority) → TodoListResponse
- updateTodo(Long id, TodoUpdateRequest) → TodoResponse
- deleteTodo(Long id) → void

존재하지 않는 TODO는 ResourceNotFoundException을 던져줘.
```

---

## 🚀 실습 4: Controller

**💬 Copilot Agent:**
```
TodoController를 만들어줘.
FastAPI 버전과 동일한 API 경로를 사용해:

- POST   /api/v1/todos      → 201 Created
- GET    /api/v1/todos       → 200 (페이지네이션: page, size 파라미터)
- GET    /api/v1/todos/{id}  → 200
- PATCH  /api/v1/todos/{id}  → 200
- DELETE /api/v1/todos/{id}  → 204 No Content

@Valid로 입력 검증하고,
@RestControllerAdvice로 글로벌 예외 처리도 추가해줘.
```

---

## 🚀 실습 5: 테스트

**💬 Copilot Agent:**
```
TodoController 통합 테스트를 만들어줘.
@SpringBootTest + @AutoConfigureMockMvc 사용.

테스트 케이스:
1. TODO 생성 성공 (201)
2. 빈 제목으로 생성 실패 (400)
3. TODO 조회 (200)
4. 존재하지 않는 TODO 조회 (404)
5. TODO 목록 페이지네이션
6. TODO 수정 (200)
7. TODO 삭제 (204)
```

---

## 🎯 비교 포인트: Python vs Java

| 항목 | FastAPI (Python) | Spring Boot (Java) |
|------|-----------------|-------------------|
| 모델 정의 | SQLModel | JPA Entity + Lombok |
| 유효성 검사 | Pydantic Field() | Jakarta @Valid |
| 라우팅 | `@app.get()` | `@GetMapping()` |
| DI | `Depends()` | `@Autowired` / 생성자 주입 |
| 테스트 | pytest + TestClient | JUnit + MockMvc |
| 응답 코드 | `status_code=201` | `@ResponseStatus(CREATED)` |
| DB 세션 | Session 제너레이터 | `@Transactional` |

---

## ✅ 검증 체크리스트

- [ ] Spring Boot 프로젝트 생성 완료
- [ ] H2 콘솔 접속 가능 (http://localhost:8080/h2-console)
- [ ] POST /api/v1/todos → 201 Created
- [ ] GET /api/v1/todos → 페이지네이션 동작
- [ ] GET /api/v1/todos/{id} → 200 OK
- [ ] PATCH /api/v1/todos/{id} → 부분 업데이트
- [ ] DELETE /api/v1/todos/{id} → 204 No Content
- [ ] 유효성 검사 실패 시 400/422 응답
- [ ] 통합 테스트 전체 통과

---

## 💡 학습 포인트

| 관찰 항목 | 체크 |
|----------|------|
| Copilot이 Java 보일러플레이트를 얼마나 줄여주는가? | |
| Python 코드를 참고로 제공하면 변환 품질이 높아지는가? | |
| Instructions를 Java 맥락으로 수정하면 도움이 되는가? | |
| Spring의 어노테이션을 올바르게 사용하는가? | |

## 🔗 참고

- [Spring Boot 공식 가이드](https://spring.io/guides)
- [Spring Data JPA 문서](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Spring Initializr](https://start.spring.io/)
