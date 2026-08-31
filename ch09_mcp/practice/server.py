"""9장 실습 - 나만의 MCP 서버.

실행: python server.py
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")


@mcp.tool()
def hello(name: str) -> str:
    """이름을 받아 인사말을 돌려줍니다."""
    return f"안녕하세요, {name}님!"


# TODO 나만의 도구 추가하기

if __name__ == "__main__":
    mcp.run(transport="stdio")
