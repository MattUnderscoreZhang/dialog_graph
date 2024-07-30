from dialog_graph import nodes


game_state = {
    "inventory": ["bubble gum"],
    "locations": ["field", "weapons shop", "lint golem"],
}

intro_screen = WaitForEnterNode("""Welcome adventurer, to the magic land of Socklandia! This place is where all lost socks go, and can only be accessed by spinning around three times in your dryer. You are here in search of your favorite sock, but it is guarded by a fierce lint golem. Can you save your sock?

[Press Enter to continue]""")

field = FreeInputNode("""You are in a field. You see the lint golem to the north of you. To your south is a weapons shop. To the east and west are invisible walls because this is a tech demo.

What would you like to do?""")

check_action = LLMNode("""Which of the following actions is the player attempting to perform?

action_list = {
    "move": move, 
    "talk": talk, 
    "fight": fight, 
    "check inventory": inventory, 
    "other": other,
}""")

move
"""
x
"""

talk
"""
x
"""

fight
"""
x
"""

inventory
"""
Here is your inventory: {inventory}.
"""

other
"""
Respond humorously to the player's action as though you were a text adventure game. Some interesting action can occur in the game world, but it must not end up progressing the game or causing any real effect.
"""
