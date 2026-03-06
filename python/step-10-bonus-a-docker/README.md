# Bonus A. Docker — Copilot으로 컨테이너화하기

> ⏱️ 30분 | 난이도 ⭐⭐ | **체감: "Copilot이 Docker 설정도 척척!"**
>
> 🎯 **목표**: Copilot Agent를 활용해 TODO 앱을 Docker로 컨테이너화하고 docker-compose로 실행하기

---

## 📚 사전 준비

- **메인 트랙 Step 06 이상 완료** (Agent 모드 사용법 숙지)
- VS Code + GitHub Copilot 확장 설치 완료
- Docker Desktop 설치 및 실행 중
- Step 06 `complete/` 코드 사용 (또는 본인이 작업 중인 코드)

---

## 📖 배경 지식: 왜 Docker인가?

| 항목 | 설명 |
|------|------|
| **환경 일관성** | "내 PC에서는 되는데…" 문제 해결 |
| **배포 단순화** | 이미지 하나로 어디서든 실행 |
| **격리** | 호스트 환경과 독립적으로 애플리케이션 실행 |
| **확장성** | docker-compose로 멀티 서비스 구성 용이 |

> 💡 Copilot은 Dockerfile, docker-compose.yml, .dockerignore 등의 패턴을 잘 이해합니다. 프로젝트 코드를 컨텍스트로 제공하면 더 정확한 설정을 생성합니다.

---

## 🐳 실습 1: Dockerfile 생성 (10분)

> TODO 앱을 위한 Dockerfile을 Copilot에게 만들어 달라고 합니다.

### 1-1. Copilot Agent에게 요청

**💬 Copilot Agent:**
```
#file:step-05-agent/complete/app/main.py
#file:step-05-agent/complete/requirements.txt

위 Python FastAPI TODO 앱을 위한 Dockerfile을 만들어줘.

요구사항:
- Python 3.11 slim 베이스 이미지
- 멀티스테이지 빌드
- 비루트 사용자로 실행
- 헬스 체크 포함
- .dockerignore 도 만들어줘
```

### 1-2. 생성된 Dockerfile 확인

Copilot이 생성한 Dockerfile에서 다음 항목을 확인합니다:

| 확인 항목 | 기대 내용 |
|----------|----------|
| 베이스 이미지 | `python:3.11-slim` |
| 의존성 설치 | `requirements.txt` 먼저 복사 후 `pip install` (캐시 활용) |
| 비루트 사용자 | `USER` 지시어로 루트가 아닌 사용자 설정 |
| HEALTHCHECK | `/health` 엔드포인트를 활용한 헬스 체크 |
| EXPOSE | 8000 포트 |

### 1-3. 이미지 빌드 및 실행

```bash
# step-05-agent/complete 디렉토리에서 실행
cd step-05-agent/complete

# Docker 이미지 빌드
docker build -t todo-api .

# 컨테이너 실행
docker run -d -p 8000:8000 --name todo-app todo-api

# 동작 확인
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/todos

# 정리
docker stop todo-app && docker rm todo-app
```

### 관찰 포인트
- [ ] Copilot이 보안 모범 사례를 따르는가? (비루트 사용자 등)
- [ ] 멀티스테이지 빌드를 올바르게 구성했는가?
- [ ] .dockerignore에 적절한 파일이 포함되어 있는가? (`__pycache__`, `.git`, `*.db` 등)

---

## 🏗️ 실습 2: docker-compose.yml 생성 (10분)

> 멀티 서비스 환경을 docker-compose로 구성합니다.

### 2-1. Copilot Agent에게 요청

**💬 Copilot Agent:**
```
docker-compose.yml을 만들어줘.

서비스:
1. api: FastAPI TODO 앱 (포트 8000)
2. postgres: PostgreSQL DB (SQLite 대신)

설정:
- 환경 변수로 DB URL 주입
- 볼륨 마운트로 데이터 영속화
- 네트워크 설정
- depends_on + healthcheck
```

