from typing import Dict, List, Optional

import pydantic


class Poll(pydantic.BaseModel):
    id: int
    question: str
    choices: List[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "question": "What is your favorite color?",
                "choices": ["Red", "Green", "Blue"],
            }
        }


class PollCreate(pydantic.BaseModel):
    question: str
    choices: List[str]

    class Config:
        schema_extra = {
            "example": {
                "question": "What is your favorite color?",
                "choices": ["Red", "Green", "Blue"],
            }
        }


class PollUpdate(pydantic.BaseModel):
    question: Optional[str] = None
    choices: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "question": "What is your least favorite color?"
            }
        }


class VoteCreate(pydantic.BaseModel):
    choice: int | str

    class Config:
        schema_extra = {
            "example": {
                "choice": "Red",
            }
        }


class Vote(pydantic.BaseModel):
    id: int
    poll_id: int
    choice: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "poll_id": 1,
                "choice": 1,
            }
        }


class Result(pydantic.BaseModel):
    poll_id: int
    results: Dict[str, int]
    outcome: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "poll_id": 1,
                "results": {"Red": 2, "Green": 0, "Blue": 1},
                "outcome": "The winner is Red",
            }
        }
