import base64

from clients.openai import OpenAIClient
import os

open_ai = OpenAIClient(model="gpt-4o")

map_directory = "mapy/"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


map_messages = []

for idx, map_file in enumerate(os.listdir(map_directory), start=1):
    file = os.path.join(map_directory, map_file)
    encoded_image = encode_image(file)
    image_url = f"data:image/jpeg;base64,{encoded_image}"
    message = open_ai.prepare_message_with_image_url(image_url, f"Map {idx}")
    map_messages.append(message)

prompt = """
I sent you image with 4 maps. Three of them are from the same city, one is from different city.
Using your own knowledge and these maps, can you tell me what city is this?
What I know about this city is that there used to be the Granaries and the Stronghold
"""

msg = open_ai.prepare_message(prompt)
messages = [*map_messages, msg]
response = open_ai.chat(messages)
result = open_ai.get_content(response)
print(result)
