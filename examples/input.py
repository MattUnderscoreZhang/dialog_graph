from dialog_graph import nodes


if __name__ == "__main__":
    node = nodes.SequenceNode([
        nodes.FreeInputNode("What is your name?"),
        nodes.WaitForEnterNode("Hi {{in_text}}!"),
    ])
    node.run("")
