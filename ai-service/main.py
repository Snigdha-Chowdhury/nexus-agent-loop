from fastapi import FastAPI
from pydantic import BaseModel
from graph.workflow import app as workflow_app
from langgraph.types import Command

app = FastAPI()

class StartRequest(BaseModel):
    topic: str

class ResumeRequest(BaseModel):
    thread_id: str
    decision: str

@app.post("/workflow/start")
def worflow_start(request: StartRequest):
    thread_id = str(__import__("uuid").uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    result = workflow_app.invoke({"topic": request.topic}, config=config)
    return {"thread_id": thread_id, "status": "interrupted", "critique": result.get("critique")}

@app.get("/workflow/status/{thread_id}")
def worflow_status(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = workflow_app.get_state(config)
    return {"current_state": state}

@app.post("/workflow/resume")
def workflow_resume(request: ResumeRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    result = workflow_app.invoke(Command(resume=request.decision), config=config)
    return {"status": "completed", "final_action": result.get("final_action")}