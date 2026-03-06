# Bonus D. Chat Debug View — AI 대화 디버깅

> ⏱️ 15분 | 난이도 ⭐~⭐⭐ | **체감: "Copilot이 왜 이렇게 답했는지 직접 들여다본다!"**
>
> 🎯 **목표**: Chat Debug View로 Copilot의 내부 동작(System Prompt, Context, Tool 호출 등)을 직접 확인하는 방법 체험

---

## 📚 사전 준비

- **메인 트랙 Step 02 이상 완료** (Copilot Chat 사용법 숙지)
- IntelliJ IDEA + GitHub Copilot 플러그인 설치 완료

> 💡 Chat Debug View는 현재 VS Code에서 지원됩니다. IntelliJ에서는 VS Code를 추가로 사용하거나, IntelliJ의 Copilot 로그를 확인하는 방식으로 대체할 수 있습니다.

---

## 실습 개요

1. VS Code에서 `Developer: Show Chat Debug View` 열기
2. System Prompt, User Prompt, Context, Response, Tool responses 확인
3. Instructions 적용 여부 확인
4. 컨텍스트 누락 진단

> 상세 실습 가이드는 [Python 버전의 Step 13](../../python/step-13-bonus-d-debug/README.md)를 참고하세요.
> IDE에 따라 접근 방식만 다를 뿐, 핵심 개념은 동일합니다.

---

## ✅ 체크리스트

- [ ] Chat Debug View를 열어 각 섹션 확인
- [ ] Instructions가 System Prompt에 포함되는지 확인
- [ ] `#file:` 멘션이 Context에 올바르게 포함되는지 확인

---

## 🔗 참고 링크

- [VS Code 공식 문서 — Debug chat interactions](https://code.visualstudio.com/docs/copilot/chat/chat-debug-view)
