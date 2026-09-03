# 개발 환경 구축

교재 4장의 환경 설정을 **상업적으로 문제없는 구성**으로 다시 정리한 문서입니다.
교재는 아나콘다(Anaconda)를 쓰지만, 여기서는 **미니포지(Miniforge)** 를 씁니다. 이유는 §2에 있습니다.

| | |
| :--- | :--- |
| 대상 | Windows 11 · 관리자 권한 없는 계정 |
| 파이썬 | **3.12.14** |
| LLM | **올라마 · `qwen3.5:2b`** (API 키 없이 진행) |
| 확인 시점 | 2026-09-03 |

> 이 문서의 모든 명령과 출력은 **실제로 실행해 얻은 것**입니다. 버전이 다르면 출력도 달라집니다.

---

## 1. VS Code 설치

- 다운로드: <https://code.visualstudio.com/>

설치 후 확장 두 개만 깔면 4장 실습에 충분합니다.

| 확장 | ID |
| :--- | :--- |
| Python | `ms-python.python` |
| Jupyter | `ms-toolsai.jupyter` |

> **인터프리터를 직접 골라 주세요.** `Ctrl+Shift+P` → `Python: Select Interpreter` 에서 §3에서 만든 환경을 고릅니다. 안 고르면 시스템 파이썬이 잡혀 `ModuleNotFoundError` 가 납니다.

---

## 2. 미니포지 — 왜 아나콘다가 아닌가

### 2.1 라이선스

문제가 되는 것은 `conda` 라는 **도구**가 아니라, 패키지를 받아오는 **채널**입니다.

| 대상 | 라이선스 | 상업적 사용 |
| :--- | :--- | :--- |
| `conda` 도구 자체 | BSD-3 | 자유 |
| 미니콘다 설치 프로그램 | Miniconda EULA | 자유 |
| **`defaults` 채널** (`repo.anaconda.com`) | Anaconda ToS | **직원·계약자 200명 이상 조직은 유료** |
| `conda-forge` 채널 | 각 패키지의 OSS 라이선스 | 자유 |

- **아나콘다 배포판(Anaconda Distribution)** 과 **미니콘다(Miniconda)** 는 둘 다 기본 채널이 `defaults` 입니다. 설치 직후 `conda install` 을 치는 순간 유료 대상 저장소를 씁니다
- **미니포지(Miniforge)** 는 기본 채널이 `conda-forge` 입니다. 설정을 건드리지 않아도 Anaconda 저장소에 접속하지 않습니다
- 조직이 200명 미만이면 미니콘다 + `defaults` 도 무료입니다. 다만 경계에 걸릴 여지를 만들지 않으려고 미니포지를 골랐습니다

> **`conda install anaconda` 는 치지 마세요.** Anaconda Distribution 메타패키지로, 명백히 유료 라이선스 대상입니다.

> **ToS 동의 프롬프트가 뜨면 신호입니다.** 2025-07-15 이후 미니콘다는 Anaconda 저장소 접근 시 `conda tos accept` 를 요구합니다. 미니포지를 제대로 설치했다면 이 프롬프트를 볼 일이 없습니다.

