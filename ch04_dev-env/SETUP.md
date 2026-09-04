# 개발 환경 구축

교재 4장. **상업적으로 문제없는 구성**으로 정리했습니다.

| | |
| :--- | :--- |
| 대상 | Windows 11 · 관리자 권한 없는 계정 |
| 파이썬 | 3.12.14 (conda 환경 `agent`) |
| LLM | 올라마 · `qwen3.5:2b` (API 키 불필요) |
| 확인 | 2026-09-04 · 전 과정 재현 검증 |

`<사용자>` 는 본인 계정으로 바꿔 쓰세요.

---

## 1. VS Code

<https://code.visualstudio.com/> · 확장 `ms-python.python` · `ms-toolsai.jupyter`

> `Ctrl+Shift+P` → **Python: Select Interpreter** 에서 §3의 `agent` 환경을 고르세요. 안 고르면 `ModuleNotFoundError` 가 납니다.

---

## 2. 미니포지

**아나콘다가 아니라 미니포지입니다.** 유료 대상은 `conda` 도구가 아니라 **채널**입니다 — `defaults`(repo.anaconda.com)는 직원 200명 이상 조직에 유료이고, 미니포지는 기본 채널이 `conda-forge` 라 그 저장소에 접속하지 않습니다. ([근거](https://www.anaconda.com/legal/terms/terms-of-service) · 판단 이력은 [history.md](../history.md) ⑫)

<https://github.com/conda-forge/miniforge/releases> 에서 `Miniforge3-Windows-x86_64.exe`

```powershell
Start-Process -Wait -FilePath .\Miniforge3-Windows-x86_64.exe -ArgumentList `
  '/InstallationType=JustMe','/RegisterPython=0','/AddToPath=0','/S','/D=C:\Users\<사용자>\miniforge3'
```

```powershell
C:\Users\<사용자>\miniforge3\Scripts\conda.exe config --show channels   # conda-forge 만 나와야 함
```

> **`conda install anaconda` 는 치지 마세요.** 유료 대상입니다.

### conda 를 부르는 법 — 먼저 정하고 넘어가세요

PATH에 넣지 않았으므로 셋 중 하나입니다.

| 상황 | 방법 |
| :--- | :--- |
| 대화형 | 시작 메뉴 → **Miniforge Prompt** |
| VS Code 터미널 | `conda init powershell` **한 번** 실행 후 창 다시 열기 |
| 스크립트 | `…\miniforge3\envs\agent\python.exe` **전체 경로로 직접** |

> **`conda activate` 를 그냥 치면** `CondaError: Run 'conda init' before 'conda activate'`
>
> **`conda run` 은 쓰지 마세요.** 한글 출력이 cp949에서 깨지고 죽습니다.

---

## 3. 파이썬 환경과 패키지

```powershell
$conda = "C:\Users\<사용자>\miniforge3\Scripts\conda.exe"

& $conda create -n agent "python=3.12.14" -c conda-forge --override-channels -y
& $conda install -n agent -c conda-forge --override-channels -y `
  "langgraph<2" "langchain<2" "langchain-openai<2" "langchain-ollama<2" python-dotenv
```

6장 이후는 그 장에 갈 때 추가합니다 — 장별 목록은 [STUDY.md](../STUDY.md#올라마로-어디까지-되나).

> **버전 상한 `<2` 를 반드시 붙입니다.** 풀면 교재 예제가 깨집니다([CLAUDE.md](../CLAUDE.md) §6).
>
> **`--override-channels`** 를 붙이면 설정이 꼬여도 유료 채널을 안 탑니다.

```powershell
& $conda list -n agent --show-channel-urls    # 전 줄이 conda-forge 여야 함
```

---

## 4. 올라마에 연결

**서버가 어디서 도는지는 학습에 차이가 없습니다.** 주소 하나만 있으면 됩니다.

| 서버가 | |
| :--- | :--- |
| 있다 | 주소만 아래 `.env` 에 |
| 없다 | [윈도우에 설치](ollama/windows.md) 또는 [쿠버네티스에 배포](ollama/k8s.md) |

### `.env` — 저장소 루트 하나로 관리합니다

```powershell
copy .env.example .env      # 저장소 루트에서 한 번만
```

```ini
OLLAMA_BASE_URL=http://<주소>:11434
OLLAMA_MODEL=qwen3.5:2b
OLLAMA_EMBED_MODEL=bge-m3
OPENAI_API_KEY=
```

> **`http://` 입니다.** 올라마는 평문 HTTP 로만 서비스합니다. `https://` 로 적으면 `SSL connection could not be established`.
>
> **모델을 바꾸는 곳은 여기 한 줄입니다.** 코드에 박지 마세요.

### 연결 테스트

```powershell
C:\Users\<사용자>\miniforge3\envs\agent\python.exe ch04_dev-env\ollama\check_ollama.py
```

```
[1] 단순 호출  : 262토큰 / 35.0초 / 7.5 tok/s
[2] 도구 호출  : get_weather({'city': '서울'})
    method='function_calling' 실패: AttributeError
[3] 구조화 출력: 기타 (method='json_schema')   <- 오분류. 정답은 환불
[4] 병렬 호출  : ['get_weather', 'get_time']  (한 응답에 2건)
```

**[2]와 [4]가 통과하면 6장 이후로 갈 수 있습니다.**

---

## 5. 결과를 읽는 법 — 함정 셋

**① 구조화 출력의 `method` 는 모델마다 다릅니다.**

`qwen3.5:2b` 는 `json_schema`, 사내 9B 는 `function_calling` 이었습니다. 기본값으로 두면 `None` 이 와서 `AttributeError` 로 죽습니다. **모델을 바꾸면 위 검사부터 다시 돌리세요** — 되는 `method` 를 찾아 알려 줍니다.

```python
chain = llm.with_structured_output(Schema, method="json_schema")
```

**② 통과 = 형식이 맞는다는 뜻입니다.** 정확하다는 뜻이 아닙니다. `qwen3.5:2b` 는 *"돈 돌려주세요"* 를 `환불` 이 아니라 `기타` 로 분류했습니다. 스키마 필드는 `Literal` 로 좁히세요.

**③ `reasoning=False` 를 꼭 넣으세요.** qwen3 계열은 생각을 글로 뱉어 몇 배 느려집니다.

```python
llm = ChatOllama(model=MODEL, temperature=0, base_url=BASE, reasoning=False)
```

> `tok/s` 는 재볼 때마다 다릅니다(같은 PC에서 7.2~9.9). **숫자를 맞추려 하지 말고 [2]~[4] 통과만 보세요.**

---

## 6. 매번 확인할 것

```powershell
$conda = "C:\Users\<사용자>\miniforge3\Scripts\conda.exe"
$py    = "C:\Users\<사용자>\miniforge3\envs\agent\python.exe"

& $conda config --show channels                   # conda-forge 만
& $py --version                                   # 3.12.14
(Invoke-WebRequest http://<주소>:11434/api/version).Content
& $py ch04_dev-env\ollama\check_ollama.py
```

---

[⬅ Chapter 04](README.md) · [전체 목차](../STUDY.md)
