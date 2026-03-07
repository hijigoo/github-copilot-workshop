---
agent: "agent"
description: "기존 패턴에 맞춰 새 API 엔드포인트를 추가합니다"
---
다음 기능에 대한 API 엔드포인트를 추가해주세요:

기능: ${input:featureDescription}

## 순서 (반드시 이 순서대로!)
1. **DTO**: dto/ 패키지에 필요한 요청/응답 DTO record 추가
2. **Controller**: TodoController에 엔드포인트 메서드 추가
3. **TEST**: test/에 새 엔드포인트에 대한 테스트 작성
4. **VERIFY**: ./gradlew test로 전체 테스트 통과 확인

## 참고 파일
#file:dto/
#file:TodoController.java
