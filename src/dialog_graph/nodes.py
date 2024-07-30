from abc import abstractmethod
from dataclasses import dataclass
from dotenv import load_dotenv
from gpt_interface import GptInterface
import jinja2
import os
from typing import Callable, cast


@dataclass
class Result:
    success: bool
    out_text: str


class Node:
    @abstractmethod
    def run(self, in_text: str) -> Result:
        ...


class WaitForEnterNode(Node):
    def __init__(self, display_text: str):
        self.display_text = display_text
        self.jinja_environment = jinja2.Environment()

    def run(self, in_text: str) -> Result:
        template = self.jinja_environment.from_string(self.display_text)
        display_text = template.render(in_text=in_text)
        print(display_text, "\n\n[Press Enter]")
        input()
        return Result(success=True, out_text="")


class FreeInputNode(Node):
    def __init__(self, display_text: str):
        self.display_text = display_text

    def run(self, in_text: str) -> Result:
        print(self.display_text, "\n")
        response = input()
        print()
        return Result(success=True, out_text=response)


class SequenceNode(Node):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def run(self, in_text: str) -> Result:
        result = Result(success=True, out_text=in_text)
        for node in self.nodes:
            result = node.run(result.out_text)
            if not result.success:
                return result
        return result or Result(success=True, out_text="")


class FallbackNode(Node):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def run(self, in_text: str) -> Result:
        result = Result(success=True, out_text=in_text)
        for node in self.nodes:
            result = node.run(result.out_text)
            if result.success:
                return result
        return result or Result(success=False, out_text="")


class ConditionNode(Node):
    def __init__(self, condition: Callable[[str], bool]):
        self.condition = condition

    def run(self, in_text: str) -> Result:
        return Result(success=self.condition(in_text), out_text=in_text)


class LLMNode(Node):
    def __init__(self, gpt_model: str, query: str):
        self.gpt_model = gpt_model
        self.query = query
        self.jinja_environment = jinja2.Environment()
        load_dotenv()

    def run(self, in_text: str) -> Result:
        try:
            interface = GptInterface(
                api_key=cast(str, os.getenv("OPENAI_API_KEY")),
                model=self.gpt_model,
            )
            template = self.jinja_environment.from_string(self.query)
            query = template.render(in_text=in_text)
            response = interface.say(query)
            return Result(success=True, out_text=response)
        except Exception as e:
            return Result(success=False, out_text=str(e))


class RetryNode(Node):
    def __init__(self, node: Node, max_retries: int):
        self.node = node
        self.max_retries = max_retries

    def run(self, in_text: str) -> Result:
        result = Result(success=True, out_text=in_text)
        for _ in range(self.max_retries):
            result = self.node.run(result.out_text)
            if result.success:
                return result
        return result or Result(success=False, out_text="")
