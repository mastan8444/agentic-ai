import requests
from tools import ppt_tools

class MCPClient:
    def __init__(self):
        self.prs = None

    def call_tool(self, name, *args):

        if name == "create_ppt":
            self.prs = ppt_tools.create_presentation(*args)
            return "PPT Created"

        elif name == "add_slide":
            ppt_tools.add_slide(self.prs, args[0], args[1])
            return "Slide Added"

        elif name == "add_chart":
            ppt_tools.add_chart_slide(self.prs, args[0])
            return "Chart Added"

        elif name == "save_ppt":
            return ppt_tools.save_presentation(self.prs, args[0])

        # 🌐 NEW TOOL
        elif name == "search_web":
            try:
                url = f"https://api.duckduckgo.com/?q={args[0]}&format=json"
                res = requests.get(url).json()
                return res.get("AbstractText", "No data found")
            except:
                return "Search failed"