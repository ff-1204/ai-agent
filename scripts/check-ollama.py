"""올라마 모델이 이 책 예제를 감당할 수 있는지 검사합니다.

    python scripts/check-ollama.py        # conda 환경 agent 에서

모델은 저장소 루트 .env 의 OLLAMA_MODEL 로 지정합니다. 없으면 첫 번째 설치된 모델을 씁니다.
서버가 떠 있어야 합니다 (`ollama serve` 또는 트레이 앱).

이 책 예제 89개 중 36개(40%)가 도구 호출을 씁니다. [2]가 실패하면
6장 이후는 이 모델로 진행하기 어렵습니다.
"""

import os
import sys
import time
from typing import Literal
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "")


def sec(n):
    print("\n" + "=" * 60)
    print(n)
    print("=" * 60)


# --- 서버와 모델 ---------------------------------------------------------
sec("[0] 서버 연결과 모델 확인")
try:
    import ollama

    client = ollama.Client(host=BASE)
    installed = [m.model for m in client.list().models]
except Exception as exc:
    print(f"  서버에 붙지 못했습니다 ({BASE})")
    print(f"  {type(exc).__name__}: {exc}")
    print("\n  `ollama serve` 가 떠 있는지 확인하세요.")
    sys.exit(1)

print(f"  서버      : {BASE}")
print(f"  설치된 모델: {installed or '(없음)'}")

if not installed:
    print("\n  모델이 없습니다.  ollama pull <모델> 로 먼저 받으세요.")
    sys.exit(1)

if not MODEL:
    MODEL = installed[0]
    print(f"  OLLAMA_MODEL 이 비어 있어 첫 번째 모델을 씁니다.")
elif MODEL not in installed and f"{MODEL}:latest" not in installed:
    print(f"\n  '{MODEL}' 이 설치 목록에 없습니다.  ollama pull {MODEL}")
    sys.exit(1)

print(f"  검사할 모델: {MODEL}")

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# reasoning=False — 생각을 글로 뱉는 모델(qwen3 계열 등)에서 응답이 크게 빨라집니다.
#                   지원하지 않는 모델이면 무시됩니다.
llm = ChatOllama(model=MODEL, temperature=0, base_url=BASE, reasoning=False)
results = {}


# --- [1] 단순 호출 -------------------------------------------------------
sec("[1] 단순 호출 — 4·5·8장에 필요")
try:
    t0 = time.perf_counter()
    r = llm.invoke("1+1은? 숫자만 답하세요.")
    dt = time.perf_counter() - t0
    usage = getattr(r, "usage_metadata", None) or {}
    out_tok = usage.get("output_tokens")
    print(f"  응답   : {r.content.strip()[:60]}")
    print(f"  걸린 시간: {dt:.1f}초", end="")
    if out_tok:
        print(f"  ({out_tok} 토큰, 약 {out_tok / dt:.1f} tok/s)")
    else:
        print()
    results["단순 호출"] = True
except Exception as exc:
    print(f"  실패: {type(exc).__name__}: {exc}")
    results["단순 호출"] = False


# --- [2] 도구 호출 -------------------------------------------------------
sec("[2] 도구 호출 — 6장 이후의 관건")


@tool
def get_weather(city: str) -> str:
    """도시 이름을 받아 그 도시의 현재 날씨를 알려 준다."""
    return f"{city}: 맑음, 21도"


try:
    t0 = time.perf_counter()
    r = llm.bind_tools([get_weather]).invoke("서울 날씨 알려줘")
    dt = time.perf_counter() - t0

    if r.tool_calls:
        call = r.tool_calls[0]
        print(f"  tool_calls : {call['name']}({call['args']})")
        ok_name = call["name"] == "get_weather"
        ok_args = "city" in call["args"] and "서울" in str(call["args"].get("city", ""))
        print(f"  도구 이름   : {'맞음' if ok_name else '틀림'}")
        print(f"  인자 채우기 : {'맞음' if ok_args else '틀림 -> ' + str(call['args'])}")
        print(f"  걸린 시간   : {dt:.1f}초")
        results["도구 호출"] = ok_name and ok_args
    else:
        print("  tool_calls 가 비어 있습니다. 도구를 부르지 않았습니다.")
        print(f"  대신 이렇게 답했습니다: {r.content.strip()[:80]}")
        results["도구 호출"] = False
except Exception as exc:
    print(f"  실패: {type(exc).__name__}: {str(exc).splitlines()[0]}")
    results["도구 호출"] = False


# --- [3] 도구 두 개 중 고르기 --------------------------------------------
sec("[3] 도구 두 개 중 고르기 — 2.4절의 '갈림길'")


@tool
def search_web(query: str) -> str:
    """최신 뉴스나 실시간 정보가 필요할 때 웹을 검색한다."""
    return "..."


try:
    r = llm.bind_tools([get_weather, search_web]).invoke("부산 날씨 어때?")
    if r.tool_calls:
        picked = r.tool_calls[0]["name"]
        print(f"  고른 도구: {picked}  ({'맞음' if picked == 'get_weather' else '틀림'})")
        results["도구 선택"] = picked == "get_weather"
    else:
        print("  도구를 부르지 않았습니다.")
        results["도구 선택"] = False
except Exception as exc:
    print(f"  실패: {type(exc).__name__}: {str(exc).splitlines()[0]}")
    results["도구 선택"] = False


# --- [4] 구조화 출력 -----------------------------------------------------
sec("[4] 구조화 출력 — 1.2절의 라우터")


class Category(BaseModel):
    """고객 문의를 분류한 결과."""

    # Literal 로 좁힙니다. 그냥 str 이면 모델이 아무 말이나 채웁니다(1.2절).
    category: Literal["환불", "배송", "기타"] = Field(description="문의 종류")
    reason: str = Field(description="그렇게 판단한 근거. 한국어 한 문장.")


# method 를 바꿔 가며 되는 것을 찾습니다. 기본값(json_schema)은
# 작은 모델에서 JSON 대신 값만 뱉어 파싱이 깨지는 경우가 있습니다.
for method in ("function_calling", "json_schema", "json_mode"):
    try:
        r = llm.with_structured_output(Category, method=method).invoke(
            "이거 마음에 안 들어요. 돈 돌려주세요."
        )
        print(f"  method={method!r} 로 성공")
        print(f"  category : {r.category}")
        print(f"  reason   : {r.reason[:50]}")
        results["구조화 출력"] = True
        if method != "function_calling":
            print(f"  -> 코드에서도 method={method!r} 를 지정하세요.")
        break
    except Exception as exc:
        print(f"  method={method!r} 실패: {type(exc).__name__}: {str(exc).splitlines()[0][:52]}")
else:
    results["구조화 출력"] = False


# --- 정리 ----------------------------------------------------------------
sec("정리")
for k, v in results.items():
    print(f"  {'O' if v else 'X'}  {k}")

print()
if results.get("도구 호출") and results.get("도구 선택"):
    print("  도구 호출이 됩니다. 6장 이후도 시도해 볼 만합니다.")
    print("  다만 실제 예제는 도구가 더 많고 대화가 길어지므로 정확도가 떨어질 수 있습니다.")
elif results.get("단순 호출"):
    print("  단순 호출은 되지만 도구 호출이 안 됩니다.")
    print("  4·5·8장은 이 모델로, 6장 이후는 도구 호출이 되는 모델이나 API 를 쓰세요.")
else:
    print("  기본 호출부터 실패했습니다. 모델과 서버 상태를 먼저 확인하세요.")

sys.exit(0 if results.get("단순 호출") else 1)
