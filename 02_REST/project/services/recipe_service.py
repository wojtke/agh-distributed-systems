from typing import List

import requests
from config import settings
from models.ingredient import Ingredient
from models.recipe import Recipe, ShortRecipe

URL_ENDPOINT = "https://api.spoonacular.com/"


class SpoonacularAPIService:
    @staticmethod
    async def get_recipes(ingredients: List[Ingredient], number: int = 10) -> List[ShortRecipe]:
        res = requests.get(
            URL_ENDPOINT + "recipes/findByIngredients",
            params={
                "ingredients": ",".join([ingredient.name for ingredient in ingredients]),
                "number": number,
                "ranking": 1,
                "ignorePantry": True
            },
            headers={
                "x-api-key": settings.SPOONACULAR_API_KEY
            }
        )

        return [ShortRecipe.from_spoonacular(recipe) for recipe in res.json()]

    @staticmethod
    async def get_full_recipe_bulk(recipe_ids: List[int]) -> List[Recipe]:
        res = requests.get(
            URL_ENDPOINT + "recipes/informationBulk",
            params={
                "ids": ",".join([str(recipe_id) for recipe_id in recipe_ids]),
                "includeNutrition": True
            },
            headers={
                "x-api-key": settings.SPOONACULAR_API_KEY
            }
        )

        return [Recipe.from_spoonacular(recipe) for recipe in res.json()]

    @staticmethod
    async def get_full_recipe(recipe_id: int) -> Recipe:
        res = requests.get(
            URL_ENDPOINT + f"recipes/{recipe_id}/information",
            params={
                "includeNutrition": True
            },
            headers={
                "x-api-key": settings.SPOONACULAR_API_KEY
            }
        )

        return Recipe.from_spoonacular(res.json())
