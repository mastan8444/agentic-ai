from agent.llm import ask_llm
from mcp_client import MCPClient
from tools.ppt_tools import add_title_slide

client = MCPClient()


# 🧠 STEP 1: PLAN
def planner_agent(prompt):
    print("\n🧠 [PLAN] Generating slide structure...")

    response = ask_llm(f"""
You are a presentation planner.

Create EXACTLY 8 slide titles.

Topic: {prompt}

Rules:
- Each title must be specific
- Cover complete topic
- No generic words like Introduction

Return ONLY titles (one per line)
""")

    slides = [s.strip("- ").strip() for s in response.split("\n") if len(s.strip()) > 5]

    if len(slides) < 8:
        slides = [
            f"Overview of {prompt}",
            f"Key Concepts of {prompt}",
            f"Technology Used",
            f"Applications",
            f"Benefits",
            f"Challenges",
            f"Statistics and Data",
            f"Future Trends"
        ]

    return slides[:8]


# 🧠 STEP 2: THINK / REASON
def reasoning_agent(title, topic):
    thought = ask_llm(f"""
Think like an expert presenter.

Slide: {title}
Topic: {topic}

What should this slide include based on real-world data?
""")

    return thought[:500]  # Return a snippet of the thought


# ✍️ STEP 3: CONTENT (ACT PREPARATION)
def content_agent(title, topic):
    print("🌐 [ACT] Fetching real data from web...")

    web_data = client.call_tool("search_web", f"{title} {topic}")

    response = ask_llm(f"""
Create slide content using REAL data.

Topic: {topic}
Slide: {title}

Web Data:
{web_data}

Rules:
- 6 to 8 bullet points
- Use facts from web data
- Each starts with "-"
- No generic content
-Create slide content.
- Each under 12 words
- No paragraphs
- Each line starts with "-"
""")

    content = []
    for line in response.split("\n"):
        if line.startswith("-"):
            content.append(line.replace("-", "").strip())

    if len(content) < 4:
        content = [
            "Real-world data integrated into explanation",
            "Key insights derived from current information",
            "Applications supported by factual references",
            "Trends based on available data"
        ]

    return content[:8]


# 🎨 STEP 4: DECISION (DESIGN)
def decide_action(title):
    if any(x in title.lower() for x in ["data", "statistics", "growth"]):
        return "chart"
    return "slide"


# 🚀 MAIN AGENT LOOP (STRICT REACT)
def run_agent(user_prompt, theme="blue"):
    print("\n🚀 AUTO-PPT AGENT STARTED")

    # 🧠 PLAN
    plan = planner_agent(user_prompt)

    print("\n📊 Slide Plan:")
    for i, p in enumerate(plan):
        print(f"{i+1}. {p}")

    # ⚙️ ACT → create PPT
    print("\n⚙️ [ACT] Creating presentation file...")
    client.call_tool("create_ppt", theme)

    # 🎨 Title Slide
    add_title_slide(client.prs, user_prompt)

    # 🔁 LOOP (CORE OF AGENT)
    for i, title in enumerate(plan):

        print(f"\n==============================")
        print(f"🔄 Processing Slide {i+1}: {title}")

        # 🧠 REASON
        thought = reasoning_agent(title, user_prompt)
        print("🧠 Thought:", thought[:120])

        # ✍️ ACT (Generate Content)
        content = content_agent(title, user_prompt)

        # 🎨 DECIDE TOOL
        action = decide_action(title)
        print("⚙️ [ACT] Decided:", action)

        # ⚙️ ACT (CALL TOOL)
        if action == "chart":
            result = client.call_tool("add_chart", title)
        else:
            result = client.call_tool("add_slide", title, "\n".join(content))

        # 👀 OBSERVE
        print("👀 [OBSERVE]:", result)

    # 💾 FINAL STEP
    print("\n💾 [FINAL ACT] Saving presentation...")
    file_path = client.call_tool("save_ppt", user_prompt)

    print("\n✅ PPT CREATED SUCCESSFULLY")
    print("📁 File:", file_path)

    return file_path