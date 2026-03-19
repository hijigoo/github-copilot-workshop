---
name: java-junit
description: 'JUnit 5 단위 테스트 및 데이터 기반 테스트 모범 사례'
---

# JUnit 5+ 모범 사례

목표는 JUnit 5를 사용하여 효과적인 단위 테스트를 작성하는 것이며, 일반 테스트와 데이터 기반 테스트를 모두 포함합니다.

## 프로젝트 설정

- 표준 Maven 또는 Gradle 프로젝트 구조를 사용합니다.
- 테스트 소스 코드는 `src/test/java`에 위치시킵니다.
- 다음 의존성을 포함합니다:
  - `junit-jupiter-api`
  - `junit-jupiter-engine`
  - `junit-jupiter-params` (파라미터화 테스트용)
- 테스트 실행:
  - Maven: `mvn test`
  - Gradle: `gradle test`

## 테스트 구조

- 테스트 클래스 이름은 `Test`로 끝나야 합니다. (예: `CalculatorTest`)
- 테스트 메서드에는 `@Test`를 사용합니다.
- Arrange-Act-Assert (AAA) 패턴을 따릅니다.
- 테스트 이름은 다음과 같은 형식을 권장합니다:
  - `methodName_should_expectedBehavior_when_scenario`
- `@BeforeEach`, `@AfterEach`를 사용해 각 테스트 전후 처리를 수행합니다.
- `@BeforeAll`, `@AfterAll`은 클래스 단위로 실행되며 static 메서드여야 합니다.
- `@DisplayName`으로 사람이 읽기 쉬운 테스트 이름을 지정할 수 있습니다.

## 일반 테스트

- 하나의 테스트는 하나의 동작만 검증해야 합니다.
- 하나의 테스트 메서드에서 여러 조건을 검증하지 않습니다.
- 테스트는 서로 독립적이고 반복 실행 가능해야 합니다.
- 테스트 간 의존성을 피해야 합니다.

## 데이터 기반 (파라미터화) 테스트

- `@ParameterizedTest`를 사용합니다.
- 간단한 값:
  - `@ValueSource`
- 복잡한 데이터:
  - `@MethodSource` (Stream, Collection 등 반환)
- CSV 데이터:
  - `@CsvSource` (인라인)
  - `@CsvFileSource` (파일)
- Enum:
  - `@EnumSource`

## Assertions (검증)

- `org.junit.jupiter.api.Assertions`의 static 메서드 사용:
  - `assertEquals`, `assertTrue`, `assertNotNull` 등
- 가독성을 위해 AssertJ 사용 가능:
  - `assertThat(...).is...`
- 예외 테스트:
  - `assertThrows`
  - `assertDoesNotThrow`
- 여러 검증:
  - `assertAll`
- 실패 시 이해를 돕기 위해 메시지를 포함합니다.

## Mocking 및 격리

- Mockito 같은 mocking 프레임워크를 사용합니다.
- `@Mock`, `@InjectMocks`로 객체 생성 및 주입을 간소화합니다.
- 인터페이스 기반 설계를 통해 mocking을 쉽게 합니다.

## 테스트 구성

- 기능 또는 컴포넌트별로 패키지를 구성합니다.
- `@Tag`를 사용해 테스트 분류:
  - `@Tag("fast")`
  - `@Tag("integration")`
- 실행 순서 제어 (필요 시):
  - `@TestMethodOrder`
  - `@Order`
- 테스트 비활성화:
  - `@Disabled` (사유 포함)
- 구조화:
  - `@Nested`로 테스트 그룹화
