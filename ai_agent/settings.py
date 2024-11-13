from dotenv import load_dotenv
import os

load_dotenv()

# ENV VARS
# General
AGENT_KEY = os.getenv("AGENT_KEY")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
# OpenAI
API_KEY = os.getenv("OPENAI_API_KEY")
# Langfuse

LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

