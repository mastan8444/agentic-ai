from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("SearchServer")

@mcp.tool()
def search_web(query: str) -> str:
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        res = requests.get(url).json()

        # extract useful info
        abstract = res.get("Abstract", "")
        related = res.get("RelatedTopics", [])

        text_data = abstract

        # add related info
        for r in related[:3]:
            if isinstance(r, dict) and "Text" in r:
                text_data += "\n" + r["Text"]

        if not text_data:
            return "No data found"

        return text_data

    except Exception as e:
        return f"Search error: {str(e)}"


if __name__ == "__main__":
    mcp.run()