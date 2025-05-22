from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Literal
import asyncio

app = FastAPI()

model_state = {
    "model_id": None,
    "status": "NOT_DEPLOYED"
}

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class CompletionRequest(BaseModel):
    messages: List[Message]

class ModelDeployRequest(BaseModel):
    model_id: str

async def simulate_model_deployment(model_id: str):
    model_state["status"] = "PENDING"
    await asyncio.sleep(1)  # Simulate waiting
    model_state["status"] = "DEPLOYING"
    await asyncio.sleep(2)  # Simulate setup
    model_state["status"] = "RUNNING"
    model_state["model_id"] = model_id

@app.get("/status")
def get_status():
    return {"status": model_state["status"]}

@app.get("/model")
def get_model():
    return {"model_id": model_state["model_id"] or "none"}

@app.post("/model")
async def deploy_model(req: ModelDeployRequest, background_tasks: BackgroundTasks):
    if not req.model_id:
        raise HTTPException(status_code=400, detail="Model ID required")
    if model_state["status"] in ["PENDING", "DEPLOYING"]:
        raise HTTPException(status_code=409, detail="Deployment already in progress")
    
    model_state["status"] = "PENDING"
    background_tasks.add_task(simulate_model_deployment, req.model_id)
    return {"status": "success", "model_id": req.model_id}

@app.post("/completion")
async def complete(req: CompletionRequest):
    if model_state["status"] != "RUNNING":
        return {"status": "error", "message": "Model is not running"}

    user_msg = req.messages[-1].content
    # Simulated response
    return {
        "status": "success",
        "response": [{"role": "assistant", "message": f"Echo: {user_msg}"}]
    }