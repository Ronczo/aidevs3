from client import OpenAIClient


client = OpenAIClient("gpt-4o-mini")

system_message = """
<result>
- As result I want you to return me json with commands like in <example>
</result>
<example>
{
 "steps": "UP, RIGHT, DOWN, LEFT"
}
</example>
"""


messages = [
    {"role": "system", "content": system_message},
    {
        "role": "user",
        "content": "There are following commands: UP UP RIGHT RIGHT DOWN DOWN RIGHT RIGHT RIGHT. With given example give me the answer",
    },
]

print(messages)
# response = client.get_response(messages, max_tokens=500)
# print(client.get_response_content(response))
