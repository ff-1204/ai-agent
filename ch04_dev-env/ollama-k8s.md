# 올라마를 쿠버네티스에 올리기

[SETUP.md](SETUP.md) §4 가 요구하는 **올라마 서버를 쿠버네티스에 준비하는 문서**입니다. 나머지(VS Code · 미니포지 · 파이썬 · 패키지)는 그대로 `SETUP.md` 를 따르세요.

> **서버를 어디에 두든 학습 경로는 같습니다.** 준비가 끝나면 주소만 `.env` 에 적고 `SETUP.md` §4 로 돌아가면 됩니다. 윈도우에 두는 쪽은 [ollama-windows.md](ollama-windows.md).

| | |
| :--- | :--- |
| 매니페스트 | [`ollama-k8s.yaml`](ollama-k8s.yaml) |
| 검증 시점 | 2026-09-04 · 사내 클러스터 (NFS · NodePort) — **전 과정 실행 확인**(§7) |
| 하는 일 | 올라마 서버를 띄우고 **주소를 만드는 것**까지 |
| 그 뒤 | `SETUP.md` §4.1~§4.5 — 서버 위치와 무관하게 동일 |

> **교재에 없는 확장입니다.** 교재 4장은 로컬 설치를 다룹니다. 이 문서는 올라마를 팀이 공유하거나 노트북 자원을 아끼고 싶을 때 쓰는 쪽입니다.

---

## 1. 무엇이 들어 있나

[`ollama-k8s.yaml`](ollama-k8s.yaml) 한 파일에 오브젝트 넷이 있습니다.

| 오브젝트 | 하는 일 |
| :--- | :--- |
| **PersistentVolumeClaim** | 모델 저장소. 파드가 죽어도 모델을 다시 안 받게 합니다 |
| **Deployment** | 올라마 서버 |
| **Service** | 클러스터 안에서 붙는 주소 |
| **Job** | 모델을 미리 받아 둡니다 |

### 왜 이렇게 잡았나

| 설정 | 값 | 이유 |
| :--- | :--- | :--- |
| `strategy` | `Recreate` | RWO 볼륨을 한 파드가 잡습니다. RollingUpdate 면 새 파드가 볼륨을 못 붙고 Pending |
| `OLLAMA_HOST` | `0.0.0.0:11434` | **기본값이 `127.0.0.1`** 입니다. 이걸 안 주면 Service 로 붙어도 연결이 안 됩니다 |
| `OLLAMA_MAX_LOADED_MODELS` | `2` | RAG 는 대화 모델과 임베딩 모델을 **동시에** 올립니다. 1 이면 서로를 밀어냅니다 |
| `requests.memory` | `5Gi` | **클러스터 실측 3.33GB**(ctx 4096). 컨텍스트·병렬을 키울 여지를 둔 값 |
| `limits.memory` | `8Gi` | CPU 추론은 램을 넘기면 **OOMKilled** 로 죽습니다. 실측 3.33GB 라 여유 있음 |
| `storage` | `20Gi` | 모델 3개 실측 3.67GB. 여유 충분 |
| `startupProbe` | 최대 5분 | 서버 기동에 시간이 걸립니다. 없으면 liveness 가 뜨는 중에 재시작시킵니다 |
| `OLLAMA_KEEP_ALIVE` | `-1` | **NFS 재적재가 10초 넘습니다**(§4.5). 3.33GB 라 requests 안에 들어가므로 안 내리는 편이 낫습니다 |

---

## 2. 이미지 태그 — 여기서 제일 많이 막힙니다

**모델마다 요구하는 올라마 버전이 있습니다.** 이미지가 그보다 낮으면 `pull` 이 막힙니다.

> **실측 (2026-09-04)** — `ollama/ollama:0.13.0` 으로 배포했다가 Job 이 이렇게 실패했습니다.
>
> ```
> 서버 대기 중…
> 서버 준비됨
> pulling manifest
> Error: pull model manifest: 412:
> The model you are attempting to pull requires a newer version of Ollama.
> ```

요구 버전은 **모델 쪽에 적혀 있습니다.**

```powershell
ollama show qwen3.5:2b
```

```
    architecture        qwen35
    parameters          2.3B
    requires            0.17.1      ← 이 값 이상이어야 합니다
```

| | |
| :--- | :--- |
| `qwen3.5:2b` 요구 | **0.17.1** 이상 |
| 매니페스트가 쓰는 태그 | **`0.33.2`** (로컬과 같은 버전이라 동작이 확인된 조합) |

