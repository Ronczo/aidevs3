import requests

from settings import ELEVEN_LABS_API_KEY


class ElevenLabsClient:
    CHUNK_SIZE = 1024

    def __init__(self):
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        self.voices_url = "https://api.elevenlabs.io/v1/voices"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_LABS_API_KEY,
        }

    def text_to_speech(
        self,
        text: str,
        voice_id: str = "CwhRBWXzGAHq8TQ4Fs17",  # Aria
        language: str = "pl",
        stability: float = 0.5,
        similarity_boost: float = 0.5,
    ):
        data = {
            "model_id": "eleven_turbo_v2_5",  # Supports Polish
            "text": text,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
            },
            "language_code": language,
        }

        response = requests.post(
            self.base_url.format(voice_id=voice_id), json=data, headers=self.headers
        )
        if response.status_code == 200:
            with open("output.mp3", "wb") as f:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
