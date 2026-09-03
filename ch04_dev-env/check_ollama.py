"""올라마 연결과 기본 기능을 확인한다.

    python ch04_dev-env/check_ollama.py

저장소 루트의 .env 에서 접속 정보를 읽는다(장별 .env 는 두지 않는다).
없으면 기본값(http://localhost:11434 · qwen3.5:2b)으로 붙는다.

검사 넷:
    [1] 단순 호출    - 4·5·8장에 필요
    [2] 도구 호출    - 6장 이후의 관건
    [3] 구조화 출력  - 라우터. 되는 method 는 모델마다 다르다
    [4] 병렬 호출    - 한 번에 도구를 여러 개 부를 수 있는가

모델을 바꿨다면 이 검사부터 다시 돌린다. [3]의 method 와 [4]의 가능 여부는
모델마다 다르고, 코드에 하드코딩하기 전에 확인해야 한다.
"""

import os
import time
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).parent.parent / ".env")

BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL") or "qwen3.5:2b"

print(f"서버 : {BASE}")
print(f"모델 : {MODEL}\n")

# reasoning=False - 생각을 글로 뱉는 모델(qwen3 계열)에서 응답이 크게 빨라진다.
#                   지원하지 않는 모델이면 무시된다.
llm = ChatOllama(model=MODEL, temperature=0, base_url=BASE, reasoning=False)


@tool
def get_weather(city: str) -> str:
    """도시 이름을 받아 그 도시의 현재 날씨를 알려 준다."""
    return f"{city}: 맑음, 21도"


@tool
def get_time(city: str) -> str:
    """도시 이름을 받아 그 도시의 현재 시각을 알려 준다."""
    return f"{city}: 14:30"


# --- [1] 단순 호출 --------------------------------------------------------
t0 = time.perf_counter()
r = llm.invoke("파이썬의 리스트와 튜플 차이를 다섯 문장으로 설명해줘.")
dt = time.perf_counter() - t0
tok = (r.usage_metadata or {}).get("output_tokens", 0)
print(f"[1] 단순 호출  : {tok}토큰 / {dt:.1f}초 / {tok / dt:.1f} tok/s")


# --- [2] 도구 호출 --------------------------------------------------------
r = llm.bind_tools([get_weather]).invoke("서울 날씨 알려줘")
if r.tool_calls:
    c = r.tool_calls[0]
    print(f"[2] 도구 호출  : {c['name']}({c['args']})")
else:
    # 도구를 부르려다 형식을 못 지키면 본문에 텍스트로 새어 나온다.
    print(f"[2] 도구 호출  : 실패 - 본문: {r.content.strip()[:60]}")


# --- [3] 구조화 출력 ------------------------------------------------------
class Category(BaseModel):
    """고객 문의를 분류한 결과."""

    # Literal 로 좁힌다. 그냥 str 이면 모델이 아무 말이나 채운다.
    category: Literal["환불", "배송", "기타"] = Field(description="문의 종류")
    reason: str = Field(description="그렇게 판단한 근거. 한국어 한 문장.")


# 되는 method 는 모델마다 다르다. 차례로 시도해 찾는다.
for method in ("function_calling", "json_schema", "json_mode"):
    try:
        out = llm.with_structured_output(Category, method=method).invoke(
            "이거 마음에 안 들어요. 돈 돌려주세요."
        )
        # 정답은 "환불". 형식이 맞았다고 판단까지 맞은 것은 아니다.
        mark = "" if out.category == "환불" else "   <- 오분류. 정답은 환불"
        print(f"[3] 구조화 출력: {out.category} (method={method!r}){mark}")
        break
    except Exception as exc:
        print(f"    method={method!r} 실패: {type(exc).__name__}")
else:
    print("[3] 구조화 출력: 전부 실패")


# --- [4] 병렬 호출 --------------------------------------------------------
r = llm.bind_tools([get_weather, get_time]).invoke(
    "서울의 날씨와 서울의 현재 시각을 둘 다 알려줘."
)
calls = [c["name"] for c in (r.tool_calls or [])]
if len(calls) >= 2:
    print(f"[4] 병렬 호출  : {calls}  (한 응답에 {len(calls)}건)")
else:
    print(f"[4] 병렬 호출  : 안 됨 - {calls or '(호출 없음)'}")
