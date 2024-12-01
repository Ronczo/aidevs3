GETTING_URLS_PROMPT = """
Below you can find some text. Read it and check if there are any links to the images.
Urls ends with .PNG> But there might be given host and file names. Then join it and return me the full url.

As result I need string with urls separated by comma. Just give me that string, dont write anyrhing else
If you can't find the host, use this path: https://centrala.ag3nts.org/dane/barbara/
The note: {note}
"""


REPAIR_CHOOSING_PROMPT = """
I am sending the picture. It's probably a little broken. Check the image and tell me what can I fix this.
I can REPAIR it if there are noises in the picture.
I can DARKEN the image if it's too bright.
I can BRIGHTEN the image if it's too dark.

Please choose one of the options above. As result I need one of the following words: REPAIR, DARKEN, BRIGHTEN, OK.
Do not write anything else except one of the words above.
If you think that picture is OK, just write OK.
"""

CORRECT_URL_PROMPT_SYSTEM = """
You are helpful assistant. I want you to describe the woman on the following pictures.
As result I need the description of the woman in Polish language!
"""
CORRECT_URL_PROMPT = """
I am attaching the picture. If there is a woman in the picture, try to remember her face.
use this picture to describe her. I just need her special signs, liek hair color, eyes color, etc. Maybe she wears something special?
Your answer must be in Polish language. Focus on details, maybe some tattoos?
"""
