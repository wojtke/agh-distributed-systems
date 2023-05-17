from typing import List

from database import db_ingredients
from fastapi import APIRouter, Depends, HTTPException
from models.ingredient import Ingredient
from routes.auth import User, get_current_active_user

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.post("/", response_model=Ingredient)
def add_ingredient(
        ingredient: Ingredient | str,
        user: User = Depends(get_current_active_user),
):
    if user.id not in db_ingredients:
        db_ingredients[user.id] = []

    if isinstance(ingredient, str):
        ingredient = Ingredient(name=ingredient)

    if ingredient in db_ingredients[user.id]:
        raise HTTPException(status_code=400, detail="Ingredient already on the list")
    db_ingredients[user.id].append(ingredient)

    return ingredient


@router.get("/", response_model=List[Ingredient])
def get_ingredients(
        user: User = Depends(get_current_active_user),
):
    if user.id not in db_ingredients:
        db_ingredients[user.id] = []
    return db_ingredients[user.id]


@router.delete("/")
def remove_ingredient(
        ingredient: Ingredient | str,
        user: User = Depends(get_current_active_user),
):
    if user.id not in db_ingredients:
        db_ingredients[user.id] = []

    if isinstance(ingredient, str):
        index = next((i for i, x in enumerate(db_ingredients[user.id]) if x.name == ingredient), None)
    else:
        index = next((i for i, x in enumerate(db_ingredients[user.id]) if x.name == ingredient.name), None)

    if index is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db_ingredients[user.id].pop(index)

    return {"message": "Ingredient removed"}


@router.delete("/")
def remove_all_ingredients(
        user: User = Depends(get_current_active_user),
):
    db_ingredients[user.id] = []

    return {"message": "All ingredients removed"}
