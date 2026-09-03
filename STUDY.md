# 『만들면서 배우는 AI 에이전트 개발 입문+실전』 학습 노트

박나연(공원나연) · 한빛미디어 · [교재 상세 페이지](https://www.hanbit.co.kr/books/%EB%A7%8C%EB%93%A4%EB%A9%B4%EC%84%9C-%EB%B0%B0%EC%9A%B0%EB%8A%94-ai-%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8-%EA%B0%9C%EB%B0%9C-%EC%9E%85%EB%AC%B8-%EC%8B%A4%EC%A0%84?code=B5614034531)

장별 폴더 하나에 **학습 노트 + 저자 예제 코드 + 내 실습 공간**이 모두 들어 있습니다.
각 장 폴더는 저장소 루트에 `ch01_…` ~ `ch11_…` 로 나란히 있습니다.

## 진도표

| 장 | 제목 | 폴더 | 절 노트 | 예제 코드 | 진도 |
| --- | --- | --- | --- | --- | --- |
| | **Part 01 | AI 에이전트의 개념과 원리** | | | | |
| 01 | LLM 기반 의사결정 구조와 에이전트 동작 방식 | [`ch01_llm-decision`](ch01_llm-decision/README.md) | ✅ 4개 | — | ☐ |
| 02 | AI 에이전트를 구성하는 3가지 핵심 요소 | [`ch02_core-elements`](ch02_core-elements/README.md) | ✅ 4개 | — | ☐ |
| 03 | 목적에 따른 에이전트 아키텍처 설계 기준 | [`ch03_architecture`](ch03_architecture/README.md) | ✅ 3개 | — | ☐ |
| | **Part 02 | 랭그래프로 구현하는 AI 에이전트** | | | | |
| 04 | 에이전트 개발 환경 구축 | [`ch04_dev-env`](ch04_dev-env/README.md) | ✅ [SETUP.md](ch04_dev-env/SETUP.md) | ✓ | ☐ |
| 05 | 랭그래프 기반 에이전트 설계 | [`ch05_langgraph-basics`](ch05_langgraph-basics/README.md) | ✅ 3개 | ✓ | ☐ |
| 06 | 싱글 에이전트 구현 | [`ch06_single-agent`](ch06_single-agent/README.md) | ✅ 5개 | ✓ | ☐ |
| | **Part 03 | 멀티 에이전트 설계와 메모리 시스템 구현** | | | | |
| 07 | 멀티 에이전트 구현 | [`ch07_multi-agent`](ch07_multi-agent/README.md) | ✅ 6개 | ✓ | ☐ |
| 08 | 에이전트 메모리 설계와 개인화 구현 | [`ch08_memory`](ch08_memory/README.md) | ✅ 4개 | ✓ | ☐ |
| | **Part 04 | 프로토콜 기반 에이전트 확장 전략** | | | | |
| 09 | MCP 기반 외부 도구 연동 | [`ch09_mcp`](ch09_mcp/README.md) | ✅ 5개 | ✓ | ☐ |
| 10 | A2A 기반 에이전트 상호운용 | [`ch10_a2a`](ch10_a2a/README.md) | ✅ 4개 | ✓ | ☐ |
| | **Part 05 | 멀티 에이전트 실전 프로젝트** | | | | |
| 11 | 웹 검색 · RAG · 파일 관리 범용 멀티 에이전트 | [`ch11_final-project`](ch11_final-project/README.md) | ✅ 6개 | ✓ | ☐ |

> **절 노트** 칸의 `✅`는 서술형 노트가 **작성 완료**된 장입니다. 표시가 없으면 아직 빈 템플릿입니다.
> **진도** 칸은 직접 읽고 공부한 표시입니다. 노트 작성과 별개로 본인이 채웁니다.
> 노트 작성 규칙과 진행 상태는 [CLAUDE.md](CLAUDE.md), 지나온 판단의 이력은 [history.md](history.md)에 있습니다.

## 장 폴더 구성

```
ch06_single-agent/
├── README.md                                # 장 개요 · 학습 목표 · 절별 노트 색인
├── 06-01_도구를 호출하는 에이전트 이해하기.md   # 절 노트 (교재 상세 목차의 절 = 파일 1개)
├── 06-02_웹 검색 에이전트 만들기.md
├── 06-03_코딩 에이전트 만들기.md
├── 06-04_create_agent 상세 구조 이해하기.md
├── 06-05_RAG를 위한 에이전트 만들기.md
├── notes.md                                 # 장 전체 요약 (마지막에 정리)
│                                           # (.env 는 장별로 두지 않습니다 - 저장소 루트 하나)
├── examples/                                # 저자 제공 원본 예제 코드
│   ├── web_agent/  coding_agent/  create_agent/  rag_agent/
│   └── langgraph.json
└── practice/                                # 예제를 보지 않고 직접 쳐보는 공간
```

- 절 노트 파일명은 `장-절_교재 소제목.md` 형식입니다.
- **작성 완료된 노트(`✅`)** 는 서술형 학습 자료입니다. 문제 제기 → 개념 전개 → 다이어그램 → `요약 및 비유` → `결론` 구성이고, 교재의 소절 번호를 소제목으로 승계합니다.
- **아직 미작성인 장**은 빈 템플릿입니다. `[실습]` 소절에 **한 일 / 코드 / 결과·막힌 점** 칸이 잡혀 있고, 여기 든 소절 목차는 교재 상세 목차를 옮겨 둔 것이라 지우면 복원할 수 없습니다.
- `examples/`는 저자 원본이므로 **읽기 전용으로 참고**하고, 직접 치는 코드는 `practice/`에 쓰는 것을 권장합니다.

## 시작하기

```powershell
# 1) 환경 만들기 — "Miniforge Prompt" 에서. 미니포지를 쓰는 이유는 SETUP.md §2.1
conda create -n agent "python=3.12.14" -c conda-forge --override-channels -y
conda activate agent
conda install -c conda-forge --override-channels -y `
  "langgraph<2" "langchain<2" "langchain-openai<2" python-dotenv "langchain-ollama<2"

# 2) .env 준비 — 저장소 루트 하나로 관리합니다 (한 번만)
copy .env.example .env

# 3) 랭그래프 스튜디오 (langgraph.json 이 있는 곳에서)
cd examples
langgraph dev
```

> **`conda activate` 가 안 되면** 일반 PowerShell 이라 그렇습니다. 실행 방법 셋 중 하나를 고르세요 — [SETUP.md §2.3](ch04_dev-env/SETUP.md). 스크립트에서는 `…\miniforge3\envs\agent\python.exe` 를 직접 부르는 쪽이 안전합니다(`conda run` 은 한글이 깨집니다).

> **위 설치는 4·5장 범위입니다.** 6장 이후 패키지(`mcp`·`a2a-sdk`·`langchain-tavily`·`supabase` 등)는 그 장에 갈 때 상한을 지켜 추가하세요([CLAUDE.md](CLAUDE.md) §5·§6).

Python 3.11 이상이 필요합니다. 이 저장소는 **3.12.14** 로 맞춰 두었습니다.

## 필요한 API 키 · 외부 서비스

| 항목 | 필요한 장 | 비고 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 4~11장 | 전 실습 공통 |
| `TAVILY_API_KEY` | 6, 7, 9, 10, 11장 | 웹 검색 도구 |
| Supabase (`SUPABASE_URL`, `SUPABASE_KEY`) | 7, 11장 | DB · 벡터 스토어 |
| Google Drive OAuth | 11장 | `credentials.json` (커밋 금지) |

> **접속 정보는 저장소 루트의 [`.env`](.env.example) 하나로 관리합니다.** 장별 `.env`는 두지 않습니다 — 예제 대부분이 `load_dotenv()`를 인자 없이 불러 위로 찾아 올라갑니다.
>
> **예외는 10장뿐입니다.** `examples/multi_agent`의 저자 코드가 `dotenv_path="../.env"`처럼 경로를 박아 두어 `ch10_a2a/examples/.env`가 따로 필요합니다.
>
> `.env`와 자격증명 파일은 `.gitignore`에 등록되어 있습니다. 절대 커밋하지 마세요.

## 올라마로 어디까지 되나

**`OPENAI_API_KEY` 자리는 올라마로 대체할 수 있습니다.** 나머지 서비스는 대체가 안 됩니다.

> **실측 (2026-08-31)** — 사내 올라마 서버(9B)에서 확인했습니다. 검사 방법은 `scripts/check-ollama.py`.
>
> **실측 (2026-09-03)** — 이 PC에 올라마를 깔고 **`qwen3.5:2b`(2.3B)** 로 다시 확인했습니다. 도구 호출 · 도구 선택 · 병렬 호출이 전부 됩니다(CPU 9.2 tok/s). 설정·수치·모델 고른 근거는 [ch04 SETUP.md](ch04_dev-env/SETUP.md), 검사는 `ch04_dev-env/check_ollama.py`.
>
> **모델마다 되는 것이 다릅니다.** 같은 4B 이하라도 Phi-4 Mini는 도구를 아예 못 부릅니다. 모델을 바꾸면 위 표를 그대로 믿지 말고 검사부터 다시 돌리세요.

> ### ⚠️ 이 표는 **키 기준**입니다. 패키지 조건은 따로입니다
>
> 아래 표의 `✅`는 **"API 키가 필요 없다"**는 뜻이지 **"지금 당장 돌아간다"**는 뜻이 아닙니다. 그 장의 패키지가 환경에 깔려 있어야 합니다.
>
> **현재 conda 환경 `agent` 에 깔린 것은 4~6장 범위입니다** (2026-09-03 · import 검사 **21/38 통과**). 확인 명령:
>
> ```powershell
> python scripts/check-env.py
> ```
>
> | 장 | 추가로 깔아야 하는 패키지 |
> | :--- | :--- |
> | 04 · 05 · 06 · 08 | **없음** — 설치돼 있습니다 |
> | **07** | `supabase` |
> | **09** | `mcp<2` · `langchain-mcp-adapters` |
> | **10** | `a2a-sdk<1` · `mcp<2` · `uvicorn` |
> | **11** | 위 전부 + `pypdf` · `google-api-python-client` 계열 |
>
> **5·8장 노트북은 이제 열립니다** — `jupyterlab 4.6.3` · `ipython 9.17.1` 설치됨. 커널은 `agent` 환경에 등록돼 있습니다.
>
> **6장 예제 중 `rag_agent` 만 예외입니다.** 저자 코드가 `OpenAIEmbeddings` 를 **모듈 최상단에서** 만들어 두어, 키 없이 import 하면 그 자리에서 `openai.OpenAIError: Missing credentials` 가 납니다. 올라마로 가려면 임베딩을 `OllamaEmbeddings` 로 바꿔야 합니다. `coding_agent`·`create_agent`·`web_agent` 는 키 없이 import 됩니다.
>
> ```powershell
> conda install -n agent -c conda-forge --override-channels -y "<패키지><상한>"
> ```
>
> **상한(`mcp<2`·`a2a-sdk<1`)을 반드시 지키세요.** 풀면 교재 예제 26개 파일이 깨집니다([CLAUDE.md](CLAUDE.md) §6). conda-forge에 없는 것은 같은 환경에 pip로 넣고 [CLAUDE.md](CLAUDE.md) §5에 기록하세요.
>
> **RAG를 쓰는 절(6.5 · 8.4 · 11.3)은 임베딩 모델도 받아야 합니다** — `ollama pull bge-m3` (아래).

| 장 | 예제 | 올라마만으로 | 추가로 필요한 것 |
| :--- | :--- | :---: | :--- |
| **4** | `check_ollama.py` | **✅ 전부** | — |
| **5** | 5.2 · 5.3 노트북 | **✅ 전부** | — |
| **6** | `coding_agent` · `create_agent` | **✅** | — |
| | `rag_agent` | **✅** | 임베딩 모델 (아래) |
| | `web_agent` | ⚠️ | **Tavily 키** |
| **7** | `how_to_use_command` | **✅** | — |
| | `network_agent` · `supervisor_planning_agent` | ⚠️ | **Tavily 키** |
| | `supervisor_agent_web` | ⚠️ | **Supabase** |
| | `supervisor_agent_triple` | ⚠️ | **Tavily + Supabase** |
| **8** | `short-term memory` | **✅ 전부** | — |
| | `long-term memory` | **✅** | 임베딩 모델 |
| **9** | `mcp_agent` (직접 만든 서버) | **✅** | — |
| | `mcp_multi_agent` | ⚠️ | **Tavily 키** |
| **10** | `hello_world` | **✅** | **LLM도 불필요** |
| | `multi_agent` | ⚠️ | **Tavily 키** |
| **11** | `orchestrator_agent` · `common` | **✅** | — |
| | 나머지 셋 | ❌ | **Tavily · Supabase · 구글 드라이브** |

### 한눈에

```mermaid
graph LR
    A["4·5장<br/>문법과 기초"] -->|"올라마만으로"| B["6장 일부<br/>코딩·create_agent·RAG"]
    B -->|"올라마만으로"| C["8장<br/>메모리 전부"]
    C -->|"올라마만으로"| D["9·10장 일부<br/>MCP 서버·A2A 배관"]
    D -->|"여기부터 키 필요"| E["웹 검색·DB·드라이브가<br/>얽힌 절들"]
```

**키 없이 4 · 5 · 8장을 통째로, 6 · 9 · 10장을 절반씩** 갈 수 있습니다. 랭그래프 문법·메모리·MCP 서버·A2A 배관이 전부 여기 들어 있습니다.

### 임베딩 모델은 따로 받아야 합니다

RAG를 쓰는 절(6.5 · 8.4 · 11.3)에는 **임베딩 전용 모델**이 필요합니다. 대화 모델로는 안 됩니다.

> **한국어 문서를 다룬다면 다국어 모델이어야 합니다.** 같은 문장 4개로 검색을 시켜 본 결과입니다.
>
> | 모델 | 차원 | 한국어 정확도 |
> | :--- | ---: | :--- |
> | `nomic-embed-text` | 768 | **0 / 3** — 전부 엉뚱한 문서 |
> | `bge-m3` | 1024 | **3 / 3** |
>
> 영어로 바꿔 시험하면 `nomic-embed-text`도 정확히 찾습니다. **모델이 나쁜 게 아니라 언어가 안 맞는 것**입니다.

**차원이 다르면 벡터 저장소를 다시 만들어야 합니다.** OpenAI(1536) → `bge-m3`(1024)로 바꾸면 기존 인덱스는 못 씁니다. [11.3절](ch11_final-project/11-03_%EB%AC%B8%EC%84%9C%20%EC%A0%80%EC%9E%A5%C2%B7%EA%B2%80%EC%83%89%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8.md)에서 경고한 함정이 여기서 실제로 걸립니다.

## 학습 순서 제안

1. **1~3장** 개념. 빠르게 훑고 3장 기준으로 만들고 싶은 서비스를 하나 정해두기
2. **4~5장** 환경 구축 + 랭그래프 문법. 여기서 손에 익혀야 6장부터 편합니다
3. **6장** 싱글 에이전트 4종 (웹 검색 / 코딩 / create_agent / RAG)
4. **7~8장** 멀티 에이전트 패턴 + 메모리
5. **9~10장** MCP · A2A 프로토콜
6. **11장** 앞의 모든 것을 합친 실전 프로젝트
