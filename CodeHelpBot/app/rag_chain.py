import logging
from pathlib import Path
from typing import Optional

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpoint
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

logger = logging.getLogger(__name__)

DOCS_PATH = "app/docs"
DB_PATH = "app/data/vectorstore"


def build_vectorstore(
    docs_path: str = DOCS_PATH,
    db_path: str = DB_PATH,
) -> Chroma:
    """docs 폴더의 md 파일을 로드해 Chroma 벡터스토어를 생성한다."""
    logger.info("Loading documents from %s", docs_path)

    loader = DirectoryLoader(
        docs_path,
        glob="*.md",
        loader_cls=TextLoader,
        encoding="utf-8",
    )
    docs = loader.load()

    if not docs:
        logger.warning("No documents found in %s", docs_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(docs)

    logger.info("Total chunks created: %d", len(chunks))

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=db_path,
    )
    logger.info("Vectorstore built and persisted to %s", db_path)
    return vectordb


def load_vectorstore(
    db_path: str = DB_PATH,
) -> Optional[Chroma]:
    """이미 생성된 Chroma 벡터스토어를 로드한다."""
    if not Path(db_path).exists():
        logger.error("Vectorstore directory does not exist: %s", db_path)
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings,
    )
    logger.info("Vectorstore loaded from %s", db_path)
    return vectordb


def build_rag_chain() -> RetrievalQA:
    """Chroma + Gemma 기반 RAG RetrievalQA 체인을 구성한다."""
    vectordb = load_vectorstore()
    if vectordb is None:
        # 초기 개발 편의를 위해, 벡터스토어가 없으면 즉석 생성
        logger.warning("Vectorstore not found. Building a new one.")
        vectordb = build_vectorstore()

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 4}
    )

    # Gemma 2B Instruct 엔드포인트
    llm = HuggingFaceEndpoint(
        repo_id="google/gemma-2b-it",
        max_new_tokens=512,
        temperature=0.2,
        top_p=0.9,
    )

    qa_chain: RetrievalQA = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )

    logger.info("RAG RetrievalQA chain created.")
    return qa_chain
