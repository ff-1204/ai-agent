# Chapter 09 · MCP 기반 외부 도구 연동

> Part 04 | 프로토콜 기반 에이전트 확장 전략

## 학습 목표

- MCP의 개념과 3계층 아키텍처(호스트·클라이언트·서버)를 설명할 수 있다
- 파이썬 SDK로 MCP 서버를 만들고 도구를 노출할 수 있다
- langchain-mcp-adapters로 랭그래프 에이전트를 MCP 클라이언트로 연결할 수 있다
- 여러 MCP 서버를 묶어 슈퍼바이저 멀티 에이전트를 구성할 수 있다

## 절별 노트

| 절 | 노트 파일 | 진도 |
| --- | --- | --- |
| 9.1 | [`09-01_MCP란.md`](09-01_MCP%EB%9E%80.md) | ☐ |
| 9.2 | [`09-02_MCP 기능이 들어간 에이전트 서비스.md`](09-02_MCP%20%EA%B8%B0%EB%8A%A5%EC%9D%B4%20%EB%93%A4%EC%96%B4%EA%B0%84%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | ☐ |
| 9.3 | [`09-03_MCP 서버 구축하기.md`](09-03_MCP%20%EC%84%9C%EB%B2%84%20%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0.md) | ☐ |
| 9.4 | [`09-04_MCP 클라이언트 구축하기 - 랭그래프.md`](09-04_MCP%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%20%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0%20-%20%EB%9E%AD%EA%B7%B8%EB%9E%98%ED%94%84.md) | ☐ |
| 9.5 | [`09-05_랭그래프에서 MCP 기반 멀티 에이전트 구현하기.md`](09-05_%EB%9E%AD%EA%B7%B8%EB%9E%98%ED%94%84%EC%97%90%EC%84%9C%20MCP%20%EA%B8%B0%EB%B0%98%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0.md) | ☐ |

<details><summary>소절까지 펼쳐보기</summary>

- [ ] **[9.1 MCP란](09-01_MCP%EB%9E%80.md)**
  - [ ] 9.1.1 MCP 개념
  - [ ] 9.1.2 MCP의 3계층 아키텍처
  - [ ] 9.1.3 MCP 파이썬 SDK
- [ ] **[9.2 MCP 기능이 들어간 에이전트 서비스](09-02_MCP%20%EA%B8%B0%EB%8A%A5%EC%9D%B4%20%EB%93%A4%EC%96%B4%EA%B0%84%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%84%9C%EB%B9%84%EC%8A%A4.md)**
  - [ ] 9.2.1 MCP 기능 탑재 에이전트 서비스
  - [ ] 9.2.2 MCP 서버 마켓플레이스
- [ ] **[9.3 MCP 서버 구축하기](09-03_MCP%20%EC%84%9C%EB%B2%84%20%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0.md)**
  - [ ] 9.3.1 Langchain-MCP-Adapters 기반 MCP 구현 흐름 이해하기
  - [ ] 9.3.2 [실습] 사용자의 정보를 읽는 도구 정의하기
  - [ ] 9.3.3 [실습] 일기를 저장하는 도구 정의하기
  - [ ] 9.3.4 [실습] 에이전트 프롬프트 작성하기
- [ ] **[9.4 MCP 클라이언트 구축하기: 랭그래프](09-04_MCP%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%20%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0%20-%20%EB%9E%AD%EA%B7%B8%EB%9E%98%ED%94%84.md)**
  - [ ] 9.4.1 [실습] 에이전트가 포함된 MCP 클라이언트 구축하기
  - [ ] 9.4.2 [실습] 에이전트와 대화를 통해 일기 작성하기
- [ ] **[9.5 랭그래프에서 MCP 기반 멀티 에이전트 구현하기](09-05_%EB%9E%AD%EA%B7%B8%EB%9E%98%ED%94%84%EC%97%90%EC%84%9C%20MCP%20%EA%B8%B0%EB%B0%98%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0.md)**
  - [ ] 9.5.1 [실습] 파일 탐색 및 저장 MCP 서버 구축하기
  - [ ] 9.5.2 [실습] 멀티 서버 클라이언트 구축하기
  - [ ] 9.5.3 [실습] 슈퍼바이저 에이전트 만들기
  - [ ] 9.5.4 [실습] 웹 검색과 파일 탐색 요청하기

</details>

## 관련 예제 코드

| 내용 | 경로 |
| --- | --- |
| 9.3~9.4 MCP 서버·클라이언트 | [`examples/mcp_agent`](examples/mcp_agent) |
| 9.5 MCP 멀티 에이전트 | [`examples/mcp_multi_agent`](examples/mcp_multi_agent) |

## `.env` 두는 위치

장 폴더에 `.env`를 두면 클라이언트가 찾아 올라갑니다. MCP 서버를 각 폴더에서 직접 띄운다면 `examples/mcp_agent/.env`, `examples/mcp_multi_agent/.env`도 만들어두면 안전합니다.

```powershell
copy .env.example .env
```

## 참고 문서

| 무엇을 볼 때 | 문서 |
| --- | --- |
| 9.1 MCP란 (개념·스펙) | [Model Context Protocol](https://modelcontextprotocol.io/) |
| 9.3 서버 구축 (`FastMCP`) | [MCP Python SDK 문서](https://py.sdk.modelcontextprotocol.io/) — **v1 섹션** |
| SDK 예제 원본 | [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) |
| 9.4~9.5 랭그래프에서 MCP 붙이기 | [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) |

> **버전 주의** — 이 저장소는 `mcp` **1.x**를 씁니다. 예제 import는 `from mcp.server.fastmcp import FastMCP`입니다.
> 공식 SDK 문서 사이트는 현재 **v2 기준**이고, v2에서는 `from mcp.server import MCPServer`로 바뀌었습니다.
> 문서를 열면 v1 섹션을 고르세요. v2 화면을 보고 따라 치면 import부터 어긋납니다.

## 이 폴더 구성

- `09-01_…md` ~ `09-05_…md` — 절별 학습 노트
- `notes.md` — 장 전체 요약 (절 노트를 다 쓴 뒤 마지막에 정리)
- `practice/` — 예제를 보지 않고 직접 쳐보는 공간
- `.env.example` — 이 장에 필요한 API 키. `copy .env.example .env` 후 값을 채우세요

> **메모**  
> MCP 서버는 별도 프로세스로 실행됩니다. 터미널을 2개 열어 서버와 클라이언트를 각각 띄우는 흐름에 익숙해지세요.

---

[⬅ 전체 목차로](../STUDY.md)
