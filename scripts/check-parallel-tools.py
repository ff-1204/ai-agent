"""여러 모델의 도구 호출 능력을 같은 검사로 비교합니다.

    python scripts/check-parallel-tools.py                    # .env 의 모델
    python scripts/check-parallel-tools.py qwen3.5:2b         # 지정한 모델
    python scripts/check-parallel-tools.py qwen3.5:2b qwen3:4b phi4-mini

서버 주소는 저장소 루트 .env 의 OLLAMA_BASE_URL, 모델은 인자로 받습니다.
인자가 없으면 그 .env 의 OLLAMA_MODEL 을 씁니다.

`ollama show` 의 `capabilities: tools` 는 믿을 것이 못 됩니다. 선언은 해 놓고
형식을 못 지켜 본문에 텍스트로 뱉는 모델이 있습니다(Granite 4.2 3B, Phi-4 Mini).
그런 경우 tool_calls 가 비므로, 실패하면 본문을 함께 찍어 원인을 보여 줍니다.

검사 다섯:
    [1] 단일 호출      - 도구 하나를 제대로 부르는가
    [2] 도구 선택      - 둘 중 맞는 것을 고르는가
    [3] 안 쓰는 판단   - 도구가 필요 없을 때 안 부르는가
    [4] 병렬(같은 도구) - 한 응답에 같은 도구를 여러 번 부르는가
    [5] 병렬(다른 도구) - 한 응답에 서로 다른 도구를 부르는가

[1]·[2] 가 되면 6장, [4]·[5] 까지 되면 도구를 여러 개 묶어 쓰는 7장 이후가
수월합니다. [3] 만 통과한 모델은 의심하세요 — 아무 때도 도구를 안 부르면
그것만 자동으로 통과합니다.
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

load_dotenv(Path(__file__).parent.parent / ".env")

BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


@tool
def get_weather(city: str) -> str:
    """도시 이름을 받아 그 도시의 현재 날씨를 알려 준다."""
    return f"{city}: 맑음, 21도"


@tool
def get_time(city: str) -> str:
    """도시 이름을 받아 그 도시의 현재 시각을 알려 준다."""
    return f"{city}: 14:30"


@tool
def search_web(query: str) -> str:
    """최신 뉴스나 실시간 정보가 필요할 때 웹을 검색한다."""
    return "..."


def names(calls):
    return [c["name"] for c in calls]


def cities(calls):
    return {str(c["args"].get("city", "")) for c in calls}


# (검사명, 건네줄 도구 목록, 프롬프트, 판정 함수)
TESTS = [
    (
        "단일 호출",
        [get_weather],
        "서울 날씨 알려줘",
        lambda c: len(c) == 1
        and c[0]["name"] == "get_weather"
        and "서울" in str(c[0]["args"].get("city", "")),
    ),
    (
        "도구 선택",
        [get_weather, search_web],
        "부산 날씨 어때?",
        lambda c: len(c) >= 1 and c[0]["name"] == "get_weather",
    ),
    (
        "안 쓰는 판단",
        [get_weather, search_web],
        "고마워요! 오늘 대화 즐거웠어요.",
        lambda c: len(c) == 0,
    ),
    (
        "병렬(같은 도구)",
        [get_weather],
        "서울과 부산의 날씨를 둘 다 알려줘.",
        lambda c: len(c) >= 2
        and set(names(c)) == {"get_weather"}
        and any("서울" in x for x in cities(c))
        and any("부산" in x for x in cities(c)),
    ),
    (
        "병렬(다른 도구)",
        [get_weather, get_time],
        "서울의 날씨와 서울의 현재 시각을 둘 다 알려줘.",
        lambda c: len(c) >= 2 and {"get_weather", "get_time"} <= set(names(c)),
    ),
]


def run(model):
    print(f"\n{'=' * 68}\n{model}\n{'=' * 68}")
    # reasoning=False - 생각을 글로 뱉는 모델(qwen3 계열)에서 크게 빨라집니다.
    llm = ChatOllama(model=model, temperature=0, base_url=BASE, reasoning=False)
    out = {}
    for name, tools, prompt, judge in TESTS:
        try:
            t0 = time.perf_counter()
            r = llm.bind_tools(tools).invoke(prompt)
            dt = time.perf_counter() - t0
            calls = r.tool_calls or []
            ok = judge(calls)

            if calls:
                detail = ", ".join(f"{c['name']}({c['args']})" for c in calls)
            else:
                # 형식을 못 지키면 본문에 텍스트로 새어 나옵니다. 그 증거를 보여 줍니다.
                body = r.content.strip().replace("\n", " ")
                detail = f"(호출 없음) 본문: {body[:60]}" if body else "(호출 없음)"

            print(f"  {'O' if ok else 'X'} {name:16} {dt:5.1f}s  {detail[:95]}")
            out[name] = ok
        except Exception as exc:
            print(f"  X {name:16}         실패: {type(exc).__name__}: {str(exc).splitlines()[0][:60]}")
            out[name] = False
    return out


if __name__ == "__main__":
    models = sys.argv[1:] or [m for m in [os.getenv("OLLAMA_MODEL")] if m]
    if not models:
        print("모델을 지정하세요. 예: python scripts/check-parallel-tools.py qwen3.5:2b")
        print("또는 저장소 루트 .env 의 OLLAMA_MODEL 을 채우세요.")
        sys.exit(1)

    print(f"서버: {BASE}")
    table = {m: run(m) for m in models}

    print(f"\n{'=' * 68}\n정리\n{'=' * 68}")
    cols = [t[0] for t in TESTS]
    print(f"{'모델':<20}" + "".join(f"{c:<17}" for c in cols))
    for m, res in table.items():
        print(f"{m:<20}" + "".join(f"{'O' if res.get(c) else 'X':<17}" for c in cols))

    print()
    for m, res in table.items():
        if res.get("단일 호출") and res.get("도구 선택"):
            extra = " 병렬 호출까지 됩니다." if res.get("병렬(다른 도구)") else ""
            print(f"  {m}: 6장 이후를 시도해 볼 만합니다.{extra}")
        elif any(res.get(c) for c in ("단일 호출", "병렬(같은 도구)", "병렬(다른 도구)")):
            print(f"  {m}: 도구 호출이 불안정합니다. 4·5·8장까지만 쓰세요.")
        else:
            print(f"  {m}: 도구를 부르지 못합니다. 6장 이후는 다른 모델을 쓰세요.")

    # 하나라도 [1]과 [2]를 통과하면 0
    sys.exit(0 if any(r.get("단일 호출") and r.get("도구 선택") for r in table.values()) else 1)
