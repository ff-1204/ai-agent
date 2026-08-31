"""교재 예제가 실제로 쓰는 import 를 전부 시험합니다.

examples/ 아래 .py 에서 뽑아낸 import 목록이 기준입니다.
API 키는 필요 없습니다. import 와 그래프 컴파일만 확인합니다.
"""

import importlib
import sys

CASES = [
    # --- langchain v1 ---
    ("langchain.agents", ["create_agent", "AgentState"]),
    ("langchain.agents.middleware",
     ["before_model", "dynamic_prompt", "AgentState", "ModelRequest",
      "wrap_model_call", "ModelResponse"]),
    ("langchain.messages", ["AIMessage", "ToolMessage", "HumanMessage"]),
    ("langchain.tools", ["tool", "ToolRuntime"]),
    ("langchain_core.messages", ["AIMessage", "ToolMessage", "SystemMessage", "HumanMessage"]),
    ("langchain_core.prompts", ["ChatPromptTemplate", "MessagesPlaceholder"]),
    ("langchain_core.tools", ["tool", "create_retriever_tool"]),
    ("langchain_text_splitters", ["RecursiveCharacterTextSplitter"]),
    ("langchain_openai", ["ChatOpenAI", "OpenAIEmbeddings"]),
    ("langchain_chroma", ["Chroma"]),
    ("langchain_tavily", ["TavilySearch"]),
    ("langchain_community.document_loaders",
     ["PyPDFLoader", "Docx2txtLoader", "WebBaseLoader"]),

    # --- langgraph v1 ---
    ("langgraph.graph", ["StateGraph", "MessagesState", "START", "END"]),
    ("langgraph.graph.message", ["add_messages"]),
    ("langgraph.graph.state", ["CompiledStateGraph"]),
    ("langgraph.prebuilt", ["ToolNode", "tools_condition"]),
    ("langgraph.types", ["Command", "Send"]),
    ("langgraph.runtime", ["Runtime"]),
    ("langgraph.checkpoint.memory", ["InMemorySaver", "MemorySaver"]),
    ("langgraph.store.memory", ["InMemoryStore"]),

    # --- MCP 1.x  (v2 로 올리면 여기가 깨집니다) ---
    ("mcp", ["ClientSession", "StdioServerParameters"]),
    ("mcp.server.fastmcp", ["FastMCP"]),
    ("mcp.server.fastmcp.prompts", ["base"]),
    ("mcp.client.stdio", ["stdio_client"]),
    ("mcp.client.streamable_http", ["streamablehttp_client"]),
    ("langchain_mcp_adapters.client", ["MultiServerMCPClient"]),
    ("langchain_mcp_adapters.tools", ["load_mcp_tools"]),
    ("langchain_mcp_adapters.prompts", ["load_mcp_prompt"]),

    # --- a2a-sdk 0.3.x  (1.x 로 올리면 여기가 깨집니다) ---
    ("a2a.client", ["A2AClient", "A2ACardResolver"]),
    ("a2a.server.agent_execution", ["AgentExecutor", "RequestContext"]),
    ("a2a.server.apps", ["A2AStarletteApplication"]),
    ("a2a.server.events", ["EventQueue"]),
    ("a2a.server.request_handlers", ["DefaultRequestHandler"]),
    ("a2a.server.tasks", ["InMemoryTaskStore", "TaskUpdater"]),
    ("a2a.types", ["AgentCard", "AgentSkill", "AgentCapabilities", "TaskState",
                   "Part", "TextPart", "DataPart", "Message",
                   "MessageSendParams", "SendMessageRequest", "Artifact"]),
    ("a2a.utils", ["new_agent_text_message", "new_task"]),

    # --- 그 외 ---
    ("openai", ["AsyncOpenAI"]),
    ("supabase", ["create_client", "Client"]),
]

ok = bad = 0
failures = []

for mod_name, names in CASES:
    try:
        mod = importlib.import_module(mod_name)
    except Exception as exc:
        bad += 1
        failures.append(f"  X  import {mod_name}  ->  {type(exc).__name__}: {exc}")
        continue
    missing = [n for n in names if not hasattr(mod, n)]
    if missing:
        bad += 1
        failures.append(f"  X  {mod_name}  ->  없는 이름: {', '.join(missing)}")
    else:
        ok += 1

print(f"import 검사: 통과 {ok} / 실패 {bad}")
for line in failures:
    print(line)

# --- 그래프를 실제로 만들어 컴파일해 봅니다 (API 키 불필요) ---
try:
    from typing import Annotated, TypedDict
    from langgraph.graph import StateGraph, START, END
    from langgraph.graph.message import add_messages
    from langgraph.checkpoint.memory import InMemorySaver
    from langchain_core.messages import HumanMessage, AIMessage

    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def echo(state: State) -> dict:
        last = state["messages"][-1].content
        return {"messages": [AIMessage(content=f"받음: {last}")]}

    builder = StateGraph(State)
    builder.add_node("echo", echo)
    builder.add_edge(START, "echo")
    builder.add_edge("echo", END)
    graph = builder.compile(checkpointer=InMemorySaver())

    cfg = {"configurable": {"thread_id": "smoke-1"}}
    graph.invoke({"messages": [HumanMessage(content="첫 번째")]}, cfg)
    out = graph.invoke({"messages": [HumanMessage(content="두 번째")]}, cfg)

    print(f"\n그래프 컴파일·실행: 통과 (체크포인터에 메시지 {len(out['messages'])}개 누적)")
    for m in out["messages"]:
        print(f"  {type(m).__name__:<12} {m.content}")
except Exception as exc:
    bad += 1
    print(f"\n그래프 검사: 실패 -> {type(exc).__name__}: {exc}")

sys.exit(1 if bad else 0)
