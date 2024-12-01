from clients.neo4j import Neo4jClient
from settings import AGENT_KEY
import requests


neo_4j = Neo4jClient()

PEOPLE_API_URL = "https://centrala.ag3nts.org/people"
PLACES_API_URL = "https://centrala.ag3nts.org/places"
BARBARA_TXT_URL = "https://centrala.ag3nts.org/dane/barbara.txt"
API_URL = "https://centrala.ag3nts.org/apidb"

query = ""
BODY = {"task": "database", "apikey": AGENT_KEY, "query": query}
users_body = BODY.copy()
connections_body = BODY.copy()
users_body['query'] = "select * from users"
connections_body['query'] = "select * from connections"

users_response = requests.post(API_URL, json=users_body)
connections_response = requests.post(API_URL, json=connections_body)

# q = "MATCH (a:Agent {id: 97, username: 'Jolanta'}) RETURN a"
# w = neo_4j.query_data_response(q)
# print(w)

# for idx, person in enumerate(users_response.json()['reply'], start=1):
#     id_ = person['id']
#     username = person['username']
#     neo_query = f"CREATE (p{idx}:Agent {{id: {id_}, username: '{username}'}})"
#     print(neo_query)
#     neo_4j.query(neo_query)
#     print("DONE")


#
# for connection in connections_response.json()['reply']:
#     first_id = connection['user1_id']
#     second_id = connection['user2_id']
#     neo_query = f"MATCH (a1:Agent {{id: {first_id}}}), (a2:Agent {{id: {second_id}}}) CREATE (a1)-[:KNOWS]->(a2)"
#     neo_4j.query(neo_query)
#     print("DONE")


q = "MATCH (a:Agent {username: 'Rafał'}, b:Agent {username: 'Barbara'}) RETURN a, b"
q = "MATCH (a:Agent {username: 'Rafał'}), (b:Agent {username: 'Barbara'}) RETURN a, b"
q = "MATCH (a:Agent {username: 'Rafał'}), (b:Agent {username: 'Barbara'}), p = shortestPath((a)-[:KNOWS*]-(b)) RETURN p"
w = neo_4j.query_data_response(q)
names = []
for x in w:
    for z in x['p']:
        if isinstance(z, dict):
            names.append(z['username'])
print(names)
answer = ", ".join(names)
print(answer)


answer_data = {"task": "connections", "apikey": AGENT_KEY, "answer": answer}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