> 법률 자문이 아닙니다. 조직 규모가 200명대 근처거나 재배포가 얽히면 [Anaconda ToS 원문](https://www.anaconda.com/legal/terms/terms-of-service)을 법무에 확인하세요.

### 2.2 설치

- 다운로드: <https://github.com/conda-forge/miniforge/releases> 내 `Miniforge3-Windows-x86_64.exe`
- 또는: `winget install --id=CondaForge.Miniforge3 -e`

실행 전에 **서명을 확인합니다.** conda-forge 배포본은 재정 후원 기관인 NumFOCUS 이름으로 서명돼 있습니다.

```powershell
Get-AuthenticodeSignature .\Miniforge3-Windows-x86_64.exe |
  Format-List Status, @{n='Signer';e={$_.SignerCertificate.Subject}}
```

```
Status : Valid
Signer : CN="NumFOCUS, Inc.", O="NumFOCUS, Inc.", L=Austin, S=Texas, C=US
```

설치 마법사에서 고를 것:

| 항목 | 선택 | 이유 |
| :--- | :--- | :--- |
| Installation Type | **Just Me** | 관리자 권한이 없어도 됩니다 |
| Destination | `C:\Users\<사용자>\miniforge3` | **공백·한글·괄호 없는 경로.** 있으면 conda가 깨집니다 |
| Add to PATH | **해제** | 시작 메뉴의 "Miniforge Prompt" 로 씁니다 |
| Register as default Python | 해제 | 시스템 파이썬을 건드리지 않습니다 |

무인 설치 (`/D=` 는 **맨 뒤 · 따옴표 없이**):

```powershell
Start-Process -Wait -FilePath .\Miniforge3-Windows-x86_64.exe -ArgumentList `
  '/InstallationType=JustMe','/RegisterPython=0','/AddToPath=0','/S','/D=C:\Users\dorim\miniforge3'
```

### 2.3 설치 확인

**PATH에 넣지 않았으므로 conda 를 부르는 방법이 셋으로 갈립니다.** 이걸 먼저 정하고 넘어가세요 — 이 문서의 나머지 명령이 전부 여기에 달려 있습니다.

| 상황 | 방법 |
| :--- | :--- |
| **대화형으로 이것저것 해 볼 때** | 시작 메뉴 → **"Miniforge Prompt"**. `conda activate` 가 바로 됩니다 |
| **VS Code 터미널·PowerShell 에서 쓸 때** | `conda init powershell` 을 **한 번** 실행하고 창을 다시 엽니다. PATH는 안 건드리고 PowerShell 프로필에만 씁니다 |
| **스크립트에서 부를 때** | 환경의 파이썬을 **전체 경로로 직접** 부릅니다 (아래) |

```powershell
# 스크립트용 - 활성화가 필요 없습니다
C:\Users\<사용자>\miniforge3\envs\agent\python.exe your_script.py
C:\Users\<사용자>\miniforge3\Scripts\conda.exe list -n agent
```

> **`conda activate` 는 그냥은 안 됩니다.** 초기화하지 않은 PowerShell 에서 치면 이렇게 나옵니다.
>
> ```
> CondaError: Run 'conda init' before 'conda activate'
> ```

> **`conda run -n agent python ...` 는 쓰지 마세요.** 자식 프로세스의 출력을 conda 가 다시 찍는데, 한국어 콘솔(cp949)에서 **한글이 깨지고 결국 죽습니다.**
>
> ```
> UnicodeEncodeError: 'cp949' codec can't encode character '\ufffd'
> ```
>
> 이 저장소의 검사 스크립트는 한국어를 출력합니다. **환경의 `python.exe` 를 직접 부르세요.**

```powershell
conda --version
conda config --show channels
```

```
conda 26.5.3
channels:
  - conda-forge
```

- **`conda-forge` 만 있어야 합니다.** `defaults` 나 `repo.anaconda.com` 이 한 줄이라도 보이면 잘못된 것입니다

섞여 있다면 이렇게 고칩니다.

```powershell
conda config --add channels conda-forge
conda config --set channel_priority strict
conda config --remove channels defaults
```

설정 파일이 어디서 오는지는 `conda config --show-sources` 로 봅니다. **갓 설치한 상태에서는 한 개뿐입니다.**

```
==> C:\Users\<사용자>\miniforge3\.condarc <==
channels:
  - conda-forge
```

| 파일 | 들어 있는 것 | 언제 생기나 |
| :--- | :--- | :--- |
| `<설치경로>\.condarc` | `channels: [conda-forge]` | **설치 프로그램이 만들어 줍니다** |
| `%USERPROFILE%\.condarc` | 사용자가 바꾼 설정 | `conda config --set …` 을 칠 때 비로소 생깁니다 |

> **`channel_priority: strict` 는 필수가 아닙니다.** 채널이 `conda-forge` 하나뿐이라 우선순위를 정할 대상이 없습니다. 나중에 채널을 더 추가할 생각이면 그때 걸어 두세요.

---

## 3. 파이썬 3.12.14 환경과 패키지

### 3.1 환경 만들기

> **base는 건드리지 않습니다.** 미니포지 base의 파이썬은 **3.14.7** 로 최신입니다. 교재가 가정하는 버전과 다르니 base를 다운그레이드하지 말고 이름 붙인 환경을 따로 만듭니다.

```powershell
conda create -n agent "python=3.12.14" -c conda-forge --override-channels -y
```

확인은 §2.3에서 정한 방법으로 합니다. 활성화 없이 확인하려면:

```powershell
C:\Users\<사용자>\miniforge3\envs\agent\python.exe --version   # Python 3.12.14
```

### 3.2 패키지 설치

교재 4장에 필요한 셋입니다. **셋 다 conda-forge에 있어서 pip를 섞지 않아도 됩니다.**

```powershell
conda install -n agent -c conda-forge --override-channels -y `
  "langgraph<2" "langchain-openai<2" python-dotenv
```

6장 이후의 `create_agent`(`langchain.agents`)를 쓰려면 본체도 필요합니다.

```powershell
conda install -n agent -c conda-forge --override-channels -y "langchain<2"
```

설치 결과 (2026-09-03):

| 패키지 | 버전 | 비고 |
| :--- | :--- | :--- |
| langgraph | 1.2.11 | 직접 설치 |
| langchain | 1.3.18 | 직접 설치 · 6장부터 필요 |
| langchain-openai | 1.6.0 | 직접 설치 |
| python-dotenv | 1.2.3 | 직접 설치 |
| langchain-core | 1.6.1 | 의존성 |
| openai | 2.53.0 ~ 3.7.0 | 의존성 — **범위입니다** |

> **의존성 버전은 이 표대로 안 나올 수 있습니다.** `langchain-openai 1.6.0` 이 요구하는 것은 `openai>=2.45.0,<4.0.0` 이라, 같은 명령을 두 번 돌려도 솔버가 다른 버전을 고릅니다. 실제로 재설치했더니 `3.7.0` 이 `2.53.0` 으로 바뀌었고, **동작에는 차이가 없었습니다.**
>
> **직접 설치한 넷의 버전만 맞으면 됩니다.** 의존성까지 고정해야 한다면 `conda list --explicit` 로 잠가 두세요.

> **버전 상한 `<2` 를 반드시 붙입니다.** 풀면 교재 예제가 깨집니다. 근거는 [CLAUDE.md](../CLAUDE.md) §6.

> **conda와 pip를 섞지 마세요.** 의존성 추적이 어긋납니다. **conda-forge에 있으면 conda로** 깔고, 없을 때만 pip를 씁니다.

### 3.3 확인

```powershell
conda list -n agent --show-channel-urls
```

- 모든 줄의 마지막 칸이 `conda-forge` 여야 합니다. `defaults` 나 `pkgs/main` 이 하나라도 있으면 §2.1의 유료 채널에서 받아온 것입니다

import 확인 (`<사용자>` 부분만 바꿔 그대로 붙여 넣으면 됩니다):

```powershell
C:\Users\<사용자>\miniforge3\envs\agent\python.exe -c "from langgraph.graph import StateGraph; from langchain_openai import ChatOpenAI; from dotenv import load_dotenv; print('OK')"
```

---

## 4. 올라마 설치와 연결 테스트

API 키 없이 로컬에서 모델을 돌리는 쪽입니다. 4·5·8장은 이것만으로 진행할 수 있습니다.

### 4.1 설치

- 다운로드: <https://ollama.com/download/OllamaSetup.exe> (약 1.5GB)

```powershell
Get-AuthenticodeSignature .\OllamaSetup.exe |
  Format-List Status, @{n='Signer';e={$_.SignerCertificate.Subject}}
```

```
Status : Valid
Signer : CN="Ollama Inc.", O="Ollama Inc.", L=Toronto, S=Ontario, C=CA
```

**관리자 권한이 필요 없습니다.** `%LOCALAPPDATA%\Programs\Ollama` 에 설치되고 사용자 PATH에 자동 등록됩니다.

```powershell
Start-Process -FilePath .\OllamaSetup.exe -ArgumentList '/VERYSILENT','/NORESTART','/SUPPRESSMSGBOXES'
```

> **`-Wait` 를 붙이지 마세요.** 설치가 끝나면 설치 프로그램이 **트레이 앱을 띄우고**, `-Wait` 가 그 프로세스까지 기다리느라 반환되지 않습니다. 10분을 기다리다 죽였는데 **설치는 이미 성공한 상태**였습니다.

설치가 끝나면 **서버가 알아서 뜹니다.** `ollama serve` 를 따로 칠 필요가 없습니다.

> **완료 판정은 파일이 아니라 API로 하세요.** `ollama.exe` 는 설치 시작 **10초 만에** 생기지만, 서버가 응답하기까지 거기서 **2분 반이 더** 걸립니다. 그 사이에 `ollama pull` 을 치면 이렇게 됩니다.
>
> ```
> Warning: could not connect to a running Ollama instance
> ```
>
> API가 응답할 때까지 기다렸다가 다음으로 넘어가세요.
>
> ```powershell
> $limit = (Get-Date).AddMinutes(8)
> do { try { $r = Invoke-WebRequest 'http://localhost:11434/api/version' -TimeoutSec 5 -EA Stop } catch { Start-Sleep 10 } }
> until ($r -or (Get-Date) -gt $limit)
> $r.Content
> ```

### 4.2 모델 고르기

**이 장은 `qwen3.5:2b` 를 씁니다.**

```powershell
ollama pull qwen3.5:2b
ollama list
```

```
NAME          ID              SIZE      MODIFIED
qwen3.5:2b    324d162be6ca    2.7 GB    2 seconds ago
```

| | |
| :--- | :--- |
| 파라미터 | 2.3B |
| 컨텍스트 | 262,144 |
| 양자화 | Q8_0 |
| 능력 | completion · **tools** · vision · thinking |

**왜 이 모델인가.** 4B 이하 모델 여섯 개를 같은 검사로 돌려 골랐습니다. 도구를 다루는 능력이 갈립니다.

| 모델 | 크기 | 도구 호출 | 도구 선택 | 병렬 호출 | CPU 속도 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| Qwen3.5 0.8B | 0.9B | ✅ | ✅ | ✅ | 5~9초 |
| Qwen3 1.7B | 1.7B | ✅ | ✅ | ✅ | 15 tok/s |
| **Qwen3.5 2B** | **2.3B** | **✅** | **✅** | **✅** | **9 tok/s** |
| Qwen3 4B | 4B | ✅ | ✅ | ✅ | 53~87초 |
| Granite 4.2 3B | 3B | △ | ❌ | ✅ | — |
| Phi-4 Mini | 3.8B | ❌ | ❌ | ❌ | — |

- **크기가 능력을 정하지 않습니다.** 0.9B가 되고 3.8B가 안 됩니다
- 더 가볍게 가려면 `qwen3.5:0.8b`, 더 정확하게 가려면 `qwen3:4b` 로 바꾸면 됩니다. `.env` 한 줄만 고치면 됩니다

**직접 재보려면.** 위 표를 만든 검사가 저장소에 있습니다. 모델을 여러 개 넘기면 나란히 비교해 줍니다.

```powershell
C:\Users\<사용자>\miniforge3\envs\agent\python.exe scripts\check-parallel-tools.py qwen3.5:2b qwen3:4b phi4-mini
```

> **`ollama show` 의 `capabilities: tools` 를 믿지 마세요.** 위 여섯 모델이 **전부** `tools` 를 선언하지만, Granite와 Phi-4 Mini는 실제로는 실패합니다. 도구를 부르려는 의도는 있는데 **형식을 못 지켜 본문에 텍스트로 뱉습니다.**
>
> ```
> granite4.2:3b  ->  본문에: <tools><function=get_weather><par...
> phi4-mini      ->  본문에: [{"type"...
> ```
>
> 파싱이 안 되니 `tool_calls` 가 빕니다. **모델을 바꾸면 §4.5를 반드시 다시 돌리세요.**

### 4.3 서버 연결 확인

가장 먼저 볼 것. 모델 없이도 됩니다.

```powershell
(Invoke-WebRequest http://localhost:11434/api/version).Content
```

```
{"version":"0.33.2"}
```

### 4.4 `.env` 설정

**접속 정보는 저장소 루트의 `.env` 하나로 관리합니다.** 장별로 두지 않습니다.

```powershell
copy .env.example .env      # 저장소 루트에서 한 번만
```

루트 [`.env.example`](../.env.example) 이 템플릿입니다. 4장에 필요한 부분은 이 셋입니다.

```ini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:2b
# 임베딩용(6·8·11장 RAG). 한국어를 다루면 다국어 모델이어야 합니다.
OLLAMA_EMBED_MODEL=bge-m3

# OpenAI API 로 돌릴 때만 채웁니다. OLLAMA_MODEL 이 비어 있으면 이쪽을 씁니다.
OPENAI_API_KEY=
```

- **모델을 바꾸는 곳은 여기 한 줄입니다.** 코드에 모델 이름을 박지 마세요 — 올라마 모델 태그는 자주 바뀝니다
- 사내·원격 올라마 서버를 쓴다면 `OLLAMA_BASE_URL` 만 그 주소로 바꿉니다. 설치도 필요 없습니다

> **`.env` 는 `.gitignore` 에 있습니다.** 확인: `git check-ignore -v .env`
> **키를 출력하지 마세요.** 노트북 셀 출력은 커밋됩니다.

### 4.5 연결 테스트 코드

[`check_ollama.py`](check_ollama.py) 를 실행합니다. `.env` 를 읽어 붙고, 4장에서 쓸 기능 셋이 실제로 도는지 확인합니다.

| 검사 | 무엇을 보나 |
| :--- | :--- |
| [1] 단순 호출 | 4·5·8장에 필요. 생성 속도(tok/s)도 함께 잽니다 |
| [2] 도구 호출 | 6장 이후의 관건 |
| [3] 구조화 출력 | 라우터. **되는 `method` 를 자동으로 찾아 알려 줍니다** |
| [4] 병렬 호출 | 한 응답에 도구를 여러 개 부를 수 있는가 |

```powershell
C:\Users\<사용자>\miniforge3\Scripts\conda.exe install -n agent -c conda-forge --override-channels -y "langchain-ollama<2"
C:\Users\<사용자>\miniforge3\envs\agent\python.exe ch04_dev-env\check_ollama.py
```

실행 결과 (qwen3.5:2b · CPU):

```
서버 : http://localhost:11434
모델 : qwen3.5:2b

[1] 단순 호출  : 261토큰 / 35.0초 / 7.5 tok/s
[2] 도구 호출  : get_weather({'city': '서울'})
    method='function_calling' 실패: AttributeError
[3] 구조화 출력: 기타 (method='json_schema')   <- 오분류. 정답은 환불
[4] 병렬 호출  : ['get_weather', 'get_time']  (한 응답에 2건)
```

**[2]와 [4]가 통과하면 6장 이후로 넘어갈 수 있습니다.** [3]에 적힌 `method` 는 코드에 그대로 써야 하는 값입니다(§4.6 ①).

> **`tok/s` 는 재볼 때마다 다릅니다.** 같은 PC·같은 모델로 네 번 재서 7.2 · 7.5 · 9.2 · 9.9 가 나왔습니다. 다른 컴퓨터의 부하·전원 설정에 따라 더 벌어집니다. **숫자를 맞추려 하지 말고 [2]~[4]가 통과하는지만 보세요.**

> 도구 두 개 중에서 고르게 하는 검사는 저장소의 `scripts/check-ollama.py` 에 있습니다.

### 4.6 결과를 읽는 법 — 함정 셋

**① 구조화 출력의 `method` 는 모델마다 다릅니다.**

| 모델 | 되는 method |
| :--- | :--- |
| **qwen3.5:2b** (이 장의 기본) | **`json_schema`** — `function_calling` 은 `None` 을 뱉어 `AttributeError` |
| qwen3:1.7b | `json_schema` |
| qwen3.5:9b-q4_K_M (사내 서버) | `function_calling` |

```python
# qwen3.5:2b 기준. 기본값(json_schema)이지만 명시해 두는 편이 낫습니다.
chain = llm.with_structured_output(Schema, method="json_schema")
```

모델을 바꾸면 §4.5를 다시 돌려 **어느 method가 되는지부터** 확인하세요. 코드에 하드코딩하기 전에 확인해야 합니다.

**② 통과했다고 정확한 것은 아닙니다.**

`qwen3.5:2b` 는 *"이거 마음에 안 들어요. 돈 돌려주세요"* 를 **`환불` 이 아니라 `기타` 로 분류했습니다.** 스키마는 맞췄지만 판단이 틀렸습니다. 1.7b도 같은 문제를 냈습니다.

- 검사 통과 = **형식이 맞는다**는 뜻입니다. 정확하다는 뜻이 아닙니다
- 2B는 4·5장 연습용으로 충분합니다. 6장 이후처럼 도구가 많아지고 대화가 길어지면 떨어집니다
- 정확도가 필요하면 `.env` 의 `OLLAMA_MODEL` 을 더 큰 모델로 바꾸거나 OpenAI API를 쓰세요

> **`Literal` 로 좁히세요.** 스키마 필드가 그냥 `str` 이면 모델이 아무 말이나 채웁니다. 후보를 `Literal["환불", "배송", "기타"]` 로 못박아야 최소한 값의 범위는 지켜집니다.

**③ 내장 GPU는 안 씁니다.**

```
dropping integrated GPU; to enable, set OLLAMA_IGPU_ENABLE=1
  library=Vulkan name=Vulkan0 description="Intel(R) Arc(TM) Graphics"
inference compute: id=cpu library=cpu total=31.5GiB available=20.2GiB
```

- 올라마는 Intel Arc 내장 GPU를 **인식은 하지만 일부러 버립니다.** 못 찾는 것이 아닙니다
- `OLLAMA_IGPU_ENABLE=1` 로 켤 수 있습니다. 더 빠른지는 재 봐야 합니다
- 그래도 쓸 만합니다 — CPU만으로 **qwen3.5:2b 가 9.2 tok/s**, 더 가벼운 qwen3:1.7b 는 14.9 tok/s
- 로그 위치: `%LOCALAPPDATA%\Ollama\server.log`

> **`reasoning=False` 를 꼭 넣으세요.** qwen3 계열은 생각을 글로 뱉습니다. 안 끄면 같은 답에 몇 배가 걸립니다.
>
> ```python
> llm = ChatOllama(model=MODEL, temperature=0, base_url=BASE, reasoning=False)
> ```

---

## 5. 한눈에 보기

| 구성 요소 | 버전 | 설치 위치 |
| :--- | :--- | :--- |
| VS Code | — | — |
| 미니포지 (conda) | 26.5.3 | `%USERPROFILE%\miniforge3` |
| 파이썬 (`agent` 환경) | **3.12.14** | `…\miniforge3\envs\agent` |
| 올라마 | 0.33.2 | `%LOCALAPPDATA%\Programs\Ollama` |
| 올라마 모델 | **qwen3.5:2b** (2.3B · Q8_0) | `%USERPROFILE%\.ollama\models` |

전부 **관리자 권한 없이** 사용자 프로필에만 설치됩니다.

### 매번 확인할 것

활성화 없이 도는 형태로 적었습니다. `<사용자>` 만 바꿔 쓰세요.

```powershell
$conda = "C:\Users\<사용자>\miniforge3\Scripts\conda.exe"
$py    = "C:\Users\<사용자>\miniforge3\envs\agent\python.exe"

& $conda config --show channels                   # conda-forge 만
& $py --version                                   # 3.12.14
(Invoke-WebRequest http://localhost:11434/api/version).Content
& $py ch04_dev-env\check_ollama.py                # 검사 4종
```

> **`conda run` 으로 바꾸지 마세요.** 한글 출력이 깨집니다(§2.3).

### 이 장에서 정한 값

| | |
| :--- | :--- |
| 모델 | `qwen3.5:2b` — `.env` 의 `OLLAMA_MODEL` |
| 구조화 출력 method | `json_schema` |
| `ChatOllama` 필수 인자 | `temperature=0, reasoning=False` |
| 6장 이후 가능 여부 | 도구 호출 ✅ · 도구 선택 ✅ · 병렬 호출 ✅ |

---

## 6. 참고

- [Anaconda Terms of Service](https://www.anaconda.com/legal/terms/terms-of-service)
- [Miniconda EULA](https://www.anaconda.com/legal/terms/miniconda)
- [Miniforge (conda-forge)](https://github.com/conda-forge/miniforge)
- [Ollama](https://ollama.com/)
- 이 저장소의 버전 상한 근거: [CLAUDE.md](../CLAUDE.md) §6
