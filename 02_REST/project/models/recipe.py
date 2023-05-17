from typing import List

from models.ingredient import Ingredient
from pydantic import BaseModel


class ShortRecipe(BaseModel):
    id: int
    name: str
    image_url: str

    @classmethod
    def from_spoonacular(cls, recipe: dict):
        return cls(
            id=recipe["id"],
            name=recipe["title"],
            image_url=recipe["image"]
        )


class Recipe(BaseModel):
    id: int
    name: str
    image_url: str
    servings: int
    time_to_prepare: int
    ingredients: List[Ingredient]
    instructions: List[str]
    source_url: str

    calories_per_serving: float
    fat_per_serving: float
    protein_per_serving: float
    carbs_per_serving: float
    serving_weight_grams: float

    def short_description(self):
        return f"{self.name}"

    @classmethod
    def from_spoonacular(cls, recipe: dict):
        return cls(
            id=recipe["id"],
            name=recipe["title"],
            image_url=recipe["image"],
            servings=recipe["servings"],
            time_to_prepare=recipe["readyInMinutes"],
            ingredients=[Ingredient.from_spoonacular(ingredient) for ingredient in recipe["extendedIngredients"]],
            instructions=[step["step"] for step in recipe["analyzedInstructions"][0]["steps"]],
            source_url=recipe["sourceUrl"],
            calories_per_serving=recipe["nutrition"]["nutrients"][0]["amount"],
            fat_per_serving=recipe["nutrition"]["nutrients"][1]["amount"],
            protein_per_serving=recipe["nutrition"]["nutrients"][8]["amount"],
            carbs_per_serving=recipe["nutrition"]["nutrients"][3]["amount"],
            serving_weight_grams=recipe["nutrition"]["nutrients"][7]["amount"],
        )

    def change_servings(self, servings):
        servings = servings / self.servings
        self.servings *= servings
        self.calories_per_serving = self.calories_per_serving * servings
        self.fat_per_serving = self.fat_per_serving * servings
        self.protein_per_serving = self.protein_per_serving * servings
        self.carbs_per_serving = self.carbs_per_serving * servings
        self.serving_weight_grams = self.serving_weight_grams * servings
        for ingredient in self.ingredients:
            ingredient.amount = ingredient.amount * servings
        return self
