from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import AgentResponse, AgentCreate

router = APIRouter()

@router.get("/api/agents", response_model=List[AgentResponse])
async def get_agents():
    agents = list(db.agents.find())
    return agents

@router.post("/api/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    agent_data = agent.dict()
    result = db.agents.insert_one(agent_data)
    agent_data["_id"] = str(result.inserted_id)
    return agent_data