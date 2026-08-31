# Chapter 06 · 싱글 에이전트 구현

> Part 02 | 랭그래프로 구현하는 AI 에이전트

## 학습 목표

- 도구를 호출하는 에이전트의 동작 루프를 이해한다
- Tavily 검색 도구를 붙인 웹 검색 에이전트를 만들고 LangGraph Studio로 확인할 수 있다
- 사용자 정의 도구(코드 실행·파일 저장)를 만들어 코딩 에이전트를 구성할 수 있다
- `create_agent`의 주요 파라미터와 미들웨어·구조화 출력을 활용할 수 있다
- 벡터 DB를 구축하고 RAG 에이전트를 구현할 수 있다

## 절별 노트

| 절 | 노트 파일 | 진도 |
| --- | --- | --- |
| 6.1 | [`06-01_도구를 호출하는 에이전트 이해하기.md`](06-01_%EB%8F%84%EA%B5%AC%EB%A5%BC%20%ED%98%B8%EC%B6%9C%ED%95%98%EB%8A%94%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0.md) | ☐ |
| 6.2 | [`06-02_웹 검색 에이전트 만들기.md`](06-02_%EC%9B%B9%20%EA%B2%80%EC%83%89%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md) | ☐ |
| 6.3 | [`06-03_코딩 에이전트 만들기.md`](06-03_%EC%BD%94%EB%94%A9%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md) | ☐ |
| 6.4 | [`06-04_create_agent 상세 구조 이해하기.md`](06-04_create_agent%20%EC%83%81%EC%84%B8%20%EA%B5%AC%EC%A1%B0%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0.md) | ☐ |
| 6.5 | [`06-05_RAG를 위한 에이전트 만들기.md`](06-05_RAG%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md) | ☐ |

<details><summary>소절까지 펼쳐보기</summary>

- [ ] **[6.1 도구를 호출하는 에이전트 이해하기](06-01_%EB%8F%84%EA%B5%AC%EB%A5%BC%20%ED%98%B8%EC%B6%9C%ED%95%98%EB%8A%94%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0.md)**
- [ ] **[6.2 웹 검색 에이전트 만들기](06-02_%EC%9B%B9%20%EA%B2%80%EC%83%89%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md)**
  - [ ] 6.2.1 [실습] 타빌리 서치 사용법 익히기
  - [ ] 6.2.2 [실습] 랭체인에서 도구 호출 사용하기
  - [ ] 6.2.3 [실습] 랭그래프로 에이전트 그래프 생성하기
  - [ ] 6.2.4 [실습] 최신 정보 검색하고 답변 받아보기
  - [ ] 6.2.5 [실습] 랭그래프 서버 실행하고 랭그래프 스튜디오 사용하기
- [ ] **[6.3 코딩 에이전트 만들기](06-03_%EC%BD%94%EB%94%A9%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md)**
  - [ ] 6.3.1 [실습] 사용자 도구 정의하기
  - [ ] 6.3.2 [실습] 코드 실행 도구 만들기
  - [ ] 6.3.3 [실습] 파일을 저장하는 도구 만들기
- [ ] **[6.4 create_agent 상세 구조 이해하기](06-04_create_agent%20%EC%83%81%EC%84%B8%20%EA%B5%AC%EC%A1%B0%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0.md)**
  - [ ] 6.4.1 create_agent 개요 이해하기
  - [ ] 6.4.2 주요 파라미터 이해하기
  - [ ] 6.4.3 [실습] 미들웨어 추가하기
  - [ ] 6.4.4 [실습] 구조화 출력 정의하기
- [ ] **[6.5 RAG를 위한 에이전트 만들기](06-05_RAG%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md)**
  - [ ] 6.5.1 RAG란
  - [ ] 6.5.2 [실습] 벡터 데이터베이스의 이해와 사용하기
  - [ ] 6.5.3 [실습] 문서 검색과 답변을 위한 도구 정의하기
  - [ ] 6.5.4 [실습] 랭그래프로 에이전트 생성하기
  - [ ] 6.5.5 [실습] 문서를 기반으로 질문하고 답변 받아보기

</details>

## 관련 예제 코드

| 내용 | 경로 |
| --- | --- |
| 6.2 웹 검색 에이전트 | [`examples/web_agent`](examples/web_agent) |
| 6.3 코딩 에이전트 | [`examples/coding_agent`](examples/coding_agent) |
| 6.4 create_agent / 미들웨어 | [`examples/create_agent`](examples/create_agent) |
| 6.5 RAG 에이전트 | [`examples/rag_agent`](examples/rag_agent) |
| LangGraph Studio 설정 | [`examples/langgraph.json`](examples/langgraph.json) |

## `.env` 두는 위치

장 폴더에 `.env` 하나면 충분합니다. 단 `langgraph dev`는 `examples/`에서 실행하므로, 스튜디오를 쓸 때는 `examples/.env`도 함께 두세요(`langgraph.json`의 `env` 설정이 그 위치를 가리킵니다).

```powershell
copy .env.example .env
```

## 이 폴더 구성

- `06-01_…md` ~ `06-05_…md` — 절별 학습 노트
- `notes.md` — 장 전체 요약 (절 노트를 다 쓴 뒤 마지막에 정리)
- `practice/` — 예제를 보지 않고 직접 쳐보는 공간
- `.env.example` — 이 장에 필요한 API 키. `copy .env.example .env` 후 값을 채우세요

> **메모**  
> `langgraph dev`는 `langgraph.json`이 있는 디렉터리에서 실행합니다. 직접 만든 에이전트를 스튜디오로 띄우려면 `practice/`에 `langgraph.json`을 하나 만들어두세요.

---

[⬅ 전체 목차로](../STUDY.md)
