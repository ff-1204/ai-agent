"""저장소의 학습 노트를 벡터 저장소로 만든다. (6.5절 실습)

    python ch06_single-agent/practice/rag_agent/build_index.py          # 5·6장만 (기본)
    python ch06_single-agent/practice/rag_agent/build_index.py --all    # 전체 장

교재는 `datasets/한글맞춤법 표준어규정 해설.pdf` 를 쓰지만 그 PDF 는 저장소에
없다(저작권 자료라 저자가 제외). 대신 **이 저장소의 한국어 학습 노트**를 지식
문서로 쓴다. 분할 -> 임베딩 -> 저장 순서는 교재와 같다.

교재와 다른 점 둘:
    - 임베딩: OpenAIEmbeddings(text-embedding-3-small, 1536차원)
              -> OllamaEmbeddings(bge-m3, 1024차원)
    - 원본:   PDF 264쪽 -> .md 노트 48개

**차원이 다르면 저장소를 다시 만들어야 한다.** 임베딩 모델을 바꾸면
chroma_db 폴더를 지우고 이 스크립트를 다시 돌린다.
"""

import os
import shutil
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

REPO = Path(__file__).resolve().parents[3]
load_dotenv(REPO / ".env")

DB_PATH = Path(__file__).parent / "chroma_db"
COLLECTION = "study_notes"
BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED = os.getenv("OLLAMA_EMBED_MODEL") or "bge-m3"


# 기본은 5·6장만 쓴다. 전부 넣으면 CPU 임베딩이 한 시간 가까이 걸린다
# (1,225조각 · 약 0.4조각/초). 전체를 넣으려면 --all 을 붙인다.
DEFAULT_CHAPTERS = ("ch05_langgraph-basics", "ch06_single-agent")


def load_notes(all_chapters: bool = False) -> list[Document]:
    """절 노트를 읽는다. README 와 examples/ 는 뺀다."""
    pattern = "ch*/*.md" if all_chapters else None
    paths = []
    if all_chapters:
        paths = sorted(REPO.glob(pattern))
    else:
        for ch in DEFAULT_CHAPTERS:
            paths.extend(sorted((REPO / ch).glob("*.md")))

    docs = []
    for md in paths:
        if md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": md.name}))
    return docs


def main() -> None:
    all_chapters = "--all" in sys.argv
    pages = load_notes(all_chapters)
    scope = "전체 장" if all_chapters else " · ".join(DEFAULT_CHAPTERS)
    print(f"노트 {len(pages)}개 읽음  ({scope})")

    # 교재와 같은 설정 (6.5절)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(pages)

    # 교재 코드가 metadata['page'] 를 쓰므로 조각 번호를 그 자리에 넣어 준다.
    for i, d in enumerate(docs):
        d.metadata["page"] = i

    print(f"조각 {len(docs)}개로 분할 (chunk_size=500, overlap=50)")

    if DB_PATH.exists():
        shutil.rmtree(DB_PATH)
        print("기존 chroma_db 삭제 (차원이 바뀌면 재사용할 수 없다)")

    store = Chroma(
        persist_directory=str(DB_PATH),
        embedding_function=OllamaEmbeddings(model=EMBED, base_url=BASE),
        collection_name=COLLECTION,
    )

    # CPU 임베딩은 느리다. 배치로 나눠 넣고 진행률을 찍는다.
    print(f"임베딩 중… 모델 {EMBED} @ {BASE}", flush=True)
    BATCH = 32
    t0 = time.perf_counter()
    for i in range(0, len(docs), BATCH):
        store.add_documents(docs[i : i + BATCH])
        done = min(i + BATCH, len(docs))
        el = time.perf_counter() - t0
        eta = el / done * (len(docs) - done)
        print(
            f"  {done:5}/{len(docs)}  ({done / len(docs):5.1%})  "
            f"경과 {el / 60:5.1f}분  남음 약 {eta / 60:5.1f}분",
            flush=True,
        )

    print(f"완료: {store._collection.count()}개 저장 -> {DB_PATH}")
    print(f"총 {(time.perf_counter() - t0) / 60:.1f}분")


if __name__ == "__main__":
    main()
