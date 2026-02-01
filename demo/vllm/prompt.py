from abc import ABC, abstractmethod


class Prompt(ABC):
    @abstractmethod
    def format(self) -> str:
        pass

    def parse(self, response: str):
        return response


class ConstantPrompt(Prompt):
    def __init__(self, prompt: str):
        self.prompt = prompt

    def format(self) -> str:
        return self.prompt
