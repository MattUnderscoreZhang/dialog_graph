from dialog_graph import nodes


class FailTwiceNode(nodes.Node):
    def __init__(self):
        self.fail_count = 0

    def run(self, in_text: str) -> nodes.Result:
        self.fail_count += 1
        return nodes.Result(success=self.fail_count > 2, out_text="")


if __name__ == "__main__":
    failure_node = nodes.SequenceNode([
        nodes.RetryNode(FailTwiceNode(), 3),
        nodes.WaitForEnterNode("Success for max 3 tries!"),
    ])
    failure_node.run("")

    failure_node = nodes.SequenceNode([
        nodes.RetryNode(FailTwiceNode(), 2),
        nodes.WaitForEnterNode("Success for max 2 tries!"),
    ])
    failure_node.run("")
