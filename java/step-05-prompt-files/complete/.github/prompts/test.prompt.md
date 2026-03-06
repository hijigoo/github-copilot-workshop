---
agent: "agent"
description: "선택한 모듈에 대한 테스트를 자동 생성합니다"
---
#file:dto/ 의 DTO 스펙을 참조하여,
다음 대상에 대한 테스트를 작성해주세요:
대상: ${input:testTarget}

## 규칙
- JUnit 5 + MockMvc 사용
- @Nested 클래스로 그룹핑
- Given-When-Then 주석 패턴
- 메서드명: test_동작_조건_결과()
- 정상 케이스 / 에러 케이스 / 경계값 각각 최소 1개
- 한국어 주석과 설명
