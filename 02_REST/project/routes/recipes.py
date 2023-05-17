from typing import List

from database import db_ingredients
from fastapi import APIRouter, Depends, HTTPException
from models.recipe import ShortRecipe
from routes.auth import User, get_current_active_user
from services.recipe_service import SpoonacularAPIService

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=List[ShortRecipe])
async def get_recipes(
        user: User = Depends(get_current_active_user),
):
    if user.id not in db_ingredients or len(db_ingredients[user.id]) == 0:
        raise HTTPException(status_code=400, detail="No ingredients - add some first")

    recipes = await SpoonacularAPIService.get_recipes(db_ingredients[user.id])
    return recipes


@router.get("/{recipe_id}")
async def get_recipe(
        recipe_id: int,
        user: User = Depends(get_current_active_user),
):
    recipe = await SpoonacularAPIService.get_full_recipe(recipe_id)
    return recipe
