# CodeHelpBot - RAG 기반 코드 질문 API

## 개요 및 목적

**CodeHelpBot**은 LangChain RAG(Retrieval Augmented Generation) 기술을 활용해 프로그래밍 오류와 코드 질문을 자동으로 해결해주는 AI API 서버입니다.

### 목적

- 개발자들이 자주 겪는 **코드 오류 해결**을 자동화
- `docs/` 폴더의 지식 베이스를 기반으로 **정확하고 구체적인 답변** 제공
- LangSmith를 통한 **실행 추적 및 품질 모니터링**으로 지속적 개선

## 기술 스택

Backend: FastAPI + Uvicorn
AI Pipeline: LangChain + Chroma + Gemma-2B
Embedding: sentence-transformers/all-MiniLM-L6-v2
Observability: LangSmith
Data: Markdown 문서 → 벡터스토어

## 설치 방법

1. **가상환경 생성**
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

2. **패키지 설치**
pip install -r requirements.txt

3. **환경변수 설정** (`.env` 또는 `file.env`)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your_langsmith_key"
LANGCHAIN_PROJECT="codehelpbot"

## 실행 방법

1. **지식 베이스 준비**
   - `app/docs/`에 코드 관련 문서(`*.md`) 추가

2. **서버 실행**
uvicorn app.main:app --reload --port 8000

3. **API 테스트**
헬스 체크
curl http://localhost:8000/health

코드 질문
curl -X POST http://localhost:8000/code-help
-H "Content-Type: application/json"
-d '{"question": "파이썬 가상환경 활성화 에러", "lang": "python"}'

## 제공 기능

| 엔드포인트 | 방법 | 기능 | 응답 예시 |
|------------|------|------|-----------|
| `/health` | GET | 서버 상태 확인 | `{"status": "ok"}` |
| `/code-help` | POST | RAG 기반 코드 Q&A | `{"answer": "...", "sources": [...], "lang": "python"}` |

**요청 형식**: `{"question": "질문", "lang": "python"}` (lang 기본값: python)

## GitHub 링크

📂 Repository: [https://github.com/sm0731/](https://github.com/sumin0731/Latset-AI/blob/main/CodeHelpBot)

---
*작성일: 2025-12-12*
