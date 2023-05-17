from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

from models import Poll, PollCreate, PollUpdate, Vote, Result, VoteCreate

app = FastAPI()
# POLLS

polls = {}
poll_votes = {}


@app.get("/polls", response_model=List[Poll])
async def get_polls():
    return list(polls.values())


@app.post("/polls", response_model=Poll)
async def create_poll(new_poll: PollCreate):
    poll = Poll(**new_poll.dict(), id=len(polls))
    polls[poll.id] = poll
    poll_votes[poll.id] = {}
    return poll


@app.get("/polls/{poll_id}", response_model=Poll)
async def get_poll(poll_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    return polls[poll_id]


@app.patch("/polls/{poll_id}", response_model=Poll)
async def update_poll(poll_id: int, poll_update: PollUpdate):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")

    if poll_votes[poll_id]:
        raise HTTPException(status_code=400, detail="Can't update poll with existing votes")

    poll = polls[poll_id]
    poll = poll.copy(update=poll_update.dict(exclude_unset=True))
    polls[poll_id] = poll
    return poll


@app.delete("/polls/{poll_id}", response_model=Poll)
async def delete_poll(poll_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")

    poll = polls.pop(poll_id)
    poll_votes.pop(poll_id, None)

    return poll


# VOTES

@app.post("/polls/{poll_id}/vote", response_model=Vote)
async def vote(poll_id: int, new_vote: VoteCreate):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")

    if isinstance(new_vote.choice, str):
        try:
            new_vote.choice = polls[poll_id].choices.index(new_vote.choice)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid choice")
    else:
        if new_vote.choice not in range(len(polls[poll_id].choices)):
            raise HTTPException(status_code=400, detail="Invalid choice")

    vote = Vote(**new_vote.dict(), id=len(poll_votes[poll_id]), poll_id=poll_id)

    poll_votes[poll_id][vote.id] = vote

    return vote


@app.patch("/polls/{poll_id}/vote", response_model=Vote)
async def update_vote(poll_id: int, vote_id: int, vote_update: VoteCreate):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    if vote_id not in poll_votes[poll_id]:
        raise HTTPException(status_code=404, detail="Vote not found")

    if isinstance(vote_update.choice, str):
        try:
            vote_update.choice = polls[poll_id].choices.index(vote_update.choice)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid choice")
    else:
        if vote_update.choice not in range(len(polls[poll_id].choices)):
            raise HTTPException(status_code=400, detail="Invalid choice")

    vote = poll_votes[poll_id][vote_id]

    vote = vote.copy(update=vote_update.dict(exclude_unset=True))

    poll_votes[poll_id][vote_id] = vote

    return vote


@app.delete("/polls/{poll_id}/vote", response_model=Vote)
async def delete_vote(poll_id: int, vote_id: int):
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    if vote_id not in poll_votes[poll_id]:
        raise HTTPException(status_code=404, detail="Vote not found")

    return poll_votes[poll_id].pop(vote_id)


@app.get("/polls/{poll_id}/results", response_model=Result)
async def get_results(poll_id: int):
    poll = polls[poll_id]
    results = {choice: 0 for choice in poll.choices}

    for vote in poll_votes[poll_id].values():
        results[poll.choices[vote.choice]] += 1

    max_votes = max(results.values())
    if max_votes == 0:
        outcome = "No votes yet"
    else:
        winners = [choice for choice, votes in results.items() if votes == max_votes]

        if len(winners) == 1:
            outcome = "Winner is " + winners[0]

        else:
            outcome = 'Tie between ' + ', '.join(winners)

    return Result(poll_id=poll_id, results=results, outcome=outcome)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
