# 데이터 모델

## Todo
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| id | integer | 자동 | 고유 식별자 |
| title | string (1~200자) | ✅ | 할일 제목 |
| description | string (최대 1000자) | ❌ | 상세 설명 |
| priority | enum (LOW, MEDIUM, HIGH) | ❌ | 우선순위 (기본: MEDIUM) |
| completed | boolean | ❌ | 완료 여부 (기본: false) |
| created_at | datetime | 자동 | 생성 시각 |
| updated_at | datetime | 자동 | 수정 시각 (수정 시 갱신) |

## 저장소
- 현재 단계: 인메모리 딕셔너리 (Step 7에서 SQLite로 전환 예정)
