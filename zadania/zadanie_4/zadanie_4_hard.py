from client import OpenAIClient


client = OpenAIClient("gpt-4o")

preview_message = "You are going to play a maze game. You must follow the rules to get to the end of the maze."
system_message = """
<MAZE_MAP>
- Map looks like chess board, but it's smaller
- Map has 6 columns: A, B, C, D, E, F
- Map has 4 rows: 1, 2, 3, 4
- Map has start point at A4
- Map has end point at F4
- Map has walls at B1, B3, B4, D2, D3
</MAZE_MAP>
<RULES>
- You can only move UP, DOWN, LEFT, RIGHT.
- You can only move one step at a time.
- You cannot move outside the maze.
- You cannot move through walls.
- If you move on wall, you go back to previous position.
- When you go back to previous position, you need to sue command from previous position
ember that you cannot skip over any position. For example, you cannot move directly from A3 to C3 as there is an obstacle at B3. Always go step by step.
</RULES>
<OBJECTIVE>
- The objective of the game is to get to the end of the maze.
- You need to member command you used to get to the end of the maze.
</OBJECTIVE>
<THINK>
- Think before you move.
- If your command provides you with a wall, you need to think of another command.
- Moving back is always a bad idea
- Remember the command which didn't provide you with a wall
</THINK>
<EXAMPLE>
{
"steps": "UP, RIGHT, DOWN, LEFT"
}

</EXAMPLE>
"""


test = """
Robot znajduje się na mapie o wymiarze 6(poziomo) na 4 (pionowo) w punkcie (0,0) w lewym dolnym rogu, a cel w punkcie (5,0) czyli w prawym dolnym rogu. Zaplanuj trasę tak, aby omijać przeszkody, które znajdują się na polach: (1,0), (1,1), (1,3), (3,1), (3,2). Ostatni ruch ma prowadzić do celu.
wewnątrz taga <plans> zaplanuj trasę pamiętając każdy swój poprzedni ruch. Gdy już ułożysz trasę omijając przeszkody, wynik w formacie JSON umieść wewnątrz taga <RESULT>.
Przykładowy JSON z wynikiem: {"steps": "UP, RIGHT, RIGHT, DOWN"}
"""

messages = [
    {"role": "system", "content": preview_message},
    {"role": "system", "content": test},
    {"role": "user", "content": ""},
]

print(messages)
response = client.get_response(messages, max_tokens=900)
print(client.get_response_content(response))
