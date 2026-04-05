from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("SearchServer")

@mcp.tool()
def search_topic(query: str):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    data = requests.get(url).json()
    return data.get("Abstract", "No data found")

if __name__ == "__main__":
    mcp.run()
