# 올라마를 쿠버네티스에 올리기

[SETUP.md](../SETUP.md) §4 가 요구하는 **서버 주소를 만드는 문서**입니다. 주소가 나오면 `.env` 에 적고 `SETUP.md` 로 돌아가면 됩니다.

매니페스트: [`k8s.yaml`](k8s.yaml) — PVC · Deployment · Service · 모델 pull Job
검증: 2026-09-04 사내 클러스터(NFS · NodePort)에서 전 과정 확인

---

## 배포

`namespace` 와 `storageClassName` 두 곳만 환경에 맞게 고칩니다.

```bash
kubectl apply -f k8s.yaml
kubectl -n <네임스페이스> rollout status deploy/ollama
kubectl -n <네임스페이스> logs -f job/ollama-pull-models    # 모델 받는 중
```

주소를 뚫습니다.

```bash
kubectl -n <네임스페이스> port-forward svc/ollama 11434:11434
```

확인되면 끝입니다.

```powershell
(Invoke-WebRequest http://<주소>/api/version).Content    # {"version":"0.33.2"}
```

---

## 걸리는 곳 넷

**① 이미지 태그가 모델보다 낮으면 pull 이 막힙니다.**

```
Error: pull model manifest: 412:
The model you are attempting to pull requires a newer version of Ollama.
```

요구 버전은 `ollama show <모델>` 의 `requires` 칸에 있습니다(`qwen3.5:2b` 는 0.17.1 이상). 매니페스트는 `0.33.2` 로 고정해 두었습니다. **`latest` 는 쓰지 마세요.**

**② `https` 로 붙으면 안 됩니다.** 올라마는 평문 HTTP 뿐입니다. TLS 가 필요하면 앞단에 인그레스를 두세요.

**③ `claimName` 에 StorageClass 이름을 넣으면 안 됩니다.** PVC 를 따로 만들고 그 이름을 넣습니다. StorageClass 는 PVC 의 `storageClassName` 에 들어갑니다.

**④ PVC 가 `Pending` 이어도 정상입니다.** `volumeBindingMode: WaitForFirstConsumer` 면 파드가 스케줄될 때까지 기다립니다.

---

## 로컬과 다른 점 둘

**NFS 는 모델 재적재가 3~4배 비쌉니다.**

| | 재적재 |
| :--- | ---: |
| 로컬 SSD | 3.4초 |
| 클러스터(NFS) | **9.9 ~ 12.8초** |

그래서 매니페스트는 `OLLAMA_KEEP_ALIVE=-1`(안 내림)로 두었습니다. 두 모델을 다 올려도 **3.33GB** 라 `requests: 5Gi` 안에 들어갑니다. 노드를 다른 워크로드와 나눠 쓴다면 `5m` 로 바꾸세요.

**로그가 프로브로 도배됩니다.** 요청 한 건당 한 줄이 찍히고 **끄는 방법이 없습니다** — `GIN_MODE` 는 무시되고([ollama#8682](https://github.com/ollama/ollama/issues/8682)), `OLLAMA_DEBUG=ERROR` 도 효과 없음을 확인했습니다. 프로브 주기를 늘려(30s/60s) 시간당 540 → 180건으로 줄여 두었고, 그래도 거슬리면 볼 때 거르세요.

```bash
kubectl -n <네임스페이스> logs -f deploy/ollama | grep -v '\[GIN\]'
```

---

## 아직 안 해 본 것

GPU 구성 · 컨텍스트를 32k 로 키웠을 때의 메모리 · `NUM_PARALLEL=2` 의 실제 부담.

---

[⬅ Chapter 04](../README.md) · [SETUP.md](../SETUP.md) · [윈도우에 설치](windows.md)
