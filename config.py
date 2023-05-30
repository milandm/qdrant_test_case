import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
ROOT = Path(__file__).parent
DATA = ROOT / "data"
MAX_SENTENCE_LENGTH = 100

# Qdrant
QDRANT_PORT = 6333
    # os.getenv("QDRANT_HOST")
QDRANT_HOST = "e9ef9c6a-888b-4f78-a401-8d0833138b37.us-east-1-0.aws.cloud.qdrant.io"
    # os.getenv("QDRANT_PORT")
QDRANT_API_KEY = "oAD1bjm8THHnMSQo_zCBTAocA5m-mN4niawGQ0uylQQfXAzpmzSWLA"
    # os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "meditations-collection_4"

# VECTOR_PARAMS_SIZE = 384
# VECTOR_PARAMS_SIZE = 1536

# OpenAI
OPENAI_API_KEY = ""
    # os.getenv("OPENAI_API_KEY")
