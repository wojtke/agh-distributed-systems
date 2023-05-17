from typing import List

import openai
from config import settings
from models.cooking import Cooking

openai.api_key = settings.OPENAI_API_KEY


class ChatContext:
    def __init__(self, system_messages: List[dict]):
        self.system = system_messages
        self.messages = []

    def add_message(self, content, role="user"):
        self.messages.append({"role": role, "content": content})

    def get_last_messages(self, n):
        return self.messages[-n:]

    def get_openai_completion(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.system + self.messages,
            max_tokens=500,
            temperature=0.9
        )
        completion = response.choices[0].message.content
        self.add_message(completion, role="assistant")
        return completion


class OpenAIService:
    @staticmethod
    def get_dish_ideas(ingredients: List[str], query) -> List[dict]:
        pass

    @staticmethod
    def get_help(cooking: Cooking, issue: str) -> ChatContext:
        name = cooking.recipe.name
        step = cooking.get_step(cooking.current_step)

        chat = ChatContext([
            {
                "role": "system",
                "content": "You are a skilled chef. You are here to help me cook in case I have any problems. "
                           "I will ask you questions and you will respond with the correct answer."
            },
        ])

        chat.add_message(f"Hi! I am cooking '{name}' and I am having some issues with the step: '{step}'.\n {issue}")

        return chat.get_openai_completion()
