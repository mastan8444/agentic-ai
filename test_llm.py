from agent.llm import ask_llm

print("🧠 Testing LLM...\n")

response = ask_llm("""
Create 4 bullet points about modern farming in India.
Each point must be meaningful and real.
""")

print("\n📌 OUTPUT:\n")
print(response)