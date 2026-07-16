"""
Central configuration. Reads from environment / .env file.

You generally DON'T need to edit this file — but you will READ from it a lot.
Your RAG code should pull values from `settings` (e.g. settings.chunk_size)
instead of hard-coding numbers. That's what makes the app tunable from .env.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"

    # Storage
    chroma_dir: str = "./chroma_db"
    data_dir: str = "./data"

    # RAG knobs — used by the code you'll write
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_k: int = 4

    # Agent knobs
    agent_max_steps: int = 6      # cap the agent loop so it can't run forever
    mcp_enabled: bool = False     # turn on to load tools from an MCP server


settings = Settings()
