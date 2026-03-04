# Step 2. Copilot Chat

> ⏱️ 20분 | 난이도 ⭐
>
> 🎯 **핵심 학습: Chat 패널 + `@`, `#`, `/` 명령어**
>
> **체감: "대화로 코드를 다룰 수 있다!"**

---

## 이전 단계 코드

`starter/` = Step 1 완성 코드 (인메모리 CRUD TODO API)

---

## 왜 두 번째인가?

Step 1에서 수동으로 코드를 작성했으니, 이제 **대화**로 코드를 다루는 경험을 합니다.
"검색 + 코딩 + 질문"이 한 곳에서 해결됩니다.

---

## Chat 열기

| IDE | 방법 |
|-----|------|
| VS Code (Win/Linux) | `Ctrl+Shift+I` (또는 좌측 사이드바 Copilot 아이콘) |
| VS Code (Mac) | `Cmd+Shift+I` (또는 좌측 사이드바 Copilot 아이콘) |
| IntelliJ | 우측 사이드바 > GitHub Copilot Chat |

> 📸 **스크린샷**: VS Code에서 Chat 패널이 열린 모습 (Inline과 다른 새로운 인터페이스!)
> ![Copilot Chat 패널](./assets/chat-panel-opened.png)

---

## `@`, `#`, `/` — Chat 명령어 기본 개념

Chat에서는 세 가지 특수 기호를 조합하여 Copilot과 대화합니다.

| 기호 | 역할 | 설명 | 예시 |
|------|------|------|------|
| `@` | **누구에게** (컨텍스트 제공자) | Copilot이 참고할 컨텍스트 범위를 지정합니다 | `@workspace`, `@terminal`, `@vscode` |
| `#` | **무엇을 참고** (파일/선택 영역) | 특정 파일이나 선택 영역을 명시적으로 전달합니다 | `#file:app/main.py`, `#selection` |
| `/` | **무엇을** (액션) | Copilot에게 수행할 작업을 지시합니다 | `/explain`, `/fix`, `/tests` |

### 조합 예시

```
@workspace /explain #file:app/main.py
```
→ "**워크스페이스**를 참고하여, **main.py**를 **설명해줘**"

> 💡 세 기호를 모두 쓸 필요는 없습니다. 필요한 것만 조합하면 됩니다.

---

## 태스크 A: `@` — 프로젝트 맥락 질문 (3분)

Chat에 입력:

```
@workspace 이 프로젝트에 SQLite를 추가하려면 어떻게 해야 하나요?
```

**관찰**: `@workspace`가 프로젝트의 파일 구조와 의존성을 분석하여 맞춤 답변을 합니다.

---

## 태스크 B: `#` — 코드 설명 받기 (3분)

Chat에 입력:

```
/explain #file:app/main.py 한국어로 설명해줘
```

**관찰**: `#file:`로 파일을 지정하면 Copilot이 해당 파일의 구조와 각 엔드포인트의 역할을 한국어로 설명합니다.

> 💡 `/explain`만 쓰면 영어로 답변할 수 있습니다. 뒤에 "한국어로 설명해줘"를 붙이면 한국어로 받을 수 있습니다.

---

## 태스크 C: `/fix` — 버그 수정 (5분)

1. `app/main.py`의 `create_todo` 함수에서 **의도적 버그** 삽입:

```python
# 이 부분을 일부러 잘못 고치세요:
new_todo = {
    "id": next_id,
    "title": todo.description,   # ← 버그! title이 아니라 description
    "completed": True,            # ← 버그! 기본값이 True
}
```

2. 버그가 있는 코드를 선택하고:

```
/fix
```

**관찰**: Copilot이 잘못된 필드 매핑과 기본값을 정확히 찾아냅니다.

---

## 태스크 D: `/tests` — 테스트 코드 생성 (5분)

```
/tests #file:app/main.py
```

**관찰**: Copilot이 `tests/test_main.py` 파일을 생성하며, httpx + pytest 기반 테스트를 작성합니다.

생성된 테스트 실행:

```bash
pytest tests/test_main.py -v
```

---

## IntelliJ 차이점

- Chat 패널은 우측 사이드바에 위치

---

## ✅ 검증 체크리스트

- [ ] `@workspace` 질문에 프로젝트 맥락이 반영된 답변 확인
- [ ] `#file:`로 코드 설명 받음
- [ ] `/fix`로 의도적 버그 수정
- [ ] `/tests`로 테스트 파일 생성 후 `pytest` 통과

---

## 🔧 에러가 나면? — 이 단계에서 배운 기능으로 해결!

이 단계에서 배운 Chat 기능이 바로 디버깅 도구입니다.

### `/fix` 사용하기

에러가 난 파일을 열고 Chat에 입력:
```
/fix #file:app/main.py
```

### 터미널 에러를 Chat에 질문하기

Copilot Chat (`Ctrl+Shift+I` / Mac: `Cmd+Shift+I`)을 열고:
```
터미널에 에러가 났어. 분석해서 수정해줘
```
> Copilot이 터미널 컨텍스트를 자동으로 읽고 원인 분석 + 수정 코드를 제안합니다.

### 에러 메시지를 직접 붙여넣기

```
이 에러 수정해줘:
pytest에서 AssertionError가 나는데, 응답 필드가 expected와 다르대
```

> 💡 `#file:`로 관련 파일을 지정하면 더 정확한 답을 얻습니다.
> 그래도 안 되면 `complete/` 폴더의 코드와 비교해 보세요.

---

## 핵심 인사이트

> **"`#file`로 범위를 좁혀라"**
>
> Copilot에게 프로젝트 전체를 보여주면 답이 흐려집니다.
> `#file:app/main.py` 처럼 관련 파일만 참조하면 훨씬 정확한 답을 얻습니다.

---

## 다음 단계

→ [Step 3. Instructions](../step-03-instructions/README.md)
