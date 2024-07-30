from dialog_graph import nodes


if __name__ == "__main__":
    node = nodes.FallbackNode([
        nodes.SequenceNode([
            nodes.FreeInputNode("Pick an animal."),
            nodes.LLMNode("gpt-4o", "State a fun fact about {{in_text}}."),
            nodes.WaitForEnterNode("{{in_text}}"),
        ]),
        nodes.WaitForEnterNode("ERROR: {{in_text}}"),
    ])
    node.run("")
