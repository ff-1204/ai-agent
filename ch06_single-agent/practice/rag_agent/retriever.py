"""검색기와 검색 도구. (교재 6.5절 retriever.py 를 올라마로 옮긴 것)

교재와 다른 점 하나:
    OpenAIEmbeddings(text-embedding-3-small) -> OllamaEmbeddings(bge-m3)

**저장할 때와 찾을 때의 임베딩 모델이 같아야 한다.** 다르면 차원이 안 맞아
검색이 깨지거나 엉뚱한 문서가 나온다.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.tools import create_retriever_tool
from langchain_ollama import OllamaEmbeddings

REPO = Path(__file__).resolve().parents[3]
load_dotenv(REPO / ".env")

DB_PATH = Path(__file__).parent / "chroma_db"  # [ 1 ] 절대 경로로 잡아 실행 위치에 안 흔들리게
BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED = os.getenv("OLLAMA_EMBED_MODEL") or "bge-m3"

vectorstore = Chroma(
    persist_directory=str(DB_PATH),
    embedding_function=OllamaEmbeddings(model=EMBED, base_url=BASE),
    collection_name="study_notes",
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # [ 2 ]

retriever_tool = create_retriever_tool(  # [ 3 ]
    retriever,
    name="notes_search",
    description="AI 에이전트 학습 노트에서 개념·용어·코드 설명을 찾을 때 쓴다. "
    "랭그래프, 도구 호출, MCP, A2A, 메모리 같은 주제를 다룬다.",
)


if __name__ == "__main__":
    print(f"저장된 조각: {vectorstore._collection.count()}개")
    for doc in retriever.invoke("랭그래프에서 State 는 무엇인가?"):
        print(f"\n--- {doc.metadata['source']} #{doc.metadata['page']}")
        print(doc.page_content[:200])
