from typing import Optional, List

from models.recipe import Recipe
from pydantic import BaseModel


class NewCooking(BaseModel):
    recipe_id: int
    servings: int | None = None


class Issue(BaseModel):
    description: str
    step: int
    solution: str


class Cooking(BaseModel):
    recipe: Recipe
    servings: Optional[int]

    current_step: int = 0
    issues: List[Issue] = []

    def get_step(self, step: int = None):
        if step is None:
            step = self.current_step
        return self.recipe.instructions[step]
