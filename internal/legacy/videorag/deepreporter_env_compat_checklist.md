# Deep-Reporter 환경 구축 — 호환성 검증 체크리스트 & 버전 기록 (WorldMM 공유 venv 통합)

> 방향(사용자 결정): **WorldMM Docker 컨테이너의 공유 venv(`WorldMM/.venv`, uv)에 한 번에 호환되도록 구축**, **openai 업그레이드 허용**, 버전 기록.
> 방법: `uv pip install --dry-run` 해결 + 설치 메타데이터/제약 조사. **실제 설치/삭제/변경 없이 분석·검증만 수행**(2026-10-20).
> 대상 python = `WorldMM/.venv/bin/python` (Python 3.13.9).

---

## 0. 결론
**공유 venv 통합은 안전하게 가능.** dry-run 해결 성공, **순변경 = openai 2.29.0→2.54.0 교체 1건 + 신규 24개뿐**, torch/transformers/pydantic/numpy 등 **기존 핀 전부 불변**. 유일한 런타임 미검증 항목은 Risk B(langgraph/langchain 1.x API 1개 지점) → 설치 후 import/compile 테스트로 확정.

## 1. 확정 버전 세트 (Path UP = openai 업그레이드, 채택 방향)
`uv pip install langgraph langchain-core langchain-openai flask` 가 해결한 집합(C1):

**신규 설치(24)**
| 패키지 | 버전 | 비고 |
|---|---|---|
| langgraph | 1.2.16 | core |
| langchain-core | 1.6.12 | core |
| langchain-openai | 1.4.3 | core (최신 1.7.x는 certifi로 회피 — §3.4) |
| langchain-protocol | 0.0.19 | langchain-core 전이 |
| langgraph-checkpoint / -prebuilt / -sdk | 4.3.0 / 1.1.1 / 0.4.8 | langgraph 전이 |
| langsmith | 0.14.11 | langchain-core 전이 → httpx2 유발 |
| httpx2 / httpcore2 | 2.3.0 / 2.3.0 | **langsmith 전용**(별도 네임스페이스, §3.3) |
| flask / werkzeug / itsdangerous / blinker | 3.1.3 / 3.1.9 / 2.2.0 / 1.9.0 | 우리 [A] 서비스용 |
| orjson / ormsgpack / jsonpatch / jsonpointer | 3.13.0 / 1.13.0 / 1.36 / 3.4 | 경량 전이 |
| requests-toolbelt / truststore / uuid-utils / websockets / zstandard | 1.0.0 / 0.10.5 / 0.18.0 / 16.1.1 / 0.25.0 | 경량 전이 |

**업그레이드(1)**: `openai 2.29.0 → 2.54.0`
**제거/다운그레이드**: **없음**
**불변(유지)**: torch 2.8.0+cu128, transformers 4.57.6, pydantic 2.12.5, numpy 2.4.3, httpx 0.28.1, httpcore 1.x, tenacity 9.1.4, certifi 2022.12.7, typing-extensions 4.15.0, tiktoken 0.12.0, requests 2.28.1, pyyaml 6.0.3, jinja2 3.1.6, click 8.3.1, markupsafe 3.0.2

**대안 Path PIN(참고)**: `uv pip install "openai==2.29.0" langgraph langchain-core langchain-openai flask` → **uninstall 0건**, openai 불변, langchain-openai 1.3.4 선택(C4). openai를 전혀 안 건드리고 싶을 때의 더 보수적 선택지.

## 2. 왜 openai가 올라가나 / 꼭 필요한가
- langchain-openai(≥1.6.5)는 `openai>=2.45.0` 요구. 채택된 **langchain-openai 1.4.3**은 openai 2.29.0도 수용하지만, `uv pip install`이 의존 패키지를 최신으로 끌어올려 **openai를 2.54.0으로 업그레이드**(상한 핀 없음).
- 즉 **업그레이드는 "최신 선호"의 결과이지 필수는 아님**. openai를 고정하려면 Path PIN 사용.

