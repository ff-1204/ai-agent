"""이 실습이 쓰는 LLM 한 곳. (교재에는 없는 파일)

교재는 nodes.py 와 edges.py 에서 각각 `ChatOpenAI(model="gpt-4o")` 를 만든다.
올라마로 옮기면서 설정 두 개가 꼭 필요해져, 한 곳에 모아 두었다.

    reasoning=False          - qwen3 계열은 생각을 글로 뱉는다. 안 끄면 몇 배 느리다
    method="json_schema"     - 구조화 출력에서 되는 method 가 모델마다 다르다.
                               qwen3.5:2b 는 function_calling 이 None 을 뱉어
                               AttributeError 가 난다 (ch04_dev-env/SETUP.md §4.6)
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

REPO = Path(__file__).resolve().parents[3]
load_dotenv(REPO / ".env")

BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL") or "qwen3.5:2b"

llm = ChatOllama(model=MODEL, temperature=0, base_url=BASE, reasoning=False)

# 구조화 출력을 쓸 때는 이 함수를 거친다. method 를 한 곳에서만 정하기 위해서.
def structured(schema):
    return llm.with_structured_output(schema, method="json_schema")
