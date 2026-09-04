# 올라마를 윈도우에 설치하기

[SETUP.md](SETUP.md) §4 가 요구하는 **올라마 서버를 이 PC 에 준비하는 문서**입니다.

> **붙을 서버가 이미 있으면 이 문서는 건너뛰세요.** 사내 서버든 쿠버네티스든, `SETUP.md` §4 는 **주소 하나만** 봅니다.

| | |
| :--- | :--- |
| 검증 시점 | 2026-09-03 · Windows 11 · 관리자 권한 없는 계정 |
| 결과 주소 | `http://localhost:11434` |
| 대칭 문서 | 쿠버네티스에 올리려면 [ollama-k8s.md](ollama-k8s.md) |

---

## 1. 설치

- 다운로드: <https://ollama.com/download/OllamaSetup.exe> (약 1.5GB)

실행 전에 **서명을 확인합니다.**

```powershell
Get-AuthenticodeSignature .\OllamaSetup.exe |
  Format-List Status, @{n='Signer';e={$_.SignerCertificate.Subject}}
```

```
Status : Valid
Signer : CN="Ollama Inc.", O="Ollama Inc.", L=Toronto, S=Ontario, C=CA
```

**관리자 권한이 필요 없습니다.** `%LOCALAPPDATA%\Programs\Ollama` 에 설치되고 사용자 PATH 에 자동 등록됩니다.

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

---

## 2. 모델 받기

어떤 모델을 쓸지와 그 근거는 [SETUP.md](SETUP.md) §4.2 에 있습니다. 여기서는 받는 방법만 적습니다.

```powershell
ollama pull qwen3.5:2b
ollama pull bge-m3          # 임베딩용 (6·8·11장 RAG)
ollama list
```

```
NAME             ID              SIZE      MODIFIED
qwen3.5:2b       324d162be6ca    2.7 GB    2 seconds ago
bge-m3:latest    790764642607    1.2 GB    1 minute ago
```

---

## 3. 확인

```powershell
(Invoke-WebRequest http://localhost:11434/api/version).Content
```

```
{"version":"0.33.2"}
```

여기까지 되면 **[SETUP.md](SETUP.md) §4 로 돌아가** `.env` 에 이 주소를 적으면 됩니다.

```ini
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 4. 이 PC 에서만 걸리는 것

### 내장 GPU 는 안 씁니다

```
dropping integrated GPU; to enable, set OLLAMA_IGPU_ENABLE=1
  library=Vulkan name=Vulkan0 description="Intel(R) Arc(TM) Graphics"
inference compute: id=cpu library=cpu total=31.5GiB available=20.2GiB
```

- 올라마는 Intel Arc 내장 GPU 를 **인식은 하지만 일부러 버립니다.** 못 찾는 것이 아닙니다
- `OLLAMA_IGPU_ENABLE=1` 로 켤 수 있습니다. 더 빠른지는 재 봐야 합니다
- 그래도 쓸 만합니다 — CPU만으로 **`qwen3.5:2b` 가 9.2 tok/s**, 더 가벼운 `qwen3:1.7b` 는 14.9 tok/s
- 로그 위치: `%LOCALAPPDATA%\Ollama\server.log`

### 램은 얼마나 드나

> **실측 (2026-09-04 · `ollama ps`)**
>
> | | 점유 |
> | :--- | :--- |
> | `qwen3.5:2b` (4k 컨텍스트) | 2.4 GB |
> | `qwen3.5:2b` (32k 컨텍스트) | 2.8 GB |
> | `bge-m3` | 1.2 GB |
> | **RAG (둘 동시)** | **약 4.0 GB** |

- 대화 모델만 쓰면 **8GB** 로 충분합니다
- **RAG 는 16GB 를 권합니다** — 모델 2개가 동시에 올라갑니다
- 모델은 마지막 요청 후 **5분 뒤 자동으로 내려갑니다**(`OLLAMA_KEEP_ALIVE` 기본값). 재적재 비용은 **약 3.4초**(콜드 5.55초 − 웜 2.15초)

---

## 5. 지우기

```powershell
Get-Process -Name 'ollama','ollama app' -EA SilentlyContinue | Stop-Process -Force
Start-Process -Wait "$env:LOCALAPPDATA\Programs\Ollama\unins000.exe" -ArgumentList '/VERYSILENT','/NORESTART'
Remove-Item -LiteralPath "$env:USERPROFILE\.ollama" -Recurse -Force    # 모델까지
```

---

[⬅ Chapter 04](README.md) · [SETUP.md 로 돌아가기](SETUP.md) · [쿠버네티스는 ollama-k8s.md](ollama-k8s.md)
