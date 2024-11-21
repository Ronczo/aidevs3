#
#
#
#
# FACTS_PROMPT = """
# Below you can find some note. Get familiar with the content. Generate tags, which describes the content of the note.
# As result i Need python dict with name of name and surname of person as key, and tags as values:
#
# <example>
#
#     "Jan Kowalski": ["tag1", "tag2", "tag3", "tagN],
#
#
# Fact: {note}
# """
#
# NOTES_PROMPT = """
# Bellow you can find a note from the file. get familiar with the content and using context (check the facts) and the content generate list of tags, which describe the content of the note. Remember to generate tags for every note you have received.
#
# Note file name: {file_name}
# Note content: {note}
# """
#
# NOTES_2_PROMPT = """
# Below you can find a note. Get familiar with the content. Analyze the content and generate tags. Check previous message, if you want something in common, add all tags from that message, which fits to this note.
# People and their professions also can be tags
#
# <example>
# ["tag1", "tag2", "tag3", "tagN]
# </example>.
#
# Note content: {note}
#
# """
#
#
SYSTEM_PROMPT = """
You are helpful assistant.
Your task is to generate tags describing note you will received. The tags should be separated by commas.
Tags must be in Polish in noun. Remember that Polish language has different forms of nouns depending on the context. For example, for the word "kot" you should provide "kot" and for "kota" shoule be also "kot". Tag cant in plurar


As output I need only string with tags separated by commas.
"""
#
# GENERAL_PROMPT_A = """
# You will receive some information in notes. Your task is to generate tags for note.
# Try to generate tags as many as possible. When you analyze the note, check also previous messages and invlude it in generating tags.
# """
#
# GENERAL_PROMPT = """
# Generate tags for the note. Remember to include tags from previous messages if they fit to the note.
# """
#


NOTES_PROMPT = """
Here is content of the note. Analyze this note and generate tags.
The note: {note}


First analyze the note and additional info, then generate the tags

I am adding also file name. Generate tags from file name too
File name: {file_name}
"""


NOTES_PROMPT_3 = """
Here is content of the note. Analyze this note. 
The note: {note}

In the past I sent you some facts. Check if any of them is related with the note. If it is, include it in generating tags process.

"""

FACTS_PROMPT = """
Below you can find some facts. Analyze the content and keep it in mind

Fact: {fact}
"""
