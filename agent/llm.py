from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    model_id = os.getenv("MODEL_ID", "google/flan-t5-large")
    token = os.getenv("HF_TOKEN")

    base_llm = HuggingFaceEndpoint(
        repo_id=model_id,
        huggingfacehub_api_token=token,
        max_new_tokens=int(os.getenv("MAX_TOKENS", 512)),
        temperature=float(os.getenv("TEMPERATURE", 0.3)),
    )

    # 🔥 Detect chat models automatically
    if any(x in model_id.lower() for x in ["qwen", "mistral", "chat", "instruct"]):
        return ChatHuggingFace(llm=base_llm)

    return base_llm


def ask_llm(prompt: str) -> str:
    try:
        llm = get_llm()

        response = llm.invoke(prompt)

        # 🔥 Handle both response types
        if hasattr(response, "content"):   # chat response
            return response.content

        return str(response)

    except Exception as e:
        print("❌ LLM Error:", str(e))
        return fallback()


def fallback():
    return """- Concept explained clearly
- Key features highlighted
- Applications discussed
- Future scope described"""