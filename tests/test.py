from opennote import OpennoteVideoClient
import os
from dotenv import load_dotenv

load_dotenv(".env")

client = OpennoteVideoClient(api_key=os.getenv("OPENNOTE_API_KEY"))

client.video.make(
    sections=5,
    model="feynman2",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
)
