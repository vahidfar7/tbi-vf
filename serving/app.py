from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


class DeploymentStatus(str, Enum):
    NOT_DEPLOYED = "NOT_DEPLOYED"
    PENDING = "PENDING"
    DEPLOYING = "DEPLOYING"
    RUNNING = "RUNNING"

status = DeploymentStatus.NOT_DEPLOYED
current_model_id = None

class Message(BaseModel):
    role: str
    content: str

class CompletionRequest(BaseModel):
    messages: list[Message]

class CompletionResponse(BaseModel):
    status: str
    response: list[Message]

class ErrorResponse(BaseModel):
    status: str
    message: str

class ModelDeployRequest(BaseModel):
    model_id: str

class ModelDeployResponse(BaseModel):
    status: str
    model_id: str

@app.get("/status")
def get_status():
    return {"status": status}

@app.get("/model")
def get_model():
    if current_model_id is None:
        raise HTTPException(status_code=404, detail="No model currently deployed")
    return {"model_id": current_model_id}

@app.post("/model", response_model=ModelDeployResponse, responses={400: {"model": ErrorResponse}})
def deploy_model(request: ModelDeployRequest):
    global status, current_model_id
    model_id = request.model_id

    try:
        status = DeploymentStatus.DEPLOYING
        current_model_id = model_id
        status = DeploymentStatus.RUNNING
        return {"status": "success", "model_id": model_id}
    except Exception as e:
        status = DeploymentStatus.NOT_DEPLOYED
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/completion", response_model=CompletionResponse, responses={400: {"model": ErrorResponse}})
def complete(request: CompletionRequest):
    if status != DeploymentStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Model is not running")

    return {
        "status": "success",
        "response": [{"role": "assistant", "content": "This is a mock response"}]
    }