import asyncio
import logging
import os
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain.smith import traceable

from app.rag_chain import build_rag_chain

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# LangSmith 환경 변수 (file.env / .env 에서 로드된다고 가정)
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
# LANGCHAIN_API_KEY=...
# LANGCHAIN_PROJECT="codehelpbot"
LANGSMITH_ENABLED = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

rag_chain = build_rag_chain()

app = FastAPI(title="CodeHelpBot API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요시 프론트 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeHelpRequest(BaseModel):
    question: str
    lang: str = "python"


class CodeHelpResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    lang: str
    trace_id: str | None = None


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """헬스 체크 엔드포인트."""
    return {"status": "ok"}


@traceable  # LangSmith 트레이싱용
def _run_rag_sync(query: str) -> Dict[str, Any]:
    """동기 RAG 체인 호출 함수 (LangSmith 트레이싱 대상)."""
    return rag_chain({"query": query})


@app.post("/code-help", response_model=CodeHelpResponse)
async def code_help(request: CodeHelpRequest) -> CodeHelpResponse:
    """
    코드 질문을 받아 RAG 기반으로 답변을 생성하는 엔드포인트.
    - 입력: question(필수), lang(기본 python)
    - 출력: answer, sources 메타데이터, lang, trace_id
    """
    try:
        # 응답 시간 제한: 5초
        result = await asyncio.wait_for(
            asyncio.to_thread(_run_rag_sync, request.question),
            timeout=5.0,
        )
    except asyncio.TimeoutError:
        # 타임아웃 기본 응답
        logger.warning("RAG chain timeout for question: %s", request.question)
        return CodeHelpResponse(
            answer=(
                "요청 처리 시간이 5초를 초과했습니다. "
                "질문을 조금 더 구체적으로 나눠서 다시 시도해 주세요."
            ),
            sources=[],
            lang=request.lang,
            trace_id=None,
        )
    except Exception as exc:
        logger.exception("Error while running RAG chain: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="코드 도움을 생성하는 중 오류가 발생했습니다.",
        ) from exc

    answer: str = result.get("result", "")
    source_docs = result.get("source_documents", [])

    sources: List[Dict[str, Any]] = [
        getattr(doc, "metadata", {}) for doc in source_docs
    ]

    # LangSmith는 trace_id를 환경에 따라 자동 관리하므로,
    # 여기서는 단순히 필드만 둬서 확장 여지를 남겨둔다.
    trace_id: str | None = None
    if LANGSMITH_ENABLED:
        # 실제 프로덕션에서는 컨텍스트에서 trace_id를 꺼내 세팅할 수 있음.
        trace_id = os.getenv("LANGCHAIN_PROJECT", "codehelpbot")

    return CodeHelpResponse(
        answer=answer,
        sources=sources,
        lang=request.lang,
        trace_id=trace_id,
    )
