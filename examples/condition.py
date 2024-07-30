from dialog_graph import nodes


if __name__ == "__main__":
    node = nodes.FallbackNode([
        nodes.SequenceNode([
            nodes.FreeInputNode("Pick a number from 1 to 10."),
            nodes.ConditionNode(lambda in_text: int(in_text) < 5),
            nodes.WaitForEnterNode("Number is less than 5."),
        ]),
        nodes.WaitForEnterNode("Number is greater than or equal to 5."),
    ])
    node.run("")
