# Bonus C. Python 마이그레이션 — 같은 API를 Python으로

> ⏱️ 30분 | 난이도 ⭐⭐ | **체감: "Copilot이 언어 전환도 도와준다!"**
>
> 🎯 **목표**: Java Spring Boot로 만든 TODO API를 Python(FastAPI)으로 마이그레이션하며 Copilot의 언어 전환 능력 체험

---

## 📚 사전 준비

- **메인 트랙 Step 06 이상 완료**
- Python 3.11+ 설치

---

## 실습 개요

1. 기존 Java 코드를 `#file`로 참조하여 Python 변환 요청
2. FastAPI + SQLModel로 동일한 API 구현
3. 동일한 엔드포인트/응답 형식 유지
4. pytest로 테스트 작성

---

## 💬 Copilot Agent 프롬프트 예시

```
#file:TodoController.java
#file:TodoService.java
#file:entity/Todo.java
#file:dto/

위 Java Spring Boot 코드를 Python (FastAPI 프레임워크)로 변환해줘.

조건:
- 동일한 API 엔드포인트 (/todos)
- SQLite + SQLModel 사용
- 같은 JSON 응답 형식
- 같은 유효성 검사 규칙
- pytest + TestClient로 테스트 코드도 포함
```

---

## 관찰 포인트

- [ ] Copilot이 Java → Python 패턴 차이를 이해하는가? (ex: @Entity → SQLModel)
- [ ] 에러 핸들링 방식이 적절히 변환되는가?
- [ ] DTO record → Pydantic BaseModel 매핑이 올바른가?
- [ ] 어디서 수동 수정이 필요한가?

---

## ✅ 체크리스트

- [ ] Python FastAPI로 API 변환 완료
- [ ] 동일한 엔드포인트 동작 확인
- [ ] pytest 테스트 통과
