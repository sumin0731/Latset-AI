# CURRENT TASK: FastAPI + RAG 코드 질문 API 고도화

## 현재 태스크

`app/main.py`와 `app/rag_chain.py`를 이용해 **RAG 기반 코드 질문 API**를 완성하고, LangSmith 트레이싱과 타임아웃 처리까지 적용한다.

## 완료되어야 할 기능

1. FastAPI 서버 기본 구조
   - `app/main.py`에서 FastAPI 앱 초기화
   - CORS 미들웨어 설정 (개발 단계에서는 `["*"]` 허용 가능)
   - `GET /health` → `{"status": "ok"}` 응답

2. 코드 질문 API (`POST /code-help`)
   - 엔드포인트: `POST /code-help`
   - 요청 스키마: `CodeHelpRequest`
     - `question: str` (필수)
     - `lang: str = "python"` (기본값)
   - 응답 스키마: `CodeHelpResponse`
     - `answer: str`
     - `sources: List[Dict[str, Any]]`  (참조 문서 메타데이터)
     - `lang: str`
     - `trace_id: Optional[str]` (LangSmith 연동용 필드)

3. RAG 체인 연동
   - `app/rag_chain.py`에서:
     - `build_vectorstore()`로 `app/docs` 폴더의 md 파일 로드 → 분할 → 임베딩 → Chroma 벡터스토어 생성
     - `load_vectorstore()`로 기존 벡터스토어 로드
     - `build_rag_chain()`에서 Chroma + Gemma LLM 조합으로 `RetrievalQA` 체인 생성
   - `app/main.py`에서:
     - 서버 시작 시 `rag_chain = build_rag_chain()`으로 체인 준비
     - `/code-help`에서 `rag_chain({"query": request.question})` 호출

4. LangSmith 트레이싱 + 타임아웃 처리
   - LangSmith 환경 변수:
     - `LANGCHAIN_TRACING_V2=true`
     - `LANGCHAIN_ENDPOINT=https://api.smith.langchain.com`
     - `LANGCHAIN_API_KEY=...`
     - `LANGCHAIN_PROJECT=codehelpbot`
   - `_run_rag_sync()` 함수에 `@traceable` 데코레이터 적용
   - `/code-help` 엔드포인트에서:
     - `asyncio.wait_for(asyncio.to_thread(...), timeout=5.0)` 사용
     - `TimeoutError` 발생 시:
       - 기본 안내 메시지 + 빈 `sources`로 응답
     - 기타 예외는 `HTTPException(status_code=500, ...)`으로 변환

## 예상 결과 예시

curl -X POST http://localhost:8000/code-help
-H "Content-Type: application/json"
-d '{"question": "파이썬 가상환경 에러가 나요", "lang": "python"}'
→ 예시 응답 구조:

{
"answer": "...에러 원인과 해결 방법에 대한 요약...",
"sources": [
{"source": "python_virtualenv.md", "lang": "python", "tags": ["env", "setup"]}
],
"lang": "python",
"trace_id": "codehelpbot" // 또는 실제 트레이스 ID
}