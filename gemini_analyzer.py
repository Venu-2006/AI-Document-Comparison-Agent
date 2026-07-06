import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-20b"


def analyze_page(
    source_page,
    target_page
):

    # We'll implement the image support in the next step.

    return "Working"
