from dialog_graph import nodes


if __name__ == "__main__":
    countdown = nodes.SequenceNode([
        nodes.WaitForEnterNode(f"Blast off in {i}")
        for i in range(10, 0, -1)
    ])
    countdown.run("")
