BARBARA_PROMPT = """
Read the note below. Analyze it and write down all people and all places you found. I dont need surnames, only names.
Places and names are Polish. You need to adjust them to basic form. For example: 'Warszawie' -> 'Warszawa'. Dont use polish diacritics.
note: {note}

as result I need python dictionary with keys 'people' and 'places' and values as list of strings.
I need only dict, dont write anything else. Don't use \'\'\'python or any other code blocks.
"""

ANSWER_PROMPT = """
Barbara była widziana w tych miastach: {cities}. W którym z nich jest teraz?
Miej na uwadzę te notatkę: {note}

Podaj jedynie nazwe miasta.
"""