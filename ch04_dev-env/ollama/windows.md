# 올라마를 윈도우에 설치하기

[SETUP.md](../SETUP.md) §4 가 요구하는 **서버 주소를 만드는 문서**입니다. 붙을 서버가 이미 있으면 건너뛰세요.

결과 주소: `http://localhost:11434` · 검증: 2026-09-03 · Windows 11 · **관리자 권한 불필요**

---

## 설치

<https://ollama.com/download/OllamaSetup.exe> (약 1.5GB)

```powershell
Start-Process -FilePath .\OllamaSetup.exe -ArgumentList '/VERYSILENT','/NORESTART','/SUPPRESSMSGBOXES'
```

> **`-Wait` 를 붙이지 마세요.** 설치가 끝나면 트레이 앱이 떠서 반환되지 않습니다.
>
> **완료 판정은 API 로 하세요.** `ollama.exe` 는 10초 만에 생기지만 **서버가 응답하기까지 2분 반이 더** 걸립니다. 그 사이 `ollama pull` 을 치면 `could not connect to a running Ollama instance`.

설치가 끝나면 서버가 알아서 뜹니다. `ollama serve` 는 필요 없습니다.

```powershell
ollama pull qwen3.5:2b
ollama pull bge-m3
(Invoke-WebRequest http://localhost:11434/api/version).Content   # {"version":"0.33.2"}
```

여기까지 되면 [SETUP.md](../SETUP.md) §4 로 돌아가 `.env` 에 주소를 적습니다.

---

## 이 PC 에서 알아둘 것

**내장 GPU 는 안 씁니다.** 올라마가 Intel Arc 를 인식은 하되 일부러 버리고 CPU 로 갑니다(`dropping integrated GPU; to enable, set OLLAMA_IGPU_ENABLE=1`). CPU 만으로 `qwen3.5:2b` 가 9.2 tok/s 라 쓸 만합니다. 로그: `%LOCALAPPDATA%\Ollama\server.log`

**램은 이만큼 듭니다.**

| | |
| :--- | ---: |
| `qwen3.5:2b` (4k / 32k 컨텍스트) | 2.4 / 2.8 GB |
| `bge-m3` | 1.2 GB |
| **RAG (둘 동시)** | **약 4.0 GB** |

대화 모델만이면 8GB, RAG 까지 하면 16GB 를 권합니다. 모델은 마지막 요청 후 5분 뒤 내려가고, 재적재는 3.4초입니다.

---

## 지우기

```powershell
Get-Process -Name 'ollama','ollama app' -EA SilentlyContinue | Stop-Process -Force
Start-Process -Wait "$env:LOCALAPPDATA\Programs\Ollama\unins000.exe" -ArgumentList '/VERYSILENT','/NORESTART'
Remove-Item -LiteralPath "$env:USERPROFILE\.ollama" -Recurse -Force    # 모델까지
```

---

[⬅ Chapter 04](../README.md) · [SETUP.md](../SETUP.md) · [쿠버네티스에 배포](k8s.md)
