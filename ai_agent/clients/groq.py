from groq import Groq
from settings import GROQ_API_KEY


class GroqClient:
    def __init__(self):
        self.client = Groq(
            api_key=GROQ_API_KEY,
        )

    def transcript_from_audio(self, file_name):
        with open(file_name, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(file_name, file.read()),
                model="whisper-large-v3-turbo",
                # prompt="Specify context or spelling",  # Optional
                # response_format="json",  # Optional
                # language="en",  # Optional
                # temperature=0.0  # Optional
            )
            return transcription.text