> **`latest` 를 쓰지 마세요.** 당장은 되지만 어느 날 모델 호환성이 조용히 바뀝니다. **태그를 고정하되 `requires` 를 넘는 값**으로 잡으세요.
>
> 실재하는 태그인지는 [Docker Hub 태그 목록](https://hub.docker.com/r/ollama/ollama/tags)에서 확인합니다. 추측해서 적으면 위 412 를 만납니다.

---

## 3. 배포

`namespace` 와 `storageClassName` 을 환경에 맞게 고친 뒤 적용합니다.

```bash
kubectl apply -f ollama-k8s.yaml
```

```bash
kubectl -n <네임스페이스> rollout status deploy/ollama
```

### PVC 가 바로 Bound 안 돼도 정상입니다

StorageClass 에 `volumeBindingMode: WaitForFirstConsumer` 가 걸려 있으면 **파드가 스케줄될 때까지 `Pending`** 입니다. 오류가 아니라 설계된 동작입니다.

```bash
kubectl -n <네임스페이스> get pvc,pod -l app=ollama
```

### 모델 받기

Job 이 자동으로 받습니다. **Deployment 가 먼저 Ready 여야** 합니다.

```bash
kubectl -n <네임스페이스> logs -f job/ollama-pull-models
```

> **모델을 바꾸려면 Job 이름도 바꾸세요.** 완료된 Job 은 `args` 만 고쳐 재적용할 수 없습니다. 지우고 다시 만들어야 합니다.
>
> ```bash
> kubectl -n <네임스페이스> delete job ollama-pull-models && kubectl apply -f ollama-k8s.yaml
> ```

---

## 4. 검증

`<주소>` 는 NodePort 나 `port-forward` 로 뚫은 곳입니다.

```bash
kubectl -n <네임스페이스> port-forward svc/ollama 11434:11434
```

### 4.1 서버가 떴는가

```powershell
(Invoke-WebRequest http://<주소>/api/version).Content
```

> **실측 (2026-09-04 · 사내 클러스터 NodePort)**
> ```
> {"version":"0.33.2"}
> ```

> **`https` 가 아니라 `http` 입니다.** 올라마는 평문 HTTP 로만 서비스합니다. NodePort 를 `https://` 로 부르면 이렇게 됩니다.
>
> ```
> The SSL connection could not be established
> ```
>
> `.env` 의 `OLLAMA_BASE_URL` 에도 **`http://`** 로 적으세요. TLS 가 필요하면 앞단에 인그레스를 두는 쪽입니다.

### 4.2 스토리지에 쓸 수 있는가 — **가장 잘 막히는 곳**

NFS 스토리지를 쓴다면 여기가 관건입니다. 올라마 이미지는 **root(uid 0)로 돌고** `/root/.ollama` 에 씁니다. 익스포트에 `root_squash` 가 걸려 있으면 root 가 `nobody` 로 매핑돼 **쓰기가 실패**합니다.

작은 모델로 먼저 확인하면 대역폭을 아낍니다.

```powershell
$body = @{ model = 'all-minilm'; stream = $false } | ConvertTo-Json
Invoke-RestMethod http://<주소>/api/pull -Method Post -Body $body -ContentType 'application/json'
```

> **실측 (2026-09-04 · NFS `nfsvers=3,nolock`)** — 43.8MB 모델 pull **10.6초 성공**. `root_squash` 문제 없었습니다.

### 4.3 추론이 되는가

```powershell
$body = @{ model = 'all-minilm'; input = '테스트' } | ConvertTo-Json
(Invoke-RestMethod http://<주소>/api/embed -Method Post -Body $body -ContentType 'application/json').embeddings[0].Count
```

> **실측** — 384차원 반환. **콜드 0.79초 / 웜 0.07초**

### 4.4 적재 상태와 만료

```powershell
(Invoke-RestMethod http://<주소>/api/ps).models
```

`expires_at` 이 `OLLAMA_KEEP_ALIVE` 만큼 뒤로 찍혀 있으면 설정이 먹은 것입니다. `-1` 이면 **수년 뒤**로 찍힙니다.

> **실측 (2026-09-04 · 두 모델 동시 적재 · ctx 4096)**
>
> | 모델 | 점유 |
> | :--- | ---: |
> | `qwen3.5:2b` | 2.20 GB |
> | `bge-m3` | 1.14 GB |
> | **합계** | **3.33 GB** |
>
> `limits: 8Gi` 안에 넉넉히 들어갑니다. **`OLLAMA_MAX_LOADED_MODELS=2` 도 동작해** 둘이 서로를 밀어내지 않습니다.

### 4.5 NFS 에서는 `KEEP_ALIVE` 판단이 달라집니다

**이것이 로컬 설치와 갈리는 가장 큰 지점입니다.**

> **실측 (2026-09-04)** — 같은 모델을 두 번 재봤습니다.
>
> | | 콜드 | 웜 | 재적재 비용 |
> | :--- | ---: | ---: | ---: |
> | 로컬 SSD | 5.55초 | 2.15초 | **3.4초** |
> | **클러스터 (NFS)** | 13.22 / 10.44초 | 0.43 / 0.58초 | **9.9 ~ 12.8초** |
>
> `bge-m3` 콜드도 6.6초입니다.

**NFS 는 재적재가 3~4배 비쌉니다.** `5m` 으로 두면 5분 넘게 쉴 때마다 첫 응답이 10초 이상 늦습니다.

그런데 **두 모델을 다 올려도 3.33GB** 라 `requests: 5Gi` 안에 들어갑니다 — **`-1` 로 두어도 이미 예약해 둔 양을 넘지 않습니다.**

```yaml
            - name: OLLAMA_KEEP_ALIVE
              value: "-1"
```

| 상황 | 값 |
| :--- | :--- |
| **전용 파드** | **`-1`** — 매니페스트의 기본값 |
| 노드를 다른 워크로드와 나눠 씀 | `5m` — 안 쓸 때 램을 돌려줍니다 |

> 로컬 설치는 이야기가 다릅니다. 재적재가 3.4초로 싸고 노트북 램은 아껴야 하므로 **기본값(`5m`)이 낫습니다.**

---

## 5. 파이썬에서 붙기

`SETUP.md` §4.3 과 같습니다. **주소만 바꾸면 됩니다.**

```ini
OLLAMA_BASE_URL=http://<주소>
OLLAMA_MODEL=qwen3.5:2b
OLLAMA_EMBED_MODEL=bge-m3
```

검사 스크립트도 그대로 씁니다.

```powershell
python ch04_dev-env\check_ollama.py
```

`method` 가 모델마다 다르다는 것, `reasoning=False` 가 필요하다는 것은 **서버가 어디 있든 같습니다** — [SETUP.md](SETUP.md) §4.5.

---

## 6. 막혔을 때

| 증상 | 원인 | 확인 |
| :--- | :--- | :--- |
| `412 requires a newer version` | **이미지가 모델보다 낮음** | `ollama show <모델>` 의 `requires` (§2) |
| `SSL connection could not be established` | `https` 로 붙음 | `http://` 로 (§4.1) |
| 파드는 Ready 인데 붙을 수 없음 | `OLLAMA_HOST` 미설정 | 기본값이 `127.0.0.1` 입니다 |
| PVC 가 `Pending` | `WaitForFirstConsumer` | 파드까지 배포하면 풀립니다 (§3) |
| pull 에서 permission denied | NFS `root_squash` | §4.2 의 작은 모델 테스트 |
| 파드가 `OOMKilled` | `limits.memory` 부족 | 모델 2개 실측 3.33GB(ctx 4096). 컨텍스트를 키웠는지 `/api/ps` 로 확인 |
| 새 파드가 `Pending` | RWO 볼륨 경합 | `strategy: Recreate` 인지 확인 |

---

## 7. 검증 범위

**2026-09-04 사내 클러스터에서 실제로 돌려 확인한 것.**

| 항목 | 결과 |
| :--- | :--- |
| 서버 기동 · NodePort 도달 | ✅ `{"version":"0.33.2"}` |
| PVC 쓰기 (NFS) | ✅ `root_squash` 문제 없음 |
| 모델 pull | ✅ 3개 · 3.67GB (`qwen3.5:2b` 2.55 · `bge-m3` 1.08 · `all-minilm` 0.04) |
| **20Gi PVC** | ✅ 3.67GB 사용 — 충분 |
| **두 모델 동시 적재** | ✅ **3.33GB** — `limits: 8Gi` 안 |
| `MAX_LOADED_MODELS=2` | ✅ 서로 안 밀어냄 |
| **NFS 콜드 스타트** | ✅ **9.9 ~ 12.8초** (§4.5) |
| `KEEP_ALIVE=-1` | ✅ 만료가 무기한으로 찍힘 |
| 추론 (생성 · 임베딩) | ✅ 임베딩 1024차원 |

### 아직 안 해 본 것

- **GPU 구성** — 매니페스트 주석에만 있고 돌려 본 적 없습니다
- **컨텍스트를 키웠을 때의 메모리** — 위 3.33GB 는 `ctx=4096` 기준입니다. 32k 로 올리면 늘어납니다(로컬 실측으로는 모델당 +0.4GB)
- **`NUM_PARALLEL=2` 의 실제 부담** — 동시 요청을 두 개 넣어 본 적이 없습니다
- **파드 재시작·롤아웃 중 동작** — `Recreate` 전략이 의도대로 도는지

---

[⬅ Chapter 04](README.md) · [SETUP.md 로 돌아가기](SETUP.md) · [윈도우에 설치는 ollama-windows.md](ollama-windows.md)
