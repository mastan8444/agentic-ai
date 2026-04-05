🚀 AI-Powered PPT Generator (Agentic AI + MCP)

An intelligent Agentic AI-based PowerPoint Generator that creates structured, well-designed presentations from user prompts.
This project leverages AI agents, MCP servers, and automation tools to generate slides dynamically with content, formatting, and visuals.

📌 Project Overview

This project demonstrates how Agentic AI systems can automate real-world tasks like presentation creation.

👉 Instead of manually designing slides, users simply:

Enter a topic
The AI agent generates:
Structured content
Slide-wise breakdown
PowerPoint file (.pptx)

Agentic AI systems are designed to autonomously plan, reason, and execute tasks, making them ideal for workflow automation

✨ Features
🧠 Prompt → PPT generation
📑 Automatic slide structuring
🎯 Bullet-point content (not paragraphs)
🖼️ Image integration support
📂 Download generated PPT files
⚡ FastAPI-based backend
🔗 MCP (Model Context Protocol) integration
🤖 Multi-agent workflow execution
🏗️ Project Structure
auto_ppt_agent/
│
├── app.py                # Main backend (API)
├── app_ui.py             # UI interface
├── mcp_client.py         # MCP client connection
├── test_llm.py           # LLM testing
├── requirements.txt      # Dependencies
│
├── agent/                # Agent logic
├── tools/                # PPT generation tools
├── mcp_servers/          # MCP server implementations
│
├── output/               # Generated PPT files
├── generated_images/     # Images used in slides
│
└── .env                  # Environment variables
⚙️ Tech Stack
Backend: FastAPI
AI/LLM: OpenAI / LLM APIs
Architecture: Agentic AI
Protocol: MCP (Model Context Protocol)
Language: Python
Libraries:
python-pptx
requests
dotenv
🚀 How It Works
User provides a topic
Agent analyzes the prompt
Breaks it into slide-wise content
Generates bullet points
Creates PPT using python-pptx
Saves and returns downloadable file
🛠️ Installation
1️⃣ Clone the repository
git clone https://github.com/mastan8444/agentic-ai.git
cd agentic-ai
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Setup environment variables

Create .env file:

OPENAI_API_KEY=your_api_key_here
▶️ Run the Project
python app.py

or (if using FastAPI):

uvicorn app:app --reload
📸 Example Use Case

Input:

AI in Education

Output:

Slide 1: Title
Slide 2: Introduction
Slide 3: Applications
Slide 4: Benefits
Slide 5: Challenges
Slide 6: Future Scope

👉 Download ready-to-use PPT 🎉

🎯 Future Enhancements
🌐 Web frontend (React UI)
🎨 Canva-like slide design
📊 Charts & graphs integration
🗣️ Voice input support
☁️ Cloud deployment
🤝 Contributing

Contributions are welcome!

Fork the repo
Create a branch
Submit a PR
📄 License

This project is open-source and available under the MIT License

👨‍💻 Author

Shaik Mastan
💡 Passionate about Data Science & AI
🚀 Building Agentic AI Projects

⭐ Support

If you like this project:
👉 Give it a ⭐ on GitHub

💡 Summary

This project showcases how Agentic AI + MCP + LLMs can automate complex workflows like presentation generation, highlighting the future of AI-driven productivity tools.
