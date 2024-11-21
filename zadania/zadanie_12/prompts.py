TAG_PROMPT = """
Read the text below and provide tags for it:
{content}
"""


TAG_SYSTEM_PROMPT = """
You are helpful assistant.
Your task is to generate tags describing note you will received. The tags should be separated by commas.
Tags must be in Polish in noun. Remember that Polish language has different forms of nouns depending on the context. For example, for the word "kot" you should provide "kot" and for "kota" shoule be also "kot". Tag cant in plurar


As output I need only string with tags separated by commas.
"""