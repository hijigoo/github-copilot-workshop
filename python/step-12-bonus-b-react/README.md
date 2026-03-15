# Bonus B. React.js 프론트엔드 — TODO 앱 UI

> ⏱️ 40분 | 난이도 ⭐⭐ | **체감: "백엔드 API를 소비하는 프론트엔드!"**
>
> 🎯 **목표**: Copilot Agent로 React 프론트엔드를 빠르게 구현

## 📚 사전 준비

- **메인 트랙 Step 08 완료** (또는 Step 06 이상)
- Node.js 18+ 설치
- 백엔드 서버 실행 중 (`uvicorn app.main:app --reload`)

## 🛠️ 기술 스택

| 도구 | 버전 | 용도 |
|------|------|------|
| React | 18+ | UI 프레임워크 |
| TypeScript | 5+ | 타입 안전성 |
| Vite | 5+ | 빌드 도구 |
| Tailwind CSS | 3+ | 스타일링 |

## 📁 폴더 구조

```
todo-frontend/
├── src/
│   ├── api/           ← (실습 중 Copilot으로 생성)
│   ├── components/    ← (실습 중 Copilot으로 생성)
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## 🔧 프로젝트 초기화

터미널에서 실행:

```bash
# 프로젝트 폴더 생성 및 이동
mkdir todo-frontend && cd todo-frontend

# Git 초기화
git init

# Vite + React + TypeScript 프로젝트 생성
npm create vite@latest . -- --template react-ts

# 의존성 설치
npm install

# Tailwind CSS 설치
npm install -D tailwindcss @tailwindcss/vite

# 컴포넌트 디렉터리 생성
mkdir -p src/api src/components
```

### 검증

```bash
npm run dev
```

브라우저에서 `http://localhost:5173` 접속 시 Vite + React 기본 페이지가 보이면 성공! ✅

---

## 🚀 실습 1: 프로젝트 설정 (5분)

### 1-1. Tailwind CSS 설정

**💬 Copilot Agent에게 요청:**
```
이 React + TypeScript + Vite 프로젝트에 Tailwind CSS 설정을 완료해줘.
vite.config.ts에 @tailwindcss/vite 플러그인을 추가하고,
src/index.css에 @import "tailwindcss" 를 추가해줘.
```

### 1-2. 프록시 설정

**💬 Copilot Agent:**
```
vite.config.ts에 프록시를 설정해줘.
/api 로 시작하는 요청은 http://localhost:8000 으로 프록시해야 합니다.
```

**예상 결과 (vite.config.ts):**
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
});
```

---

## 🚀 실습 2: API 클라이언트 생성 (10분)

**💬 Copilot Agent:**
```
백엔드 TODO API에 대한 TypeScript API 클라이언트를 만들어줘.

API 엔드포인트:
- GET /api/v1/todos?page=1&size=10&priority=&q= → TodoListResponse
- POST /api/v1/todos → TodoResponse
- GET /api/v1/todos/:id → TodoResponse
- PATCH /api/v1/todos/:id → TodoResponse
- DELETE /api/v1/todos/:id → 204
- GET /api/v1/categories → CategoryListResponse
- GET /api/v1/stats → StatsResponse

타입 정의와 fetch 함수를 분리해서 만들어줘.
src/api/types.ts 와 src/api/todoApi.ts 로 나눠줘.
```

### 관찰 포인트
- Copilot이 백엔드 스키마와 일치하는 타입을 잘 생성하는지
- 에러 핸들링을 포함하는지

---

## 🚀 실습 3: 컴포넌트 구현 (15분)

### 3-1. TODO 목록 컴포넌트

**💬 Copilot Agent:**
```
TODO 목록을 보여주는 TodoList 컴포넌트를 만들어줘.

기능:
- 할 일 목록 표시 (제목, 우선순위 뱃지, 완료 체크박스)
- 우선순위별 색상 (high: 빨강, medium: 노랑, low: 초록)
- 완료 토글 (체크박스 클릭 시 PATCH 호출)
- 삭제 버튼
- 페이지네이션
- 검색 입력 필드

