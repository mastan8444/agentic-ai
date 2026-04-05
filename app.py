from agent.agent_core import run_agent

if __name__ == "__main__":
    print("🚀 Auto PPT Agent Started")
    
    user_input = input("👉 Enter your PPT request:\n> ")
    
    print("\n⚙️ Generating presentation...\n")
    
    run_agent(user_input)
    
    print("\n✅ Done! Check the output folder.")