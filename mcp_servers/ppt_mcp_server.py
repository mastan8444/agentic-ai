from mcp.server.fastmcp import FastMCP
from tools.ppt_tools import *

mcp = FastMCP("PPTServer")

@mcp.tool()
def create_ppt():
    return create_presentation()

@mcp.tool()
def add_slide_tool(prs, title, content):
    add_slide(prs, title, content)
    return "Slide Added"

@mcp.tool()
def save_ppt(prs, filename):
    return save_presentation(prs, filename)

if __name__ == "__main__":
    mcp.run()
