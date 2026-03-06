---
agent: "agent"
description: "스펙 기반으로 DTO → 테스트 → 구현을 순서대로 수행합니다"
---
다음 기능을 Spec-Driven Development로 구현해주세요:
기능: ${input:featureDescription}

## 순서 (반드시 이 순서대로!)
1. **SPEC**: dto/ 패키지에 DTO record 추가
2. **TEST**: test/에 테스트 작성 (실패하는 상태)
3. **IMPL**: controller/ 에 구현 코드 작성
4. **VERIFY**: ./gradlew test로 전체 테스트 통과 확인

## 참고 파일
#file:dto/