Tailwind CSS로 스타일링하고 반응형으로 만들어줘.
```

### 3-2. TODO 생성 폼

**💬 Copilot Agent:**
```
새 TODO를 추가하는 AddTodoForm 컴포넌트를 만들어줘.

필드:
- 제목 (필수, 텍스트)
- 설명 (선택, 텍스트)
- 우선순위 (select: low/medium/high)
- 카테고리 (select: API에서 가져온 카테고리 목록)
- 마감일 (date picker)

폼 제출 시 POST /api/v1/todos 호출하고 목록을 새로고침해줘.
```

### 3-3. 통계 대시보드

**💬 Copilot Agent:**
```
Stats 컴포넌트를 만들어줘. GET /api/v1/stats 데이터를 시각적으로 표시해.

- 전체 완료율 (프로그레스 바)
- 우선순위 분포 (간단한 바 차트)
- 카테고리별 통계 (카드 형태)

Chart 라이브러리 없이 Tailwind CSS 만으로 구현해줘.
```

---

## 🚀 실습 4: 페이지 조합 (5분)

**💬 Copilot Agent:**
```
App.tsx를 수정해서 다음 레이아웃을 만들어줘:

1. 상단: 앱 제목 + 통계 요약
2. 좌측: 카테고리 필터 사이드바
3. 중앙: TODO 목록 + 검색 + 페이지네이션
4. 모달: 새 TODO 추가 폼

반응형으로 모바일에서는 사이드바가 숨겨지게.
```

---

## 🔧 백엔드 CORS 설정

프론트엔드(`:5173`)에서 백엔드(`:8000`)로 직접 요청할 경우 CORS 설정이 필요합니다.
Vite 프록시를 사용하면 CORS 없이도 동작하지만, 직접 연동하려면:

**💬 Copilot Agent (FastAPI 프로젝트에서):**
```
FastAPI에 CORS 설정을 추가해줘.
localhost:5173 과 localhost:3000 에서의 요청을 허용해야 해.
CORSMiddleware를 사용해줘.
```

**예상 결과:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚀 실습 5: 통합 테스트 (5분)

### 5-1. 백엔드 실행

```bash
# FastAPI 프로젝트 디렉토리에서
uvicorn app.main:app --reload
```

### 5-2. 프론트엔드 실행

```bash
# todo-frontend 디렉토리에서
npm run dev
```

### 5-3. 동작 확인

브라우저에서 `http://localhost:5173` 접속:

| 확인 항목 | 동작 |
|----------|------|
| 목록 조회 | TODO 목록이 표시되는가? |
| TODO 생성 | 폼에서 제출 시 목록에 추가되는가? |
| 완료 토글 | 체크박스 클릭 시 상태가 변경되는가? |
| 삭제 | 삭제 버튼 클릭 시 목록에서 제거되는가? |
| 검색 | 검색 입력 시 해당 키워드만 표시되는가? |
| 페이지네이션 | 10개 이상일 때 페이지 이동이 동작하는가? |

---

## ✅ 검증 체크리스트

- [ ] `npm run dev` 로 개발 서버 시작 (localhost:5173)
- [ ] 백엔드 API와 연동 성공 (프록시 동작)
- [ ] API 클라이언트 생성 (`src/api/`)
- [ ] TodoList 컴포넌트 구현
- [ ] AddTodoForm 컴포넌트 구현
- [ ] App.tsx에서 전체 레이아웃 조합
- [ ] 백엔드 + 프론트엔드 통합 테스트 성공
- [ ] CRUD 전체 동작 확인

---

## 💡 학습 포인트

| 관찰 항목 | 체크 |
|----------|------|
| Copilot이 TypeScript 타입을 정확히 생성하는가? | |
| React 컴포넌트 분리를 적절히 하는가? | |
| Tailwind 클래스를 올바르게 사용하는가? | |
| API 에러 핸들링을 포함하는가? | |
| 접근성(a11y)을 고려하는가? | |

## 🔗 참고

- [Vite 공식 문서](https://vitejs.dev/)
- [Tailwind CSS 공식 문서](https://tailwindcss.com/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

---

## 다음 단계

→ [Step 13. Spring Boot 백엔드](../step-13-bonus-c-spring/README.md)
