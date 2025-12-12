# CodeHelpBot - 개발 컨텍스트 및 기술 사양

## 핵심 파일 구조

app/
├── main.py # FastAPI 앱 + 엔드포인트 (/health, /code-help)
├── rag_chain.py # RAG 체인 (벡터스토어 + Gemma LLM)
├── docs/ # 지식 베이스 문서들 (*.md)
│ └── python_virtualenv.md
├── data/
│ └── vectorstore/ # Chroma 벡터스토어 (자동 생성)
└── init.py # Python 패키지화

**프로젝트 루트**: `requirements.txt`, `.env`, `README.md`

## 데이터 명세

### 1. 입력 데이터 (POST /code-help)
{
"question": "파이썬 가상환경 활성화가 안돼요",
"lang": "python" // 기본값: "python"
}

### 2. 출력 데이터
{
"answer": "가상환경 활성화 오류 해결 방법...",
"sources": [
{
"source": "python_virtualenv.md",
"page_content": "source venv/bin/activate...",
"lang": "python"
}
],
"lang": "python",
"trace_id": "codehelpbot-abc123"
}

### 3. 지식 베이스 (`app/docs/*.md`)
- 형식: `{lang}_{topic}.md` (예: `python_virtualenv.md`)
- 내용: 오류 해결 가이드, 코드 예시, FAQ
- 청크 크기: 800자, 오버랩: 100자

## 기술적 제약 사항

| 항목 | 제약 | 이유 |
|------|------|------|
| **응답 시간** | 5초 내 | Gemma-2B Inference Endpoint 지연 |
| **검색 문서** | 최대 4개 (`k=4`) | 컨텍스트 길이 제한, 비용 최적화 |
| **임베딩** | all-MiniLM-L6-v2 | 속도/정확도 균형 |
| **LLM** | Gemma-2B-IT | 오픈소스, Inference API 지원 |

## 개선 사항 (CURRENT_TASK 통합)

### 완료된 작업
[✔] FastAPI 서버 + CORS + Pydantic 스키마
[✔] RAG 체인: docs → Chroma → Gemma LLM
[✔] LangSmith 트레이싱 (@traceable 데코레이터)
[✔] 5초 타임아웃 + graceful degradation
[✔] 에러 처리 (HTTPException + 로깅)

### 진행 중 / 예정
[ ] 벡터스토어 초기화 스크립트 분리
[ ] Lang 필터링 (python, javascript 등)
[ ] 캐싱 레이어 (Redis)
[ ] 프론트엔드 UI (Streamlit/Next.js)
[ ] 멀티모달 지원 (이미지 코드 분석)

### 모니터링 지표
- LangSmith 대시보드에서 확인 가능

- 첫 번째 토큰 시간 (TTFT): <3초 목표

- 성공률: 85% 이상 (RAGAS 평가)

- 평균 응답 길이: 200~400자

---
*작성일: 2025-12-12 | 버전: v1.0*
