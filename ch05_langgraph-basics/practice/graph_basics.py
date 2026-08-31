"""5장 실습 - 랭그래프 기본 구성요소를 직접 조립해보는 공간."""
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph

load_dotenv()


class State(TypedDict):
    # TODO 5.2.1 상태 정의 / 5.2.2 리듀서 추가
    messages: list


def node(state: State) -> State:
    # TODO 5.2.3 노드 구현
    return state


builder = StateGraph(State)
builder.add_node("node", node)
builder.add_edge(START, "node")   # TODO 5.2.4 엣지 / 5.2.5 조건부 엣지
builder.add_edge("node", END)
graph = builder.compile()

if __name__ == "__main__":
    print(graph.invoke({"messages": []}))