### 2-2. 생성된 docker-compose.yml 확인

| 확인 항목 | 기대 내용 |
|----------|----------|
| services | `api`, `postgres` 두 서비스 정의 |
| depends_on | `api`가 `postgres`에 의존 (healthcheck 조건) |
| volumes | PostgreSQL 데이터 영속화 볼륨 |
| environment | `DATABASE_URL` 환경 변수 |
| healthcheck | 각 서비스에 헬스 체크 설정 |
| networks | 서비스 간 통신을 위한 네트워크 |

### 2-3. 실행 및 확인

```bash
# 빌드 & 실행
docker-compose up --build

# 다른 터미널에서 확인
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/todos

# 종료
docker-compose down
```

### 관찰 포인트
- [ ] 환경 변수가 올바르게 분리되어 있는가?
- [ ] 볼륨 마운트가 데이터를 영속화하는가?
- [ ] `depends_on`과 healthcheck가 올바르게 설정되어 있는가?

---

## 🔧 실습 3: Docker 설정 개선 (10분)

> Copilot에게 추가적인 Docker 설정 개선을 요청합니다.

### 3-1. 개발환경용 docker-compose 오버라이드

**💬 Copilot Agent:**
```
개발환경용 docker-compose.override.yml을 만들어줘.

요구사항:
- 소스 코드 볼륨 마운트 (핫 리로드)
- uvicorn --reload 모드로 실행
- 디버그 포트 노출
- .env 파일 로드
```

### 3-2. 프로덕션용 최적화 요청

**💬 Copilot Agent:**
```
프로덕션 배포를 위해 Dockerfile을 최적화해줘.

요구사항:
- 이미지 크기 최소화
- 보안 강화 (불필요한 패키지 제거)
- gunicorn + uvicorn worker 구성
- 적절한 레이블(LABEL) 추가
```

### 3-3. 결과 비교

| 항목 | 개발용 | 프로덕션용 |
|------|--------|-----------|
| 소스 마운트 | 볼륨 마운트 (핫 리로드) | COPY (이미지에 포함) |
| 서버 | uvicorn --reload | gunicorn + uvicorn worker |
| 디버그 | 포트 노출 | 최소 포트만 노출 |
| 이미지 크기 | 개발 도구 포함 | 최소화 |

### 관찰 포인트
- [ ] 개발/프로덕션 환경 분리가 명확한가?
- [ ] Copilot이 환경별 차이점을 이해하고 있는가?
- [ ] gunicorn 설정이 적절한가?

---

## ✅ 전체 체크리스트

- [ ] Dockerfile 생성 및 이미지 빌드 성공
- [ ] .dockerignore 파일 생성
- [ ] docker-compose.yml로 멀티 서비스 실행
- [ ] 헬스 체크가 정상 동작
- [ ] 개발/프로덕션 환경 분리 설정
- [ ] 볼륨 마운트로 데이터 영속화 확인

---

## 💡 핵심 인사이트

- **컨텍스트가 핵심**: `#file`로 `requirements.txt`와 `main.py`를 함께 제공하면, Copilot이 의존성과 엔트리포인트를 정확히 파악해 더 나은 Dockerfile을 생성합니다.
- **보안은 반드시 검토**: Copilot은 Dockerfile 패턴을 잘 알지만, 비루트 사용자 실행, 시크릿 관리 등 보안 설정은 항상 직접 검토하세요.
- **환경 분리**: docker-compose.override.yml 패턴을 활용하면 하나의 기본 설정으로 개발/프로덕션 환경을 깔끔하게 분리할 수 있습니다.

---

## 🔗 참고 링크

- [Docker 공식 문서 — Dockerfile 베스트 프랙티스](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [FastAPI 공식 문서 — Docker 배포](https://fastapi.tiangolo.com/deployment/docker/)
