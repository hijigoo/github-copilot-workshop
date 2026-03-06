# Bonus B. React 프론트엔드 — TODO 앱 UI 만들기

> ⏱️ 30분 | 난이도 ⭐⭐ | **체감: "Copilot이 프론트엔드도!"**
>
> 🎯 **목표**: Copilot과 함께 React + TypeScript로 TODO 앱 UI를 만들고 Spring Boot API와 연동하기

---

## 📚 사전 준비

- **메인 트랙 Step 06 이상 완료**
- Node.js 18+ 설치
- Step 06 `complete/` 백엔드 서버 실행 가능

---

## 실습 개요

1. Vite + React + TypeScript 프로젝트 생성
2. Copilot Agent에게 TODO 목록/생성/수정/삭제 UI 구현 요청
3. Spring Boot API(`http://localhost:8080`)와 연동
4. Tailwind CSS로 스타일링

---

## 💬 Copilot Agent 프롬프트 예시

```
Vite + React + TypeScript + Tailwind CSS로 TODO 앱 프론트엔드를 만들어줘.

요구사항:
- Spring Boot API (http://localhost:8080/todos)와 연동
- TODO 목록 표시, 생성, 수정(완료 토글), 삭제
- 우선순위별 필터링
- 페이지네이션
- 반응형 디자인
```

---

## ✅ 체크리스트

- [ ] React 프로젝트 생성 및 실행
- [ ] API 연동하여 CRUD 동작 확인
- [ ] 우선순위 필터링, 페이지네이션 동작
