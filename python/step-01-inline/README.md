# Step 1. 코드 완성 (Inline Suggestions)

> ⏱️ 20분 | 난이도 ⭐
>
> 🎯 **핵심 학습: Tab 자동완성 (Ghost Text)**
>
> **체감: "타이핑이 빨라졌다!"**

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | Step 0 결과 (빈 프로젝트 구조) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

---

## 왜 이게 첫 번째인가?

가장 낮은 진입 장벽입니다.
코드를 치는 도중에 AI가 **회색 텍스트(Ghost Text)**로 제안하는 것을 `Tab`으로 수락하면 됩니다.

---

## 태스크 1: TODO 모델 작성 (5분)

`app/models.py` 파일을 열고, **아래 코드까지만 타이핑**한 뒤 멈추세요:

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    # ← 여기서 멈추고 Tab! Copilot이 나머지 필드를 제안합니다
```

> 📸 **스크린샷**: 회색 Ghost Text로 Copilot이 나머지 필드를 제안하는 모습
> ![Inline Suggestion Ghost Text](./assets/inline-ghost-text.png)

### Copilot 조작법

| 동작 | VS Code (Win/Linux) | VS Code (Mac) | IntelliJ |
|------|-------------------|---------------|----------|
| 제안 수락 | `Tab` | `Tab` | `Tab` |
| 제안 거절 | `Esc` | `Esc` | `Esc` |
| 다른 제안 | `Alt+]` / `Alt+[` | `Option+]` / `Option+[` | `Alt+]` / `Alt+[` |
| 단어 단위 수락 | `Ctrl+→` | `Cmd+→` | — |

### 목표 모델들

- `TodoCreate` — 생성 요청 (title, description?, priority?)
- `TodoResponse` — 응답 (id, title, description, completed, created_at)

> 💡 **팁**: 클래스명 + 필드 1개만 쓰면, Copilot이 나머지를 유추합니다.

---

## 태스크 2: CRUD 엔드포인트 작성 (10분)

`app/main.py` — **한글 주석을 먼저 쓰고** 코드가 따라오는 패턴:

```python
from fastapi import FastAPI, HTTPException
from app.models import TodoCreate, TodoResponse

app = FastAPI(title="TODO API")
todos: list[dict] = []
next_id: int = 1

# 모든 TODO 목록을 반환하는 엔드포인트
# ← 주석을 쓰고 Enter 치면 함수가 자동 생성됩니다!
```

### 만들어야 할 엔드포인트 4개

| Method | Path | 설명 |
|--------|------|------|
| GET | `/todos` | 전체 목록 조회 |
| POST | `/todos` | 새 TODO 생성 |
| PUT | `/todos/{id}` | TODO 수정 |
| DELETE | `/todos/{id}` | TODO 삭제 |

**각 엔드포인트마다**:
1. 한글 주석을 먼저 쓴다
2. `@app.get` or `@app.post` 등을 시작한다
3. Copilot 제안을 `Tab`으로 수락한다
4. 필요하면 수정한다

---

## 태스크 3: 서버 실행 & 수동 테스트 (5분)

```bash
uvicorn app.main:app --reload
```

브라우저에서 [http://localhost:8000/docs](http://localhost:8000/docs) 접속 → Swagger UI

> 📸 **스크린샷**: Swagger UI에서 4개 엔드포인트가 표시된 화면
> ![Swagger UI](./assets/swagger-ui-step01.png)

- POST /todos 로 TODO 생성
- GET /todos 로 목록 확인
- PUT /todos/1 로 수정
- DELETE /todos/1 로 삭제

---

## ✅ 검증 체크리스트

- [ ] Copilot이 모델 필드를 제안했고 수락함
- [ ] 주석 → 함수 패턴으로 엔드포인트 4개 완성
- [ ] `uvicorn` 서버가 정상 실행
- [ ] Swagger UI에서 CRUD 모두 동작

---

## 트러블슈팅

<details>
<summary><strong>🔧 에러가 나면? — Copilot으로 해결하기</strong></summary>

### 방법 1: Copilot Chat에 "에러 고쳐줘"

1. Copilot Chat 열기: `Ctrl+Shift+I` (Mac: `Cmd+Shift+I`)
2. 에러 메시지를 붙여넣고:
   ```
   이 에러 수정해줘: [에러 메시지]
   ```

### 방법 2: 그래도 안 되면

- `complete/` 폴더의 코드와 비교해 보세요
- `complete/` 코드를 복사해서 진행해도 괜찮습니다 — 이번 단계의 목표는 **Inline Suggestion 체험**입니다

</details>

---

## 핵심 인사이트

> **"주석/docstring이 곧 프롬프트다"**
>
> 의도를 명확히 쓸수록 Copilot의 제안이 정확합니다.
> 주석 없이 빈 줄에서 `Tab`을 누르면 엉뚱한 코드가 나올 수 있습니다.

---

## 다음 단계

→ [Step 2. Copilot Chat](../step-02-chat/README.md)