## 3. 호환성 체크리스트 (검증 결과)
| # | 우려 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | 기존 패키지 다운그레이드/제거 | ✅ 없음(openai 교체만) | C1 전체 dry-run: "Would uninstall 1 package"=openai |
| 2 | openai 상한 핀 충돌 | ✅ 없음 | litellm `>=2.8.0`, transformers `>=1.98.0`, langchain-openai 1.4.3 모두 2.54.0 수용. 상한 핀 부재(C2) |
| 3 | httpx ↔ httpx2 충돌 | ✅ 없음 | httpx2는 **langsmith `httpx2>=2,<3`** 요구(C3). 별도 배포/모듈명 → 기존 httpx 0.28.1(openai/litellm/hf_hub용) 유지, 공존 |
| 4 | certifi 충돌 | ✅ 변경 없음 | 설치 certifi 2022.12.7. 최신 langchain-openai(1.7.x)는 `certifi>=2024.6.2` 요구 → resolver가 **회피하여 1.4.3 선택** → certifi 불변(C5). 상한 핀 부재 |
| 5 | torch/transformers/pydantic/numpy 영향 | ✅ 불변 | 추가 패키지들이 이들에 비의존, dry-run에서 변경 없음(C1) |
| 6 | Python 3.13 지원 | ✅ | langgraph/langchain 1.x는 3.13 지원 |
| 7 | **Risk B: Deep-Report(0.2/0.3-era 코드) ↔ langgraph/langchain 1.x** | ⚠️ 저위험, 런타임 확인 1건 | §4 |

## 4. Risk B — langgraph/langchain 1.x API 표면 분석 (C6/C7)
Deep-Report가 쓰는 API는 **작고 대부분 안정적**:
- langgraph: `from langgraph.graph import StateGraph, END`; `add_node/add_edge/add_conditional_edges/.compile()`; `from langgraph.config import get_stream_writer, RunnableConfig` → 1.x에서 안정 ✅
- langchain_core: `runnables.RunnableConfig`, `language_models.BaseChatModel`, `messages.{BaseMessage,AIMessage,HumanMessage,SystemMessage,ToolMessage,AIMessageChunk}`, `messages.ai.UsageMetadata`, `outputs.{ChatResult,ChatGeneration,ChatGenerationChunk}`, `callbacks.CallbackManagerForLLMRun` → 1.x에서 안정 ✅
- langchain_openai: `ChatOpenAI` ✅
- ⚠️ **유일한 황색 신호**: `graph.py:30 StateGraph(MultimodalLongFormState, config_schema=ConfigSchema)` — langgraph 1.x에서 `config_schema`가 deprecated/rename(→`context_schema`) 가능성. **import/compile 테스트로 확인 필요**(아래 §6-b). 깨지면 해당 인자만 소폭 수정 or langgraph 버전 핀다운으로 대응.

## 5. 설치 명령 (사용자 직접 실행 — 버전 기록 포함)
```bash
cd /data1/jyheo/workspace/VAU_RAG/WorldMM
# (1) 설치 전 스냅샷(복구용)
uv pip freeze > /data1/jyheo/workspace/VAU_RAG/claude_output/venv_before_deepreporter.lock.txt
# (2) 설치 (Path UP: openai 2.54.0 업그레이드 포함)
uv pip install langgraph langchain-core langchain-openai flask
# (3) 설치 후 버전 동결(기록)
uv pip freeze > /data1/jyheo/workspace/VAU_RAG/claude_output/venv_after_deepreporter.lock.txt
```
(보수적으로 openai 고정을 원하면 (2)를 `uv pip install "openai==2.29.0" langgraph langchain-core langchain-openai flask` 로 대체 = Path PIN)

## 6. 설치 후 필수 검증 (런타임)
```bash
cd /data1/jyheo/workspace/VAU_RAG/WorldMM
# (a) 버전 확인
python -c "import importlib.metadata as m; [print(p, m.version(p)) for p in ['langgraph','langchain-core','langchain-openai','openai','flask']]"
# (b) ★Risk B 확정: Deep-Reporter 그래프 import + compile
cd /data1/jyheo/workspace/VAU_RAG/Deep-Report
python -c "from deep_reporter.core.graph import MultimodalLongFormGraph; g=MultimodalLongFormGraph(); print('graph build OK')"
# (c) ★WorldMM 무손상 확인(openai 2.54.0 영향)
cd /data1/jyheo/workspace/VAU_RAG/WorldMM
python -c "from worldmm.memory.memory import WorldMemory; from worldmm.llm import LLMModel; print('WorldMM import OK')"
```
- (b) 통과 → Risk B 해소. `config_schema` 관련 에러 시 메시지 공유(인자 소폭 수정으로 대응).
- (c) 통과 → openai 업그레이드가 WorldMM에 무해 확정.

## 7. 요약
- **dry-run 기준 공유 venv 통합은 안전**(순변경 openai 1건 + 경량 24개, 기존 핀 불변).
- 유일한 미해결은 **런타임 Risk B 1지점**(`StateGraph(config_schema=...)`) → §6-b로 확정.
- 버전은 §1에 기록, 설치 시 §5-(1)/(3)로 lock 파일 2개 자동 기록.
