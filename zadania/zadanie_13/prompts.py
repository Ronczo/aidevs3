SQL_PROMPT = """
You are developer with perfect SQL skills. Below you can find 4 sql queries.
Your task is to generate sql query that will give me information about datacenters with their managers. Try to include as much information as possible.
I need only SQL query, dont write anything else. Output must be a simple string
{sql_queries}
"""


NOTE_PROMPT = """
Poniżej znajdziesz listę słowników python z informacjami o datacenter.
Twoim zadaniem jest przefiltrowanie ich tak, aby zwrócić ID tych, które odopowiadają na poniższe pytanie

{question}

Jako output potrzebuję jedynie ID datacenterów, które spełniają warunek. Podaj je w formie listy.
Podaj jedynie liste, nic innego nie pisz

Słowniki: {datacenters}
"""
