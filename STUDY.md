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
| 04 | 에이전트 개발 환경 구축 | [`ch04_dev-env`](ch04_dev-env/README.md) | ✅ 4개 | ✓ | ☐ |
| 05 | 랭그래프 기반 에이전트 설계 | [`ch05_langgraph-basics`](ch05_langgraph-basics/README.md) | ✅ 3개 | ✓ | ☐ |
| 06 | 싱글 에이전트 구현 | [`ch06_single-agent`](ch06_single-agent/README.md) | 5개 | ✓ | ☐ |
| | **Part 03 | 멀티 에이전트 설계와 메모리 시스템 구현** | | | | |
| 07 | 멀티 에이전트 구현 | [`ch07_multi-agent`](ch07_multi-agent/README.md) | 6개 | ✓ | ☐ |
| 08 | 에이전트 메모리 설계와 개인화 구현 | [`ch08_memory`](ch08_memory/README.md) | 4개 | ✓ | ☐ |
| | **Part 04 | 프로토콜 기반 에이전트 확장 전략** | | | | |
| 09 | MCP 기반 외부 도구 연동 | [`ch09_mcp`](ch09_mcp/README.md) | 5개 | ✓ | ☐ |
| 10 | A2A 기반 에이전트 상호운용 | [`ch10_a2a`](ch10_a2a/README.md) | 4개 | ✓ | ☐ |
| | **Part 05 | 멀티 에이전트 실전 프로젝트** | | | | |
| 11 | 웹 검색 · RAG · 파일 관리 범용 멀티 에이전트 | [`ch11_final-project`](ch11_final-project/README.md) | 6개 | ✓ | ☐ |

> **절 노트** 칸의 `✅`는 서술형 노트가 **작성 완료**된 장입니다. 표시가 없으면 아직 빈 템플릿입니다.
> **진도** 칸은 직접 읽고 공부한 표시입니다. 노트 작성과 별개로 본인이 채웁니다.
> 노트 작성 규칙과 진행 상태는 [CLAUDE.md](CLAUDE.md)에 있습니다.

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
├── .env.example                             # 그 장에 필요한 API 키
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
# 1) 가상환경 (uv 사용 시) — 저장소 루트에서
uv venv
.venv\Scripts\activate
uv sync

# 2) 아나콘다 사용 시 (책 4장)
conda create -n langgraph python=3.12
conda activate langgraph
pip install -r requirements.txt

# 3) 실습할 장으로 이동해 .env 준비
cd ch06_single-agent
copy .env.example .env

# 4) 랭그래프 스튜디오 (langgraph.json 이 있는 곳에서)
cd examples
langgraph dev
```

Python 3.11 이상이 필요합니다.

## 필요한 API 키 · 외부 서비스

| 항목 | 필요한 장 | 비고 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 4~11장 | 전 실습 공통 |
| `TAVILY_API_KEY` | 6, 7, 9, 10, 11장 | 웹 검색 도구 |
| Supabase (`SUPABASE_URL`, `SUPABASE_KEY`) | 7, 11장 | DB · 벡터 스토어 |
| Google Drive OAuth | 11장 | `credentials.json` (커밋 금지) |

> `.env`와 자격증명 파일은 `.gitignore`에 등록되어 있습니다. 절대 커밋하지 마세요.

## 학습 순서 제안

1. **1~3장** 개념. 빠르게 훑고 3장 기준으로 만들고 싶은 서비스를 하나 정해두기
2. **4~5장** 환경 구축 + 랭그래프 문법. 여기서 손에 익혀야 6장부터 편합니다
3. **6장** 싱글 에이전트 4종 (웹 검색 / 코딩 / create_agent / RAG)
4. **7~8장** 멀티 에이전트 패턴 + 메모리
5. **9~10장** MCP · A2A 프로토콜
6. **11장** 앞의 모든 것을 합친 실전 프로젝트
